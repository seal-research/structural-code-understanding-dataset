import ast
import sys
import pandas as pd
from datasets import load_dataset
from HumanEval_Tracer import generate_symbols, add_line_identifiers

# Load the HumanEvalPlus dataset
dataset = load_dataset("evalplus/humanevalplus")

# Function to prepare the prompt and solution
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

# Function to extract inputs from the check function within the test string
def extract_inputs_from_check_function(test_code):
    try:
        tree = ast.parse(test_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "check":
                for inner_node in ast.walk(node):
                    if isinstance(inner_node, ast.Assign):
                        for target in inner_node.targets:
                            if isinstance(target, ast.Name) and target.id == "inputs":
                                inputs = ast.literal_eval(inner_node.value)
                                return inputs
    except Exception as e:
        print(f"Error extracting inputs: {e}")
    return []

# Function to run and trace the function calls
def run_code_and_trace(function_name, *args):
    line_numbers = []
    
    def trace_lines(frame, event, arg):
        if event == 'line':
            line_numbers.append(frame.f_lineno)
        return trace_lines

    sys.settrace(trace_lines)
    try:
        func = globals()[function_name]
        func(*args)
    finally:
        sys.settrace(None)
    
    return line_numbers

# Main processing function to create a dataset
def process_humanevalplus_dataset():
    results = []
    
    for i, task in enumerate(dataset['test']):
        test_code = task['test']
        prompt_code = task['prompt']
        solution_code = task['canonical_solution']
        entry_point = task['entry_point']
        human_eval_id = task['task_id']
        
        print(f"Processing task {human_eval_id}...")

        # Prepare the solution function
        try:
            candidate_function = prepare_solution_function(prompt_code, solution_code)
            print(f"Candidate function prepared for task {human_eval_id}.")
        except Exception as e:
            print(f"Error preparing function for task {i}: {e}")
            continue

        # Extract the inputs from the check function
        inputs = extract_inputs_from_check_function(test_code)
        
        if not inputs:
            print(f"No inputs found for task {i}")
            continue
        
        # Insert the candidate function into the global scope to trace it
        try:
            exec(candidate_function, globals())
            print(f"Function {entry_point} injected into global scope for tracing.")
        except Exception as e:
            print(f"Error injecting function for task {i}: {e}")
            continue
        
        # Trace execution for each input
        for input_args in inputs:
            if isinstance(input_args, list):
                try:
                    print(f"Tracing input: {input_args}")
                    executed_lines = run_code_and_trace(entry_point, *input_args)
                    
                    # Generate symbols using the existing `generate_symbols` function
                    candidate_with_indices, index_dict = add_line_identifiers(candidate_function, enumerate_letters=False)
                    candidate_with_symbols, symbol_dict = add_line_identifiers(candidate_function, enumerate_letters=True)
                    
                    # Add line identifiers using the existing `add_line_identifiers` function
                    executed_lines_symbols = [symbol_dict[line] for line in executed_lines if line in symbol_dict]
                    
                    # Prepare the data for the CSV in the required format
                    results.append({
                        'HumanEval_ID': human_eval_id,
                        'Name': entry_point,
                        'FunctionCall': entry_point,
                        'ExecutedLines': executed_lines,
                        'ExecutedLines_Symbols': executed_lines_symbols,
                        'Code_Indices': candidate_with_indices,
                        'Code_Symbols': candidate_with_symbols
                    })
                    print(f"Task {i} traced successfully.")
                except Exception as e:
                    print(f"Error tracing task {i} with input {input_args}: {e}")
    
    # Save the results to a CSV with the specified format
    results_df = pd.DataFrame(results)
    results_df.to_csv('HumanEvalPlus_trace_results.csv', index=False)
    print("Results saved to 'HumanEvalPlus_trace_results.csv'.")
    
process_humanevalplus_dataset()


