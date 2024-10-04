import os
import sys
import trace


# Import the bubble_sort function
from Sorting_Python.BubbleSort import bubble_sort

# Global list to store executed line numbers
executed_lines = []

import trace

# Assuming bubble_sort is imported from another file
# from your_module import bubble_sort

def run_func_and_trace(function_name:str, *args):
    # Create a Trace object to collect line numbers
    tracer = trace.Trace(count=False, trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])
    
    # Initialize a list to hold the line numbers
    line_numbers = []

    # Define a function to collect line numbers
    def collect_line_numbers(frame, event, arg):
        if event == 'line':
            # Get the line number from the frame
            line_number = frame.f_lineno
            line_numbers.append(line_number)
        return collect_line_numbers

    # Set the trace function
    sys.settrace(collect_line_numbers)

    func = globals()[function_name]  # Use globals to get the function from the current module
    func(*args)

    # Disable tracing
    sys.settrace(None)

    # Output the collected line numbers
    return line_numbers

# Example call to the bubble_sort function
result = run_func_and_trace('bubble_sort', [5, 2, 9, 1, 5, 6])  # Pass your desired input here
print(result)
