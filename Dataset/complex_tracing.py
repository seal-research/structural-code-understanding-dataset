import sys
import os
import pandas as pd
from typing import List, Optional
from collections import defaultdict

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
    base_folders = ['Recursion_prepared']  # List the folders containing your Python files
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
        output_file = 'Complex_Trace/program_traces_Python_Recursion.csv'
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No results to save")

if __name__ == "__main__":
    process_python_files()

