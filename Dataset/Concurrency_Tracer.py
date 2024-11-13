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
import nest_asyncio
nest_asyncio.apply()
import asyncio
from typing import TextIO, Callable
import concurrent
from queue import Queue
import random

import sys
import threading


def run_code_and_trace(filepath):
    """
    Executes the code in filepath and traces all lines from dynamically executed code
    including lines inside functions/classes defined within that code.
    Handles concurrent program traces with #START and #END markers.
    If the file contains asyncio, apply a different tracing method.
    """
    line_numbers = []
    concurrent_starts = set()
    concurrent_ends = set()

    # First pass: identify concurrent sections
    with open(filepath, "r") as file:
        lines = file.readlines()
        
    for i, line in enumerate(lines, 1):
        if '#START' in line:
            concurrent_starts.add(i)
        if '#END' in line:
            concurrent_ends.add(i)

    # Check if asyncio is present in the file
    with open(filepath, "r") as file:
        code = file.read()
        if 'asyncio' in code or 'async def' in code or 'await' in code:
            is_asyncio = True
        else:
            is_asyncio = False
    
    def trace_lines(frame, event, arg):
        # Only trace lines from dynamically executed code
        if event == 'line' and frame.f_code.co_filename == "<string>":
            line_number = frame.f_lineno
            
            # Check if this is a concurrent section start
            if line_number in concurrent_starts and not '(' in line_numbers:
                line_numbers.append('(')
                line_numbers.append(line_number)
            elif line_number in concurrent_ends and not ')' in line_numbers:
                line_numbers.append(')')
                line_numbers.append(line_number)
            else:
                line_numbers.append(line_number)
        return trace_lines

    try:

        # Apply the standard trace function to all threads
        sys.settrace(trace_lines)
        threading.settrace(trace_lines)
        
        # Execute the code in an isolated global environment
        shared_globals = globals().copy()  # Copy current globals to preserve imports
        isolated_globals = shared_globals.copy()
        
        # Execute the code
        with open(filepath, "r") as file:
            exec(file.read(), isolated_globals)
            
    except Exception as e:
        print(f"Error during execution of {filepath}: {str(e)}")
    finally:
        # Reset tracing for main thread
        sys.settrace(None)
        
    # If there are unclosed concurrent sections, add closing bracket at the end
    if '(' in line_numbers and not ')' in line_numbers:
        line_numbers.append(')')
            
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
        output_file = 'Complex_Trace/program_traces_Python_Concurrency_T.csv'
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results to save")
        
process_python_files()
