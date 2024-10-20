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
    
    print(f"Function name: {function_name}")
    print(f"Args: {args}")


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

    # Print the modified test code for debugging
    print("Modified Test Code:")
    print(modified_test_code)

    # Find all lines with the entry point
    lines_with_calls = []
    calls = []
    
    # Regex to match assert statements that call the entry point
    pattern = rf"assert\s+({entry_point}\s*\([^\)]*\)\s*==)"
    
    for line in modified_test_code.splitlines():
        if re.search(pattern, line):
            lines_with_calls.append(line)
            # Find the complete assert statement
            call_match = re.search(pattern, line)
            if call_match:
                start = call_match.start(1)
                end = len(line)
                calls.append(line[start:end].strip())
    
    # Print the lines containing the function calls
    print("\nLines with Function Calls:")
    for line in lines_with_calls:
        print("Line with function call:", line)

    # Print extracted function calls and catch potential errors
    print("\nExtracted Function Calls:")
    for call in calls:
        call = call.strip()  # Strip any extraneous whitespace
        try:
            print(call)
            # Here you could evaluate or process the call if needed
        except Exception as e:
            print(f"Error while processing call '{call}': {e}")

    return modified_test_code, calls

import ast

class FunctionCallExtractor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        # Extract function name
        function_name = ""
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = f"{node.func.value.id}.{node.func.attr}"

        # Extract arguments and their source segments
        arguments = [ast.get_source_segment(self.code, arg) for arg in node.args]
        self.calls.append((function_name, arguments))
        
        # Visit other nodes
        self.generic_visit(node)

    def set_code(self, code):
        self.code = code

class CallExtractor(ast.NodeVisitor):
    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.function_calls = []

    def visit_Call(self, node):
        # Check if the function called is the entry point
        if isinstance(node.func, ast.Name) and node.func.id == self.entry_point:
            # Extract raw arguments and store them as tuples
            args = tuple(self.get_arg_value(arg) for arg in node.args)
            self.function_calls.append(args)  # Group the args into a tuple
        self.generic_visit(node)

    def get_arg_value(self, arg):
        # Extract the argument value based on its type
        if isinstance(arg, ast.Constant):  # Python 3.8+
            return arg.value
        elif isinstance(arg, ast.Str):  # For older Python versions
            return arg.s
        elif isinstance(arg, ast.Num):  # For numeric literals
            return arg.n
        elif isinstance(arg, ast.List):  # For lists
            return [self.get_arg_value(el) for el in arg.elts]
        elif isinstance(arg, ast.Tuple):  # For tuples
            return tuple(self.get_arg_value(el) for el in arg.elts)
        elif isinstance(arg, ast.Set):  # For sets
            return {self.get_arg_value(el) for el in arg.elts}
        elif isinstance(arg, ast.Dict):  # For dictionaries
            return {self.get_arg_value(key): self.get_arg_value(value) for key, value in zip(arg.keys, arg.values)}
        # Add more cases as needed for different argument types
        return None

def extract_function_calls_with_ast(test_code: str, entry_point: str):
    test_code = test_code.replace('candidate', entry_point)
    # Parse the test code into an AST
    tree = ast.parse(test_code)

    # Create an instance of CallExtractor
    extractor = CallExtractor(entry_point)
    extractor.visit(tree)

    # Return modified test code and extracted function calls
    modified_test_code = test_code
    return modified_test_code, extractor.function_calls

# Sanitize function call arguments
def sanitize_args(args_str: str):
    args_str = args_str.strip()
    # Check for empty string or only spaces
    if not args_str:
        return None
    return args_str

def extend_dataset():
    filtered_df = pd.read_csv('HumanEval_trace_results_filtered.csv')

    # Extract existing IDs into a set for quick lookup
    existing_ids = set(filtered_df['HumanEval_ID'].tolist())
    
    # Prepare results list for new entries
    new_results = []
    
    # Load the HumanEval data again
    with open("HumanEval/human-eval-v2-20210705.jsonl", "r") as f:
        human_eval_data = [json.loads(line) for line in f]
    
    # Process each task in the dataset
    for task in human_eval_data:
        test_name = task['task_id']
        prompt_code = task['prompt']
        solution_code = task['canonical_solution']
        test_code = task['test']
        entry_point = task['entry_point']  # Extract entry point function name
        
        # Skip if ID already exists
        if test_name in existing_ids:
            continue
        
        # Prepare the solution function
        candidate_function = prepare_solution_function(prompt_code, solution_code)
        
        # Add the candidate function to globals so it can be traced
        exec(candidate_function, globals())  # Dynamically define the function in the current scope
        
        # Extract function calls from the test code
        modified_test_code, function_calls = extract_function_calls_with_ast(test_code, entry_point)
        print("Modified_Test_Code:", modified_test_code)
        print("Function_calls: ",function_calls)
    
        # Add line identifiers to the candidate function
        candidate_with_indices, index_dict = add_line_identifiers(candidate_function, enumerate_letters=False)
        candidate_with_symbols, symbol_dict = add_line_identifiers(candidate_function, enumerate_letters=True)
    
        # Trace the execution for each function call and collect results
        for call in function_calls:
            print("Call: ",call)
            args_str = call
            if args_str is not None:
                try:
                    # Safely parse the arguments (not necessary for AST)
                    # args = eval(f"({args_str})")  # Convert the call string to actual arguments
    
                    # Ensure args is a tuple
                    if not isinstance(args_str, tuple):
                        args = tuple(args_str)  # Convert to tuple if not already
                    else:
                        args = args_str  # Keep as is if it's already a tuple
                    print("args: ",args)
                    print("args: ",*args)
                    # Run the code and collect executed lines
                    lines_executed = run_code_and_trace(entry_point, *args)
    
                    # Check if the length of the executed lines is under 1025
                    if len(lines_executed) < 1025:
                        # Convert executed line numbers to corresponding symbols
                        executed_lines_symbols = [symbol_dict[line] for line in lines_executed if line in symbol_dict]
    
                        # Append the result as a new entry
                        new_results.append({
                            'HumanEval_ID': test_name,
                            'Name': entry_point,
                            'FunctionCall': call,
                            'ExecutedLines': lines_executed,
                            'ExecutedLines_Symbols': ''.join(executed_lines_symbols),
                            'Code_Indices': candidate_with_indices,
                            'Code_Symbols': candidate_with_symbols
                        })
    
                except (SyntaxError, NameError, TypeError, Exception) as e:
                    print(f"Error while processing call '{call}': {e}")
    
    # Convert new results to DataFrame
    new_results_df = pd.DataFrame(new_results)
    
    # Append new results to the existing DataFrame
    combined_df = pd.concat([filtered_df, new_results_df], ignore_index=True)
    
    # Save the combined DataFrame back to CSV
    combined_df.to_csv('HumanEval_trace_results_filtered_2.csv', index=False)
    
    # Output the number of new entries added
    print(f"Added {len(new_results)} new entries to 'HumanEval_trace_results_filtered.csv'.")
    
extend_dataset()

# =============================================================================
# # Example usage:
# with open("HumanEval/human-eval-v2-20210705.jsonl", "r") as f:
#     human_eval_data = [json.loads(line) for line in f]
# 
# # Prepare results list
# results = []
# 
# # Process each task in the dataset
# test_calls = 0
# test_call_list = []
# tasks = 0
# for task in human_eval_data:
#     test_name = task['task_id']
#     prompt_code = task['prompt']
#     solution_code = task['canonical_solution']
#     test_code = task['test']
#     entry_point = task['entry_point']  # Extract entry point function name
#     
#     if count_lines_of_code(solution_code) <= 2:
#         continue
#     
#     tasks += 1
# 
#     # Prepare the solution function
#     candidate_function = prepare_solution_function(prompt_code, solution_code)
#     
#     # Add the candidate function to globals so it can be traced
#     exec(candidate_function)  # Dynamically define the function in the current scope
# 
#     # Extract function calls from the test code
#     modified_test_code, function_calls = extract_function_calls(test_code, entry_point)
#     
#     # Add line numbers to the candidate function (the correct one)
#     candidate_with_indices, index_dict = add_line_identifiers(candidate_function, enumerate_letters=False)
#     candidate_with_symbols, symbol_dict = add_line_identifiers(candidate_function, enumerate_letters=True)
#     
#     # Trace the execution for each function call
#     for call in function_calls:
#         # Clean up the call to extract arguments
#         args_str = sanitize_args(call.strip())
#         
#         if args_str is not None:
#             try:
# 
#                 # Safely parse the arguments
#                 args = eval(f"({args_str})")  # Convert the call string to actual arguments
# 
#                 # Ensure args is a tuple (even if a single argument)
#                 if not isinstance(args, tuple):
#                     args = (args,)
#                 
#                 lines_executed = run_code_and_trace(entry_point, *args)
#                 
#                 # Convert executed line numbers to corresponding symbols (from solution code)
#                 executed_lines_symbols = [symbol_dict[line] for line in lines_executed if line in symbol_dict]
#                 
#                 # Append the result as a separate entry
#                 results.append({
#                     'HumanEval_ID': test_name,
#                     'Name': entry_point,
#                     'FunctionCall': call,
#                     'ExecutedLines': lines_executed,
#                     'ExecutedLines_Symbols': ''.join(executed_lines_symbols),
#                     'Code_Indices': candidate_with_indices,
#                     'Code_Symbols': candidate_with_symbols
#                 })
#                 test_calls+=1
#                 
#             except SyntaxError as e:
#                 print(f"SyntaxError while evaluating call '{call}': {e}")
#             except NameError as e:
#                 print(f"NameError while evaluating call '{call}': {e}")
#             except TypeError as e:
#                 print(f"TypeError while executing call '{call}': {e}")
#             except Exception as e:
#                 print(f"Unexpected error while processing call '{call}': {e}")
#         else:
#             print(f"Invalid argument format for call '{call}'.")
#     test_call_list.append(test_calls)
#     test_calls = 0
# 
# # Create a DataFrame from results
# df_results = pd.DataFrame(results)
# 
# # Save to CSV
# df_results.to_csv('HumanEval_trace_results.csv', index=False)
# 
# # Output the DataFrame
# print(df_results)
# ## unique tasks 95 7.6 tests per task
# print(tasks)
# =============================================================================
