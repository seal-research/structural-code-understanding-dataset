import pandas as pd
import sys
import inspect
import ast
import builtins

# Import all your sorting functions
from Sorting_Python.BubbleSort import *
from Sorting_Python.HeapSort import *
from Sorting_Python.InsertionSort import *
from Sorting_Python.MergeSort import *
from Sorting_Python.QuickSort import *
from Sorting_Python.SelectionSort import *
from Sorting_Python.ShellSort import *

# List of sorting algorithms
sorting_algorithms = [
    'bubble_sort',
    'min_heap_sort',
    'insertion_sort',
    'merge_sort',
    'quick_sort',
    'selection_sort',
    'shell_sort'
]

# Function to check if a function is recursive using AST
import ast
import inspect

# Function to check if a function is recursive using AST
import ast
import inspect

# Recursive function to check if a function or any of its helpers are recursive
def is_recursive(function_name: str):
    func = globals().get(function_name)  # Get the function from global scope
    if not func:
        print(f"Function {function_name} not found.")
        return False
    
    # Get the source code of the function
    source_code = inspect.getsource(func)
    
    # Parse the source code into an AST
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Error parsing {function_name}: {e}")
        return False

    print(f"Checking recursion for function: {function_name}")
    print(f"Source code:\n{source_code}\n")

    # AST visitor class to detect recursive calls and calls to helper functions
    class RecursiveCallVisitor(ast.NodeVisitor):
        def __init__(self, func_name):
            self.func_name = func_name
            self.is_recursive = False
            self.helper_functions = set()  # Track any helper functions

        def visit_Call(self, node):
            # Check if this function calls itself
            if isinstance(node.func, ast.Name):
                if node.func.id == self.func_name:
                    self.is_recursive = True
                    print(f"Recursive call detected in {self.func_name} on line {node.lineno}.")
                else:
                    # Skip built-in functions
                    if node.func.id in dir(builtins):
                        print(f"Skipping built-in function {node.func.id}.")
                    else:
                        # Track helper functions
                        self.helper_functions.add(node.func.id)
            self.generic_visit(node)

    # Initialize the visitor and traverse the AST
    visitor = RecursiveCallVisitor(function_name)
    visitor.visit(tree)

    # If recursion was already detected, return True
    if visitor.is_recursive:
        return True

    # Check if any helper functions are recursive
    for helper_func in visitor.helper_functions:
        print(f"Checking if helper function {helper_func} is recursive...")
        if is_recursive(helper_func):  # Recursively check helper functions
            return True

    return visitor.is_recursive

def format_source_code_with_line_numbers(source_code: str) -> str:
    lines = source_code.splitlines()
    numbered_code = "\n".join(f"{line}  # {i + 1}" for i, line in enumerate(lines))
    return numbered_code

def read_and_format_file_with_line_numbers(filepath: str) -> str:
    with open(filepath, 'r') as file:
        source_code = file.read()
    return format_source_code_with_line_numbers(source_code)

def get_function_source_code(func):
    source_file = inspect.getsourcefile(func)
    return read_and_format_file_with_line_numbers(source_file)

# Now, when you use the is_recursive function, it should correctly check if the function is recursive.


# Function to trace and collect line numbers for each sorting algorithm
def run_function_and_trace(function_name: str, *args):
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

# Test input
test_inputs = [[1,2,3],[5, 3, 1, 8, 6], [9, 7, 5, 3, 1, 8, 6, 4, 2, 0]]

# Create an empty dataframe to store the results
df_results = pd.DataFrame(columns=['Algorithm', 'Test Case', 'List Length', 'Executed Lines', 'Is Recursive'])

# Run the test for each sorting algorithm
for test_input in test_inputs:
    for algorithm in sorting_algorithms:
        func = globals().get(algorithm)
        line_numbers = run_function_and_trace(algorithm, test_input)
        recursive_flag = is_recursive(algorithm)  # Check if the function is recursive

        # Get the source code and format it with line numbers
        formatted_code = get_function_source_code(func)
        
        # Create a new dataframe for each row
        new_row = pd.DataFrame({
            'Algorithm': [algorithm],
            'Test Case': [test_input],           # Save the test case (the list)
            'List Length': len(test_input),  # Save the length of the list
            'Executed Lines': [line_numbers],    # Save the executed lines
            'Is Recursive': [recursive_flag],     # Save whether the function is recursive
            'Source Code': [formatted_code]
        })
        
        # Concatenate the new row to the existing dataframe
        df_results = pd.concat([df_results, new_row], ignore_index=True)

# Display the dataframe with results
print(df_results)

# Optionally, save the results to a CSV file
df_results.to_csv('sorting_algorithm_trace_results.csv', index=False)