import sys
import os
import io
import pandas as pd
from typing import List, Optional
from collections import defaultdict
from threading import Lock
from threading import Thread
from threading import Semaphore
import time
from time import sleep
from time import time
from datetime import datetime
from urllib.parse import urlparse
from datetime import date
import collections
import threading
from math import cos, pi, log, tan, sqrt
import concurrent.futures
import asyncio
from typing import TextIO
import concurrent

def run_code_and_trace(filepath):
    """
    Executes the code in filepath and traces all lines from dynamically executed code
    including lines inside functions/classes defined within that code.
    """
    line_numbers = []

    def trace_lines(frame, event, arg):
        # Only trace lines from dynamically executed code (e.g., via exec)
        if event == 'line' and frame.f_code.co_filename == "<string>":
            line_number = frame.f_lineno
            line_numbers.append(line_number)
        return trace_lines

    try:
        # Read the code and prepare to execute
        with open(filepath, "r") as file:
            code = file.read()

        # Apply the trace and execute the code
        sys.settrace(trace_lines)
        exec(code, globals())  # `exec` executes with tracing applied

    except Exception as e:
        print(filepath)
        print(f"Error during execution: {str(e)}")

    finally:
        # Reset tracing
        sys.settrace(None)

    return line_numbers

# Example usage in a function that processes files
def process_python_files():
    base_folders = ['OOP_prepared']  # List the folders containing your Python files
    results = []

    for folder in base_folders:
        python_folder = os.path.join(folder, 'Python')
        
        if not os.path.exists(python_folder):
            print(f"Folder not found: {python_folder}")
            continue
        
        for filename in os.listdir(python_folder):
            if filename.endswith('.py') and '_trace_' in filename:
                base_name = filename.split('_trace_')[0]
                file_path = os.path.join(python_folder, filename)
                
                try:
                    # Get traced line numbers
                    executed_lines = run_code_and_trace(file_path)
                    
                    # Add to results
                    results.append({
                        'Filename': base_name,
                        'Category': folder,
                        'ExecutedLines': executed_lines,
                    })
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
    
    # Create DataFrame and save to CSV
    if results:
        import pandas as pd
        df = pd.DataFrame(results)
        output_file = 'Complex_Trace/program_traces_Python_OOP.csv'
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results to save")

import re

def find_main_line(file_path):
    """
    Find the line number where __main__ is declared in a Python file.
    Handles potential whitespace variations in the if __name__ == '__main__' line.
    
    Args:
        file_path (str): Path to the Python file
        
    Returns:
        int: Line number where main begins, or -1 if not found
    """
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file.readlines(), 1):
                # Use regex to match the main declaration with flexible whitespace
                if re.match(r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:\s*$', line):
                    return i
        return -1
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return -1

def process_trace(df):
    """
    Process the DataFrame to trim traces based on main method location.
    
    Args:
        df (pd.DataFrame): DataFrame with columns 'filename', 'category', and 'trace'
        
    Returns:
        pd.DataFrame: Processed DataFrame with trimmed traces
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # Process each row
    for idx in range(len(result_df)):
        # Get file details
        filename = result_df.iloc[idx]['Filename']
        category = result_df.iloc[idx]['Category']
        
        # Calculate which trace file to look at (1-5 based on position in DataFrame)
        trace_num = (idx % 5) + 1
        
        # Construct path to corresponding trace file
        trace_file_path = os.path.join(
            category,
            'Python',
            f"{filename}_trace_{trace_num}.py"
        )
        
        # Find main line number
        main_line = find_main_line(trace_file_path)
        
        if main_line != -1:
            # Get the trace as a list of lines
            trace = result_df.iloc[idx]['ExecutedLines']
            
            # Convert trace to list if it's a string
            if isinstance(trace, str):
                trace_lines = eval(trace)
            else:
                trace_lines = trace
            
            # Find the first line number in trace that's greater than main_line
            trimmed_trace = []
            found_start = False
            
            for line in trace_lines:
                # Assuming each line starts with a line number
                try:
                    if line > main_line:
                        found_start = True
                    if found_start:
                        trimmed_trace.append(line)
                except (ValueError, IndexError):
                    # If line doesn't start with a number, keep it if we've found start
                    if found_start:
                        trimmed_trace.append(line)
            
            # Update the DataFrame with trimmed trace
            result_df.at[idx, 'ExecutedLines'] = str(trimmed_trace) if trimmed_trace else result_df.iloc[idx]['ExecutedLines']
    
    return result_df

def main(input_df):
    """
    Main function to process the trace DataFrame.
    
    Args:
        input_df (pd.DataFrame): Input DataFrame with columns 'filename', 'category', and 'trace'
        
    Returns:
        pd.DataFrame: Processed DataFrame with trimmed traces
    """
    # Validate input DataFrame
    required_columns = {'Filename', 'Category', 'ExecutedLines'}
    if not all(col in input_df.columns for col in required_columns):
        raise ValueError(f"Input DataFrame must contain columns: {required_columns}")
    
    # Process the traces
    processed_df = process_trace(input_df)
    
    return processed_df

if __name__ == "__main__":
    process_python_files()
    #new_df = main(pd.read_csv('Complex_Trace/program_traces_Python_Recursion.csv'))

