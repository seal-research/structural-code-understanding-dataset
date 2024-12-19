import os
os.environ["HF_HOME"]="/share/dutta/cache/huggingface"
from models.llm import LLM 
from prompts import PROMPTS
import difflib
import json
import pandas as pd
import re
import time
import argparse

def extract_last_python_list(text):
    # Use regex to find all lists in the format of Python lists
    matches = re.findall(r'\[.*?\]', text)
    # Return the last match if available, otherwise None
    return matches[-1] if matches else None

def calculate_distance(actual, predicted):
    """Calculate similarity between two lists of lines."""
    actual_str = ','.join(map(str, actual))
    predicted_str = ','.join(map(str, predicted))
    sequence = difflib.SequenceMatcher(a=actual_str, b=predicted_str)
    return sequence.ratio()  # Similarity ratio

def save_results_to_csv(results, filename):
    """Save the results to a CSV file."""    
    
    #results_df = pd.DataFrame(results, columns = ['Filename', 'Category', 'Predicted', 'Actual', 'Matched', 'Distance'])
    
    results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


def run_llm(model, df, topic, model_name):
    i=0
    results=[]
    for index, row in df.iterrows():
        i+=1
        prompt=PROMPTS[topic].format(row['Code_Indices'], row['Name'], row['FunctionCall'])

        model_input = [{"role": "system", "content": "some system prompt"}, {"role": "user", "content": prompt}]
        start_time=time.time()
        response = model.predict(model_input)
        total_time=time.time() - start_time
        print(f">>> Prompt: {prompt}")
        print(">>> Response:")
        print(response)
        print(f">>>Time: {total_time}")
    
        actual_lines = row['ExecutedLines']
    
        response = extract_last_python_list(response)

        # Calculate similarity or distance
        distance = calculate_distance(actual_lines, response)

        # Determine if the output matches the expected value
        matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

        # Append result to the list
        if(topic == 'HumanEval'):
            results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])
        else:
            results.append([row['Filename'], row['Category'], response, actual_lines, matching, distance])
        if i > 5:
            break

    outputfile="results_{0}_{1}.csv".format(topic, model_name)
    save_results_to_csv(results, outputfile)

    
if __name__ == '__main__':

    model_name = "qwen2.5-coder-32b"#llama-3.1-8b"
    kwargs = {'max_new_tokens': 1024, 'temperature': 0.0, 'top_p': 1.0}


    df = pd.read_csv('Dataset/HumanEval_trace_expanded_fixed_reannotated.csv')
    print(df.head())
    print(df.shape)
    topic="HumanEval"
    model = LLM.get_llm(model_name, kwargs, None)

    run_llm(model, df, topic, model_name) 
    
    
        


