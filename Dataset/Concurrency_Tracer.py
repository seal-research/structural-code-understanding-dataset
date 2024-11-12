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
from datetime import datetime
from urllib.parse import urlparse
from datetime import date
import collections
import threading
from math import cos, pi, log, tan, sqrt, exp
import concurrent.futures
import asyncio
from typing import TextIO, Callable
import concurrent
from queue import Queue
import random

def run_code_and_trace(filepath):
    """
    Executes the code in filepath and traces all lines from dynamically executed code
    including lines inside functions/classes defined within that code.
    Handles concurrent program traces with #START and #END markers.
    """
    line_numbers = []
    concurrent_starts = set()
    concurrent_ends = set()
    
    # First pass: identify concurrent sections
    with open(filepath, "r") as file:
        lines = file.readlines()
        
    for i, line in enumerate(lines, 1):
        if '#START' in line:
            # Move #START comment up only if it's alone on its line
            line_without_comment = line.replace('#START', '').strip()
            if i > 1 and not line_without_comment:  # Check if line is empty except for comment
                lines[i-2] = lines[i-2].rstrip() + ' #START\n'
                lines[i-1] = '\n'  # Empty line
                concurrent_starts.add(i-1)
            else:
                concurrent_starts.add(i)
        if '#END' in line:
            # Move #END comment up only if it's alone on its line
            line_without_comment = line.replace('#END', '').strip()
            if i > 1 and not line_without_comment:  # Check if line is empty except for comment
                lines[i-2] = lines[i-2].rstrip() + ' #END\n'
                lines[i-1] = '\n'  # Empty line
                concurrent_ends.add(i-1)
            else:
                concurrent_ends.add(i)
    
    # Write modified code back
    with open(filepath, "w") as file:
        file.writelines(lines)
    
    def trace_lines(frame, event, arg):
        # Only trace lines from dynamically executed code
        if event == 'line' and frame.f_code.co_filename == "<string>":
            line_number = frame.f_lineno
            
            # Check if this is a concurrent section start
            if line_number in concurrent_starts:
                line_numbers.append(f"({line_number}")
            # Check if this is a concurrent section end
            elif line_number in concurrent_ends:
                line_numbers.append(f"{line_number})")
            else:
                line_numbers.append(line_number)
        return trace_lines

    try:
        # Read the code and prepare to execute
        with open(filepath, "r") as file:
            code = file.read()
        # Apply the trace and execute the code
        shared_globals = globals().copy()  # Copy the current globals to preserve imports
        
        # Apply the trace and execute the code in an isolated global environment
        sys.settrace(trace_lines)
        print(filepath)
        
        # Execute the code in an isolated environment, preserving only the imports
        isolated_globals = shared_globals.copy()  # New globals for exec to isolate the state
        exec(code, isolated_globals)
    except Exception as e:
        print(filepath)
        print(f"Error during execution: {str(e)}")
    finally:
        # Reset tracing
        sys.settrace(None)
        
    # If there are unclosed concurrent sections, add closing bracket at the end
    if len([x for x in line_numbers if isinstance(x, str) and x.startswith("(")]) > len([x for x in line_numbers if isinstance(x, str) and x.endswith(")")]):
        if isinstance(line_numbers[-1], str):
            line_numbers[-1] = f"{line_numbers[-1]})"
        else:
            line_numbers[-1] = f"{line_numbers[-1]})"
    
    return line_numbers

def process_python_files():
    base_folders = ['Concurrency_prepared']  # List the folders containing your Python files
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
        output_file = 'Complex_Trace/program_traces_Python_Concurrency.csv'
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results to save")
        
process_python_files()