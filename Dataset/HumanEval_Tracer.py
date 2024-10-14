import json
import pandas as pd
import sys
import re
import string

# Helper function to generate symbols for line enumeration
def generate_symbols():
    letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    symbols = list('!@#$%^&*()_+-={}[]|:;<>,.?/~`')  # Add more symbols if needed
    return letters + symbols

# Function to add line identifiers to code
def add_line_identifiers(code, enumerate_letters=False):
    lines = code.split('\n')
    if enumerate_letters:
        # Use dynamically generated symbols for solution code lines
        symbols = generate_symbols()
        if len(lines) > len(symbols):
            raise IndexError("Not enough symbols to represent all lines.")
        numbered_lines = [f"{line}  # {symbols[i]}" for i, line in enumerate(lines) if line.strip()]
        symbol_dict = {i + 1: symbols[i] for i, line in enumerate(lines) if line.strip()}
    else:
        # Use numbers for test code lines
        numbered_lines = [f"{line}  # {i + 1}" for i, line in enumerate(lines)]
        symbol_dict = {i + 1: i + 1 for i, line in enumerate(lines)}
    return '\n'.join(numbered_lines), symbol_dict

def prepare_solution_function(prompt_code, solution_code):
    # Replace escape sequences with actual newlines
    prompt_code = prompt_code.replace('\\n', '\n')
    solution_code = solution_code.replace('\\n', '\n')
    
    # Combine prompt_code and solution_code directly while preserving formatting
    formatted_lines = []
    
    # Split the prompt code into lines
    lines = prompt_code.split('\n')
    
    # Initialize a flag to track if we are in a docstring
    in_docstring = False
    
    for line in lines:
        # Add the current line to formatted_lines
        formatted_lines.append(line)
        
        # Check if we are entering or leaving a docstring
        if '"""' in line:
            in_docstring = not in_docstring
        
        # If we leave the docstring and find a function signature, add a newline
        if not in_docstring and line.strip().startswith('def'):
            formatted_lines.append('')  # Add a newline after the function signature

    # Add the solution code at the end, ensuring it keeps its formatting
    formatted_lines.append(solution_code)

    # Join everything back together while preserving the formatting
    return '\n'.join(formatted_lines)

def count_lines_of_code(solution):
    lines = solution.split('\n')
    # Exclude empty lines and lines that are just function definitions or docstrings
    meaningful_lines = [line for line in lines if line.strip() and not line.strip().startswith(('def', '"""', 'return'))]
    return len(meaningful_lines)

# Function to trace and collect line numbers for the function calls
def run_code_and_trace(function_name: str, *args):
    # Initialize a list to hold the line numbers
    line_numbers = []

    # Define a function to collect line numbers
    def collect_line_numbers(frame, event, arg):
        if event == 'line':
            # Get the line number from the frame
            line_number = frame.f_lineno
            line_numbers.append(line_number)  # Collect all line numbers including duplicates
        return collect_line_numbers

    # Set the trace function
    sys.settrace(collect_line_numbers)

    try:
        # Dynamically retrieve and call the function
        func = globals()[function_name]  # Use globals to get the function from the current module
        func(*args)
    finally:
        # Disable tracing
        sys.settrace(None)

    # Output the collected line numbers
    return line_numbers  # Return the list without sorting

# Extract function calls from test code
def extract_function_calls(test_code: str, entry_point: str):
    # Replace 'candidate' with the actual entry point function name
    modified_test_code = test_code.replace("candidate", entry_point)

    # Use regex to find all calls to the entry point function
    calls = re.findall(rf"{entry_point}\s*\((.*?)\)", modified_test_code)
    
    return modified_test_code, calls

# Sanitize function call arguments
def sanitize_args(args_str: str):
    args_str = args_str.strip()
    # Check for empty string or only spaces
    if not args_str:
        return None
    return args_str

# Example usage:
with open("HumanEval/human-eval-v2-20210705.jsonl", "r") as f:
    human_eval_data = [json.loads(line) for line in f]

# Prepare results list
results = []

# Process each task in the dataset
test_calls = 0
test_call_list = []
tasks = 0
for task in human_eval_data:
    test_name = task['task_id']
    prompt_code = task['prompt']
    solution_code = task['canonical_solution']
    test_code = task['test']
    entry_point = task['entry_point']  # Extract entry point function name
    
    if count_lines_of_code(solution_code) <= 2:
        continue
    
    tasks += 1

    # Prepare the solution function
    candidate_function = prepare_solution_function(prompt_code, solution_code)
    
    # Add the candidate function to globals so it can be traced
    exec(candidate_function)  # Dynamically define the function in the current scope

    # Extract function calls from the test code
    modified_test_code, function_calls = extract_function_calls(test_code, entry_point)
    
    # Add line numbers to the candidate function (the correct one)
    candidate_with_indices, index_dict = add_line_identifiers(candidate_function, enumerate_letters=False)
    candidate_with_symbols, symbol_dict = add_line_identifiers(candidate_function, enumerate_letters=True)
    
    # Trace the execution for each function call
    for call in function_calls:
        # Clean up the call to extract arguments
        args_str = sanitize_args(call.strip())
        
        if args_str is not None:
            try:

                # Safely parse the arguments
                args = eval(f"({args_str})")  # Convert the call string to actual arguments

                # Ensure args is a tuple (even if a single argument)
                if not isinstance(args, tuple):
                    args = (args,)
                
                lines_executed = run_code_and_trace(entry_point, *args)
                
                # Convert executed line numbers to corresponding symbols (from solution code)
                executed_lines_symbols = [symbol_dict[line] for line in lines_executed if line in symbol_dict]
                
                # Append the result as a separate entry
                results.append({
                    'HumanEval_ID': test_name,
                    'Name': entry_point,
                    'FunctionCall': call,
                    'ExecutedLines': lines_executed,
                    'ExecutedLines_Symbols': ''.join(executed_lines_symbols),
                    'Code_Indices': candidate_with_indices,
                    'Code_Symbols': candidate_with_symbols
                })
                test_calls+=1
                
            except SyntaxError as e:
                print(f"SyntaxError while evaluating call '{call}': {e}")
            except NameError as e:
                print(f"NameError while evaluating call '{call}': {e}")
            except TypeError as e:
                print(f"TypeError while executing call '{call}': {e}")
            except Exception as e:
                print(f"Unexpected error while processing call '{call}': {e}")
        else:
            print(f"Invalid argument format for call '{call}'.")
    test_call_list.append(test_calls)
    test_calls = 0

# Create a DataFrame from results
df_results = pd.DataFrame(results)

# Save to CSV
df_results.to_csv('HumanEval_trace_results.csv', index=False)

# Output the DataFrame
print(df_results)
## unique tasks 95 7.6 tests per task
print(tasks)
