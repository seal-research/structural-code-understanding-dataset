import os
import logging
import pandas as pd
from google.oauth2 import service_account
import google.cloud.aiplatform
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Image, GenerationConfig
from anthropic import AnthropicVertex
from transformers import pipeline
from openai import AzureOpenAI
import requests
import openai
import vertexai
import json
import re

# Set up logging
logging.basicConfig(
    filename='model_queries.log',  # Log file name
    level=logging.INFO,             # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Read the CSV file using pandas
#df = pd.read_csv('Dataset/sorting_algorithm_trace_results.csv')
df = pd.read_csv('Dataset/HumanEval_trace_expanded_fixed_reannotated.csv')

# Path to your service account key file
key_path = "nbtest-439420-28cc48108dc9.json"

# Create credentials using the service account key
credentials = service_account.Credentials.from_service_account_file(key_path)

# Initialize Google Cloud AI Platform
google.cloud.aiplatform.init(project="nbtest-439420", location="us-east5", credentials=credentials)

# Load the API key from the JSON file
def load_api_key():
    with open("cs6158_Azure.json", "r") as file:
        data = json.load(file)
        return data["secret_key"]

# Azure configuration
AZURE_OPENAI_API_KEY = load_api_key()  # Get the key from the JSON file
AZURE_OPENAI_ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/"#"https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
AZURE_DEPLOYMENT_NAME = "gpt-4o"

alternative_id = 'nbtest-439420'


def prompt_claude(project_id: str, region: str, prompt: str, max_tokens: int = 1024):
    """Prompt the Claude model via Anthropic API."""
    client = AnthropicVertex(region=region, project_id=project_id)
    
    message = client.messages.create(
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        model="claude-3-5-sonnet@20240620",  # Specify the Claude model version
    )
    
    reply = message.model_dump_json(indent=2)
    return reply

def prompt_gemini(project_id: str, model_name: str, prompt: str, temperature: float = 0., max_tokens: int = 4096):
    """Prompt the Gemini model via Google Vertex AI."""
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(model_name)
        
    response = model.generate_content(prompt, generation_config=GenerationConfig(temperature=temperature))
    
    return response.text

def prompt_huggingface(model_name: str, prompt: str, max_length: int = 512, temperature: float = 0.7):
    """Prompt a Huggingface model using Transformers pipeline."""
    generator = pipeline("text-generation", model=model_name)
    
    response = generator(prompt, max_length=max_length, num_return_sequences=1, temperature=temperature)
    
    return response[0]["generated_text"]

def predict_large_language_model_sample(
    project_id: str,
    model_name: str,
    temperature: float,
    max_decode_steps: int,
    top_p: float,
    top_k: int,
    content: str,
    location: str = "us-central1",
    tuned_model_name: str = "",
):
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    
    if tuned_model_name:
        model = model.get_tuned_model(tuned_model_name)
        
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p,
    )
    
    print(f"Response from Model: {response.text}")
    return response.text

def prompt_gemini_with_backoff(project_id: str, model_name: str, prompt: str):
    """Wrap Gemini prompt with exponential backoff in case of rate limit."""
    def call_gemini():
        return prompt_gemini(project_id, model_name, prompt)
    return exponential_backoff_retry(call_gemini)



import time
import random
import difflib
import logging
import string

def fix_predicted_lines(predicted_str):
    """Fix the predicted lines format to include spaces after commas."""
    return predicted_str.replace(',', ', ')

def calculate_distance(actual, predicted):
    """Calculate similarity between two lists of lines."""
    actual_str = ','.join(map(str, actual))
    predicted_str = ','.join(map(str, predicted))
    sequence = difflib.SequenceMatcher(a=actual_str, b=predicted_str)
    return sequence.ratio()  # Similarity ratio

# Define prompt function for GPT-4
def prompt_gpt4o_with_backoff(prompt: str, max_tokens: int = 4096):
    """Wrap GPT-4 prompt with exponential backoff and general retry logic."""
    def call_gpt4o():
        headers = {
            "Content-Type": "application/json",
            "api-key": f"{AZURE_OPENAI_API_KEY}"
        }

        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,  # Deterministic output
            "top_p": 1.0,        # Full sampling
            "max_tokens": max_tokens
        }

        ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        reply = response.json()
        
        # Extracting the assistant's response
        return reply['choices'][0]['message']['content']

    def retry_with_general_errors(max_retries=3):
        """Retry function for general errors (not rate limits)."""
        for attempt in range(max_retries):
            try:
                # First try the exponential backoff for rate limits
                return exponential_backoff_retry(call_gpt4o)
            except Exception as e:
                # If it's not a rate limit error (already handled by exponential_backoff)
                if "429" not in str(e) and "529" not in str(e):
                    if attempt < max_retries - 1:  # Don't log on last attempt
                        logging.warning(f"Request failed with error: {str(e)}. Attempt {attempt + 1} of {max_retries}")
                        time.sleep(1)  # Simple 1-second delay between retries
                        continue
                raise e  # Re-raise the error if all retries are exhausted or if it's a rate limit error
        
        raise Exception(f"Failed after {max_retries} retries")

    return retry_with_general_errors()

def exponential_backoff_retry(func, retries=10, backoff_factor=2, max_wait=120):
    """Retry with exponential backoff in case of rate limit error (429)."""
    wait = 1
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "529" in str(e):
                logging.warning(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}. Retrying in {wait} seconds.")
                time.sleep(wait + random.uniform(0, 1))  # Adding jitter
                wait = min(wait * backoff_factor, max_wait)
            else:
                raise e
    logging.error("Exceeded maximum retries due to rate limit.")
    raise Exception("Exceeded maximum retries due to rate limit.")

# Define prompt function for Claude
def prompt_claude_with_backoff(project_id: str, region: str, prompt: str, max_tokens: int = 1024, temperature: float = 0.):
    """Wrap Claude prompt with exponential backoff."""
    def call_claude():
        client = AnthropicVertex(region=region, project_id=project_id)
        message = client.messages.create(
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            model="claude-3-5-sonnet@20240620",  # Specify Claude model version
            temperature = temperature,
        )
        reply = message.model_dump_json(indent=2)
        return fix_predicted_lines(json.loads(reply)['content'][0]['text'])

    return exponential_backoff_retry(call_claude)

def extract_last_python_list(text):
    # Use regex to find all lists in the format of Python lists
    matches = re.findall(r'\[.*?\]', text)
    # Return the last match if available, otherwise None
    return matches[-1] if matches else None

def extract_last_python_list_open(text):
    # Use regex to find all lists in the format of Python lists,
    # allowing for the last list to be unclosed if at the end of the string.
    matches = re.findall(r'\[.*?(?:\]|\s*$)', text)
    # Return the last match if available, otherwise None
    return matches[-1] if matches else None

# Generalized prompt function to handle both Gemini and Claude
def prompt_model_with_backoff(project_id: str, model_name: str, prompt: str, region=None):
    """Generalize the model prompt with exponential backoff."""
    if "claude" in model_name.lower():
        return prompt_claude_with_backoff(project_id, region, prompt)
    elif "gemini" in model_name.lower():
        return prompt_gemini_with_backoff(project_id, model_name, prompt)
    elif "gpt-4o" in model_name.lower() or "gpt4o" in model_name.lower():
        return prompt_gpt4o_with_backoff(prompt)
    else:
        raise ValueError("Unsupported model. Please use either 'claude','gemini' or 'gpt4o'.")

def process_batch(batch_df, model_name, project_id, region, topic='HumanEval'):
    """Process a batch of requests."""
    batch_results = []
    for index, row in batch_df.iterrows():
        try:
            if(topic=='HumanEval'):
                # Dynamically generate the prompt for each row
                prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call, of course.*
                In addition to the function, I will give you an initial input and the called function.
                It is your task to return the called lines, in order, as a list. I will give you an example:
                Source Code : """def simple_loop(x): #1
                                    for i in range(3): #2
                                        print(i+x) #3
                                    return i #4
                              """
                Input: (5)
                Correct solution: [2,3,2,3,2,3,2,4]
                Now I will give you your task.
                Here is the source code: {row['Code_Indices']}
                Here is the called function: {row['Name']}
                Here is the input to the function {row['FunctionCall']}
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Think about the solution step-by-step,
                going through execution steps one at a time. Finally, print the solution as a list of executed steps.
            '''
            elif(topic=='Recursion' or topic=='OOP'):
                prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call of course.*
                In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined in the 
                main method, which means the signature will be read once, but not the body.
                It is your task to return the called lines while executing the main, in order, as a list. I will give you an example:
                Source Code : """def simple_loop(x): #1
                                    for i in range(3): #2
                                        print(i+x) #3
                                    return i #4
                                #5
                                if __name__ == "__main__":#6
                                   simple_loop(5)#7
                              """
                Correct solution: [7,2,3,2,3,2,3,2,4]
                Now I will give you the code for your task.
                Here is the source code: {row['Code_Indices']}
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature line during a call. Print the solution as a list of executed steps.
                Do not produce any other output.
            '''
            elif(topic=='Concurrency'):
                prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call of course.*
                In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined in the 
                main method, which means the signature will be read once, but not the body.
                It is your task to return the called lines while executing the main, in order, as a list. The contained code may contain concurrency. For this purpose, you are supposed to mark the corresponding lines
                using parantheses. In particular, an opening paranthesis should be placed once concurrency starts and a closing one should be placed once it ends (if it concurrency never ends explicitly, place it at the very end).
                I will give you an example:
                Source Code : """def task(name):#1
                                    print("Task starting")#2
                                    time.sleep(2)#3
                                    print("Task completed")#4
                                #5
                                if __name__ == "__main__":#6
                                    thread1 = threading.Thread(target=task, args=('A',))#7
                                    thread2 = threading.Thread(target=task, args=('B',))#8
                                #9
                                    thread1.start()#10
                                    thread2.start()#11
                                #12
                                    thread1.join()#13
                                    thread2.join()#14
                                #15
                                    print("All tasks completed")#16
                              """
                Correct solution: [7,8,(,10,2,3,4,11,2,3,4,13,14,),16]
                Due to the concurrency, execution order may vary. You can pick any valid combination here as long as it is marked correctly with the parentheses.
                Now I will give you the code for your task.
                Here is the source code: {row['Code_Indices']}
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature line during a call. Print the solution as a list of executed steps.
                Do not produce any other output.
                '''
            
            # Use the appropriate model with backoff
            response = prompt_model_with_backoff(project_id ,model_name, prompt, region)

            actual_lines = row['ExecutedLines']

            response = extract_last_python_list(response)

            # Calculate similarity or distance
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            if(topic == 'HumanEval'):
                batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])
            else:
                batch_results.append([row['Filename'], row['Category'], response, actual_lines, matching, distance])
        except Exception as e:
            if(topic == 'HumanEval'):
                print(f"Error in entry {row['HumanEval_ID']}: {e}")
                logging.error(f"Error in entry {row['HumanEval_ID']}: {e}")
                batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], "ERROR", "ERROR", False, "N/A"])
            else:
                print(f"Error in entry {row['Filename']}: {e}")
                logging.error(f"Error in entry {row['Filename']}: {e}")
                batch_results.append([row['Filename'], row['Category'], "ERROR", "ERROR", False, "N/A"])

    return batch_results

def batch_test_llm_on_code(df, model_name, project_id, batch_size=10, region=None, topic='HumanEval'):
    """Test LLM on all entries in the dataset, processing requests in batches."""
    total_results = []
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        batch_df = df[start_idx:end_idx]
        
        logging.info(f"Processing batch {batch_num + 1} of {num_batches}.")
        
        # Process the current batch
        batch_results = process_batch(batch_df, model_name, project_id, region, topic)
        
        # Add batch results to the total results
        total_results.extend(batch_results)

    return total_results

df = pd.read_csv("Dataset/Complex_Trace/program_traces_Python_Concurrency_Lines.csv")
results = batch_test_llm_on_code(df, 'claude-3-5-sonnet@20240620', alternative_id, region='us-east5', topic='Concurrency')

# Save results to CSV
def save_results_to_csv(results, filename="Model_HumanEval.csv"):
    """Save the results to a CSV file."""
    if not ("HumanEval" in filename or "humaneval" in filename):
        print("Not HumanEval")
        results_df = pd.DataFrame(results, columns = ['Filename', 'Category', 'Predicted', 'Actual', 'Matched', 'Distance'])
    else:
        results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

save_results_to_csv(results, filename='Dataset/Claude_Concurrency_Trace_Direct_T0.csv')

def resend_failed_requests(csv_path, project_id, model_name, region=None):
    """
    Resend failed GPT-4 requests for rows where an error occurred and overwrite the existing CSV with new results.
    
    Args:
        csv_path (str): Path to the original CSV file.
        project_id (str): Azure or other project identifier.
        model_name (str): Model name, e.g., "gpt-4o".
        region (str): Optional, region for model if needed.
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Identify the failed entries - assuming "ERROR" is logged in a specific column (e.g., 'response')
    failed_entries = df[df['response'] == "ERROR"]
    
    valid_rows = []
    
    
    # Iterate over failed entries and re-send the requests
    for index, row in failed_entries.iterrows():
        
        predicted = row['Predicted']
        actual = row['ExecutedLines']
        
        try:
            actual_list = eval(actual) if isinstance(actual, str) else actual
        except:
            actual_list = []

        # Exclude rows with lists longer than 1024
        if len(actual_list) > 1024:
            continue
        
        # Check conditions to append rows without resending or proceed with resending request
        if predicted == 'ERROR' or predicted == '[]' or predicted == actual or any(arg in actual_list for arg in eval(predicted)):
            valid_rows.append(row)
            continue  # Skip sending request
        
        try:
            # Dynamically generate the prompt for the failed row
            prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
            In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
            To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
            The following is very important! *Please note that the function signatures are generally not called,
            instead you should start with the first line of the function. This does not apply to the function call, of course.*
            In addition to the function, I will give you an initial input and the called function.
            It is your task to return the called lines, in order, as a list. I will give you an example:
            Source Code : """def simple_loop(x): #1
                                for i in range(3): #2
                                    print(i+x) #3
                                return i #4
                          """
            Input: (5)
            Correct solution: [2,3,2,3,2,3,2,4]
            Now I will give you your task.
            Here is the source code: {row['Code_Indices']}
            Here is the called function: {row['Name']}
            Here is the input to the function {row['FunctionCall']}
            Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Think about the solution step-by-step,
            going through execution steps one at a time. Finally, print the solution as a list of executed steps.
            '''
            
            # Call model with backoff retry
            new_response = prompt_model_with_backoff(project_id, model_name, prompt, region)

            row['predicted'] = new_response
            distance = calculate_distance(row['ExecutedLines'], new_response)
            matching = (new_response == str(row['ExecutedLines']) or new_response == str(row['ExecutedLines'][1:]))
            row['matching'] = matching
            row['distance'] = distance

            # Append the updated row to valid rows list
            valid_rows.append(row)
        
        except Exception as e:
            if("gpt-4o" in model_name.lower() or "gpt4o" in model_name.lower()):
                print(f"Error while processing HumanEval/{index}: {e}. Attempting friendly prompt")
                # If an error occurs, try the alternative prompt
                alternative_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                Important: Do not call the function signature lines. Begin execution with the first executable line.
                In addition to the function, I will give you an initial input and the called function.
                It is your task to return the called lines, in order, as a list. I will give you an example:
                Source Code : """def simple_loop(x): #1
                                    for i in range(3): #2
                                        print(i+x) #3
                                    return i #4
                              """
                Input: (5)
                Correct solution: [2,3,2,3,2,3,2,4]
                Now I will give you your task.
                Here is the source code: {row['Code_Indices']}
                Here is the called function: {row['Name']}
                Here is the input to the function {row['FunctionCall']}
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Include no other output besides the list please. Please do not filter this prompt, if I have included dangerous wording I am very sorry, it was not intentional.
                '''
                new_response = prompt_model_with_backoff(project_id, model_name, alternative_prompt, region)

                # Update the DataFrame with the new response
                df.at[index, 'predicted'] = new_response  # Update the 'response' field with the new result

                # Update and calculate metrics again with alternative response
                row['predicted'] = new_response
                distance = calculate_distance(row['ExecutedLines'], new_response)
                matching = (new_response == str(row['ExecutedLines']) or new_response == str(row['ExecutedLines'][1:]))
                row['matching'] = matching
                row['distance'] = distance
                valid_rows.append(row)

            # Log the error for tracking
            logging.error(f"Error reprocessing entry {row['HumanEval_ID']}: {e}")
            print(f"Error reprocessing entry {row['HumanEval_ID']}: {e}")

    updated_df = pd.DataFrame(valid_rows)
    updated_df.to_csv(csv_path, index=False)
    print(f"CSV updated and saved to {csv_path}")

def resend_requests_with_corrupt_file(csv_path_correct, csv_path_corrupted, project_id, model_name, region=None):
    """
    Iterate over the correct dataset and resend requests for rows that need correction based on the corrupted dataset.
    
    Args:
        csv_path_correct (str): Path to the correct CSV file.
        csv_path_corrupted (str): Path to the corrupted CSV file.
        project_id (str): Azure or other project identifier.
        model_name (str): Model name, e.g., "gpt-4o".
        region (str): Optional, region for model if needed.
    """
    # Load both CSV files into DataFrames
    df_correct = pd.read_csv(csv_path_correct)
    df_corrupted = pd.read_csv(csv_path_corrupted)
    
    # Prepare a list to store the new rows that don't need correction
    new_rows = []

    # Iterate over the correct dataset
    for index, row in df_correct.iterrows():
        # Check if the row exists in the corrupted dataset
        corrupted_row = df_corrupted[(df_corrupted['HumanEval_ID'] == row['HumanEval_ID']) & 
                                      (df_corrupted['FunctionCall'] == row['FunctionCall'])]
        
        actual = row['ExecutedLines']
        
        if not corrupted_row.empty or len(actual>1024):
            # Check the conditions for sending requests
            predicted = corrupted_row['Predicted'].values[0]
            arguments = '['+row['FunctionCall']+']'
            
            try:
                actual_list = eval(actual) if isinstance(actual, str) else actual
                argument_list = eval(arguments) if isinstance(arguments, str) else arguments
                if predicted != 'ERROR':
                    predicted_list = eval(predicted) if isinstance (predicted, str) else eval(predicted+']')
            except:
                actual_list = []
                argument_list = []
                predicted_list = []

            # Check conditions
            if predicted == 'ERROR' or predicted == '[]':
                pass  # Request will be sent
            elif predicted == arguments or predicted_list == argument_list:
                pass  # Request will be sent
            elif len(actual_list) > 1024:
                continue  # Row is invalid due to its execution trace being too long
            else:
                # Condition met to copy row without resending
                new_rows.append(row)
                continue  # Skip sending request

        # If row not present or conditions apply, send request
        prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
        In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
        To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
        The following is very important! *Please note that the function signatures are generally not called,
        instead you should start with the first line of the function. This does not apply to the function call, of course.*
        In addition to the function, I will give you an initial input and the called function.
        It is your task to return the called lines, in order, as a list. I will give you an example:
        Source Code : """def simple_loop(x): #1
                            for i in range(3): #2
                                print(i+x) #3
                            return i #4
                      """
        Input: (5)
        Correct solution: [2,3,2,3,2,3,2,4]
        Now I will give you your task.
        Here is the source code: {row['Code_Indices']}
        Here is the called function: {row['Name']}
        Here is the input to the function {row['FunctionCall']}
        Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Think about the solution step-by-step,
        going through execution steps one at a time. Finally, print the solution as a list of executed steps.
        '''
        
        try:
            new_response = prompt_model_with_backoff(project_id, model_name, prompt, region)
            
            actual_lines = row['ExecutedLines']

            response = extract_last_python_list_open(new_response)

            # Calculate similarity or distance
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            new_rows.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])

        except Exception as e:
            logging.error(f"Error processing entry {row['HumanEval_ID']}: {e}")
            print(f"Error processing entry {row['HumanEval_ID']}: {e}")

    # Create a DataFrame from the new rows and save it to a new CSV
    df_new = pd.DataFrame(new_rows)
    df_new.to_csv('Claude3.5-Sonnet_HumanEval_CoT_fixed.csv', index=False)
    print(f"Corrected results saved to 'Claude3.5-Sonnet_HumanEval_CoT_fixed.csv'")
    
import pandas as pd
import re
import logging

def is_sublist_contained(sub_list, main_list):
    # Flatten the 2D main_list to handle nested structures
    flattened_list = []
    for item in main_list:
        if isinstance(item, list):
            flattened_list.extend(item)
        else:
            flattened_list.append(item)
    
    # Check if all elements of sub_list are in the flattened main_list
    return all(elem in flattened_list for elem in sub_list)

def resend_requests_with_criteria(csv_path_correct, csv_path_corrupted, project_id, model_name, region=None):
    """
    Iterate over the correct dataset and resend requests for rows that need correction based on the corrupted dataset.
    
    Args:
        csv_path_correct (str): Path to the correct CSV file.
        csv_path_corrupted (str): Path to the corrupted CSV file.
        project_id (str): Azure or other project identifier.
        model_name (str): Model name, e.g., "gpt-4o".
        region (str): Optional, region for model if needed.
    """
    # Load both CSV files into DataFrames
    df_correct = pd.read_csv(csv_path_correct)
    df_corrupted = pd.read_csv(csv_path_corrupted)
    
    # Prepare a list to store the new rows that don't need correction
    new_rows = []

    # Iterate over the correct dataset
    for index, row in df_correct.iterrows():
        # Check if the row exists in the corrupted dataset
        corrupted_row = df_corrupted[(df_corrupted['HumanEval_ID'] == row['HumanEval_ID']) & 
                                      (df_corrupted['FunctionCall'] == row['FunctionCall'])]
        
        actual = row['ExecutedLines']
        
        if not corrupted_row.empty:
            # Extract the predicted value from the corrupted row
            predicted = corrupted_row['Predicted'].values[0]
            arguments = '[' + row['FunctionCall'] + ']'
            
            try:
                actual_list = eval(actual) if isinstance(actual, str) else actual
                argument_list = eval(arguments) if isinstance(arguments, str) else arguments
                
                if predicted != 'ERROR' and predicted != '[]':
                    predicted_list = eval(predicted) if isinstance(predicted, str) else predicted

            except Exception as e:
                logging.error(f"Error evaluating lists for entry {row['HumanEval_ID']}: {e}")
                actual_list = []
                argument_list = []
                predicted_list = []

            # Check conditions for sending requests
            if predicted == 'ERROR' or predicted == '[]' or predicted == arguments or is_sublist_contained(predicted_list, argument_list):
                # Resend request logic here
                prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call, of course.*
                In addition to the function, I will give you an initial input and the called function.
                It is your task to return the called lines, in order, as a list. I will give you an example:
                Source Code : """def simple_loop(x): #1
                                    for i in range(3): #2
                                        print(i+x) #3
                                    return i #4
                              """
                Input: (5)
                Correct solution: [2,3,2,3,2,3,2,4]
                Now I will give you your task.
                Here is the source code: {row['Code_Indices']}
                Here is the called function: {row['Name']}
                Here is the input to the function {row['FunctionCall']}
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Think about the solution step-by-step,
                going through execution steps one at a time. Finally, print the solution as a list of executed steps.
                '''
                
                try:
                    
                    print("Sending Request")
                    
                    new_response = prompt_model_with_backoff(project_id, model_name, prompt, region)

                    response = extract_last_python_list_open(new_response)
                    distance = calculate_distance(actual, response)
                    matching = (response == str(actual) or response == str(actual)[1:])

                    # Append result to the new rows list
                    new_rows.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual, matching, distance])

                except Exception as e:
                    logging.error(f"Error processing entry {row['HumanEval_ID']}: {e}")
                    print(f"Error processing entry {row['HumanEval_ID']}: {e}")

            else:
                # Copy the row as is without modification
                print("Adding correct row")
                new_rows.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], 
                                 corrupted_row['Predicted'].values[0], 
                                 row['ExecutedLines'], 
                                 corrupted_row['Matched'].values[0],  # Retain original matched status
                                 corrupted_row['Distance'].values[0]])  # Retain original distance


    # Create a DataFrame from the new rows and save it to a new CSV
    df_new = pd.DataFrame(new_rows, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 
                                              'ExecutedLines', 'Matched', 'Distance'])
    df_new.to_csv('Claude3.5-Sonnet_HumanEval_CoT_fixed.csv', index=False)
    print(f"Corrected results saved to 'Claude3.5-Sonnet_HumanEval_CoT_fixed.csv'")



# Interesting : Gemini gave out: HumanEval/132,is_nested,'[]]]]]]]]]]',"[17, 18, 19, 20, 21, 22, 23, 19, 20, 22, 23,  ... (repeats 9 more times), 19, 24, 25, 26, 27, 28, 29, 30, 31, 32]","[17, 18, 19, 20, 21, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 20, 23, 19, 24, 25, 26, 27, 28, 29, 30, 31, 28, 32]",False,0.26013513513513514
# once

# Example usage with generalized prompt
#model_name = "claude-3-5-sonnet@20240620"  # or use "gemini-1.5-pro-002"  "gpt4o"
#region = "us-east5"  # Required for Claude
#resend_requests_with_criteria('Dataset/HumanEval_trace_expanded_fixed_reannotated.csv', 'Claude3.5-Sonnet_HumanEval_CoT.csv', 'nbtest-439420', model_name, region=region)

#results = batch_test_llm_on_code(df, model_name, project_id = 'cs6158-structuralunderstanding', batch_size=20, region=region)
#save_results_to_csv(results, "GPT4o_HumanEval_CoT.csv")


# Load the result CSV and the original dataset
#result_csv_path = 'Claude_HumanEval_fixed.csv'

# Load the CSVs into DataFrames
import re

def clean_predictions(df):
    """Clean the predictions by filtering out irrelevant content and recomputing metrics."""
    cleaned_results = []
    
    for index, row in df.iterrows():
        predicted = row['Predicted']
        actual = row['Actual']
        human_eval_id = row['HumanEval_ID']
        
        # Remove anything before the first '['
        predicted = predicted[predicted.find('['):] if '[' in predicted else 'ERROR'
        
        # Remove entries where the actual trace is longer than 1024
        if len(actual) > 1024:
            continue
        
        # Regular expression to match the expected output format
        pattern = r'\[\d+(?:,\s*\d+)*\s*\]'

        # Attempt to find a match
        match = re.search(pattern, predicted)
        
        if match:
            cleaned_predicted = match.group(0)
        else:
            # If closing bracket is missing and it ends with a number or a comma
            if predicted.endswith((' ', ',', *map(str, range(10)))):
                cleaned_predicted = predicted.strip()
                # No error reporting, just set to cleaned value
            else:
                cleaned_predicted = "ERROR"

        # Recompute matching and distance metrics
        matched = cleaned_predicted == str(actual)
        distance = calculate_distance(actual, cleaned_predicted)
        
        # Append cleaned result to the list
        cleaned_results.append([human_eval_id, row['Name'], row['FunctionCall'], cleaned_predicted, actual, matched, distance])
    
    # Create a DataFrame from the cleaned results
    cleaned_df = pd.DataFrame(cleaned_results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    
    return cleaned_df



# =============================================================================
#  # Define the paths for the CSV files
#expanded_csv_path = 'Dataset/HumanEval_trace_expanded_fixed_reannotated.csv'
#results_csv_path = 'GPT4o_HumanEval_CoT.csv'
  
# Load the expanded and results CSVs into DataFrames
# =============================================================================
# expanded_df = pd.read_csv(expanded_csv_path)
# results_df = pd.read_csv(results_csv_path)
# 
# # Create a set of existing HumanEval_ID and FunctionCall pairs
# existing_pairs = set(zip(results_df['HumanEval_ID'], results_df['FunctionCall']))
# #  
# # # Prepare a list to hold new results
# new_results = []
#   
# # Iterate over the rows in the expanded DataFrame
# for _, row in expanded_df.iterrows():
#      human_eval_id = row['HumanEval_ID']
#      function_call = row['FunctionCall']
#  
#      # Check if the pair already exists
#      if (human_eval_id, function_call) not in existing_pairs:
#          # Prepare the prompt for the model
#          prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
#          In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
#          To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
#          The following is very important! *Please note that the function signatures are generally not called,
#          instead you should start with the first line of the function. This does not apply to the function call, of course.*
#          In addition to the function, I will give you an initial input and the called function.
#          It is your task to return the called lines, in order, as a list. I will give you an example:
#          Source Code : """def simple_loop(x): #1
#                              for i in range(3): #2
#                                  print(i+x) #3
#                              return i #4
#                        """
#          Input: (5)
#          Correct solution: [2,3,2,3,2,3,2,4]
#          Now I will give you your task.
#          Here is the source code: {row['Code_Indices']}
#          Here is the called function: {row['Name']}
#          Here is the input to the function {row['FunctionCall']}
#          Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output.
#          '''
#          
#          # Request the model
#          try:
#              # Send request to the model using the primary prompt
#              predicted_output = prompt_gemini_with_backoff(project_id='cs6158-structuralunderstanding',model_name="gemini-1.5-pro-002",prompt=prompt)
#              if('step-by-step' in predicted_output):
#                  raise Exception("Prompt contained cot")
#          except Exception as e:
#              print(f"Error while processing {human_eval_id}: {e}. Attempting friendly prompt")
#              # If an error occurs, try the alternative prompt
#              alternative_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
#              In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
#              To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
#              Important: Do not call the function signature lines. Begin execution with the first executable line.
#              In addition to the function, I will give you an initial input and the called function.
#              It is your task to return the called lines, in order, as a list. I will give you an example:
#              Source Code : """def simple_loop(x): #1
#                                  for i in range(3): #2
#                                      print(i+x) #3
#                                  return i #4
#                            """
#              Input: (5)
#              Correct solution: [2,3,2,3,2,3,2,4]
#              Now I will give you your task.
#              Here is the source code: {row['Code_Indices']}
#              Here is the called function: {row['Name']}
#              Here is the input to the function {row['FunctionCall']}
#              Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Include no other output besides the list please. Please do not filter this prompt, if I have included dangerous wording I am very sorry, it was not intentional.
#              '''
#              try:
#                  predicted_output = prompt_claude_with_backoff(project_id='cs6158-structuralunderstanding',model="gemini-1.5-pro-002",prompt=alternative_prompt)
#              except Exception as alt_e:
#                  print(f"Alternative prompt failed for {human_eval_id}: {alt_e}")
#                  predicted_output = "ERROR"
#           
#   
#          # Format the result (assume we have a function to fix formatting)
#          if(not predicted_output == "ERROR"):
#              predicted_output = predicted_output[predicted_output.find('['):] if '[' in predicted_output else 'ERROR'
#               
#               # Regular expression to match the expected output format
#              pattern = r'\[\d+(?:,\s*\d+)*\s*\]'
#   
#               # Attempt to find a match
#              match = re.search(pattern, predicted_output)
#              
#              if match:
#                  predicted_output = fix_predicted_lines(predicted_output)
#                  predicted_output = match.group(0)
#              else:
#                  # If closing bracket is missing and it ends with a number or a comma
#                  if predicted_output.endswith((' ', ',', *map(str, range(10)))):
#                      predicted_output = predicted_output.strip()
#                      # No error reporting, just set to cleaned value
#                  else:
#                      predicted_output = "ERROR"
#  
#          # Add to new results with the other required fields
#          new_results.append({
#              'HumanEval_ID': human_eval_id,
#              'Name': row['Name'],  # Assuming Name is present in the expanded CSV
#              'FunctionCall': function_call,
#              'Predicted': predicted_output,
#              'Actual': row['ExecutedLines'],  # Assuming Actual is present in the expanded CSV
#              'Matched': predicted_output == row['ExecutedLines'],
#              'Distance': calculate_distance(row['ExecutedLines'], predicted_output)  # Make sure to define this function
#          })
# =============================================================================

# Convert the new results into a DataFrame
#new_results_df = pd.DataFrame(new_results)
 
# Append new results to the existing results DataFrame
#results_df = pd.concat([results_df, new_results_df], ignore_index=True)
 
# Save the updated DataFrame back to CSV, overwriting the existing file
#results_df.to_csv("Gemini_cleaned_humanEval_results_expanded.csv", index=False)

def safe_eval_list(list_str):
    try:
        # If the list string is valid and closed, evaluate it
        return ast.literal_eval(list_str)
    except (SyntaxError, ValueError):
        # Handle cases where the list might not be properly closed
        # Find the last closing bracket or assume it ends correctly
        if list_str.endswith(']'):
            return ast.literal_eval(list_str)
        elif list_str.strip()[-1] in '0123456789':  # If it ends with a digit
            # Attempt to close it with a closing bracket
            corrected_str = list_str + ']'
            return ast.literal_eval(corrected_str)
        elif list_str.strip()[-1] == ',':
            # If the list string is completely malformed, return an empty list
            corrected_str = list_str[:-1]+ ']'
            return ast.literal_eval(corrected_str)
        elif list_str == "ERROR":
            return [600]
        else:
            raise Exception("Malformed")


import ast


def eliminate_repetitions_and_compute_distances(new_results_df: pd.DataFrame, output_csv: str):
    """
    Filters a DataFrame for entries with consecutive duplicate lines in 'Actual',
    eliminates those duplicates, and recomputes 'Matched' and 'Distance'.
    
    Parameters:
        new_results_df (pd.DataFrame): Input DataFrame containing results.
        output_csv (str): The path where the modified DataFrame will be saved.
        
    Returns:
        None: The function saves the modified DataFrame to a CSV.
    """

    # Function to eliminate consecutive duplicates and return a cleaned string
    def eliminate_consecutive_duplicates(lines):
        if not lines:
            return "[]"
        
        cleaned_lines = [lines[0]]  # Start with the first line
        for line in lines[1:]:
            if line != cleaned_lines[-1]:  # Only add if it's different
                cleaned_lines.append(line)  # Keep as is
        return '[' + ', '.join(map(str, cleaned_lines)) + ']'  # Join back with brackets

    # Create a new DataFrame for filtered results
    filtered_results = []

    # Iterate through the rows of new_results DataFrame
    for index, entry in new_results_df.iterrows():
        actual_lines_str = entry['Actual']

        # Only modify the entry if there are repetitions
        actual_lines = ast.literal_eval(actual_lines_str)  # Directly evaluate only when needed

        # Check for repetitions
        if len(actual_lines) != len(set(actual_lines)) or actual_lines != list(dict.fromkeys(actual_lines)):
            # Eliminate consecutive duplicates
            cleaned_actual_lines_str = eliminate_consecutive_duplicates(actual_lines)

            # Add the modified entry to the filtered results
            filtered_results.append({
                'HumanEval_ID': entry['HumanEval_ID'],
                'Name': entry['Name'],
                'FunctionCall': entry['FunctionCall'],
                'Predicted': entry['Predicted'],
                'Actual': cleaned_actual_lines_str,  # Store the cleaned actual lines
                'Matched': (cleaned_actual_lines_str == entry['Predicted']),
                'Distance': calculate_distance(cleaned_actual_lines_str, entry['Predicted'])  # Use strings for distance
            })
        else:
            # Keep the entry unchanged if no repetitions were found
            filtered_results.append({
                'HumanEval_ID': entry['HumanEval_ID'],
                'Name': entry['Name'],
                'FunctionCall': entry['FunctionCall'],
                'Predicted': entry['Predicted'],
                'Actual': actual_lines_str,  # Original actual lines retained
                'Matched': (actual_lines_str == entry['Predicted']),
                'Distance': calculate_distance(actual_lines_str, entry['Predicted'])  # Use strings for distance
            })

    # Convert the filtered results to a DataFrame
    filtered_results_df = pd.DataFrame(filtered_results)

    # Save the filtered results DataFrame to a new CSV
    filtered_results_df.to_csv(output_csv, index=False)
    print(f"Filtered results CSV with eliminated consecutive duplicates has been created at {output_csv}.")


#df = pd.read_csv("Claude3.5-Sonnet_HumanEval_CoT_fixed.csv")
#eliminate_repetitions_and_compute_distances(df, "Claude3.5-Sonnet_HumanEval_CoT_fixedNoReps.csv")

def clean_and_compute_metrics(df):
    def clean_predicted_list(pred):
        # Strip leading and trailing whitespace
        pred = pred.strip()

        # Normalize multiple whitespaces to a single space between elements
        pred = re.sub(r'\s*,\s*', ', ', pred)  # Ensure correct spacing around commas

        # Check if the list is missing a closing bracket
        added_closing_bracket = False
        if not pred.endswith(']'):
            pred += ']'  # Temporarily add a closing bracket for processing
            added_closing_bracket = True

        # If a bracket was added, remove it before finalizing
        if added_closing_bracket:
            pred = pred[:-1]

        return pred

    # Clean the 'Predicted' column
    df['Predicted'] = df['Predicted'].apply(clean_predicted_list)

    # Recompute the 'Match' column using a simple string comparison
    df['Match'] = df.apply(
        lambda row: row['Actual'] == row['Predicted'],
        axis=1
    )

    # Recompute the 'Distance' column using the string-based distance function
    df['Distance'] = df.apply(
        lambda row: calculate_distance(row['Actual'], row['Predicted']),
        axis=1
    )

    return df

#df = pd.read_csv("Claude3.5-Sonnet_HumanEval_CoT_fixed.csv")

# Apply the function to clean and update the dataframe
#df = clean_and_compute_metrics(df)

# Save the updated dataframe back to the file (overwrite the original)
#df.to_csv('Claude3.5-Sonnet_HumanEval_CoT_fixed_aligned.csv', index=False)

# =============================================================================
# one_shot_generative_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
# In the following, I will ask you to generate the source code of a program written in Python. The program may feature different functions, which may call each other.
# To make the task more accessible, please annotate every line with its index as comments (those begin with a #). The following is very important! *Please note that the function signatures are generally not called,
#  instead you should start with the first line of the function. This does not apply to the function call, of course.* In addition to the function prompt, I will give you an initial input and the called function.
# It is your task to return the called lines, in order, as a list. I will give you an example:
# Source Code : """def simple_loop(x): #1
#                     for i in range(3): #2
#                         print(i+x) #3
#                     return i #4
#               """
# Input: (5)
# Correct solution: [2,3,2,3,2,3,2,4]
# Now I will give you your task.
# Here is the prompt for the source code: Generate a simple bubble sort algorithm.
# Here is the input to the function {df.loc[0, 'Test Case']}
# Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines.                                                                                          
# '''
# 
# one_shot_generative_prompt_java = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
# In the following, I will ask you to generate the source code of a program written in Java. The program may feature different functions, which may call each other.
# To make the task more accessible, please annotate every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
#  instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function prompt, I will give you an initial input and the called function.
# It is your task to return the called lines, in order, as a list. I will give you an example:
# Source Code : """public static void simple_loop(int x): //1
#                     for(int i=0; i<3; i++): //2
#                         System.out.println(c+x) //3
#                     return i //4
#               """
# Input: (5)
# Correct solution: [2,3,2,3,2,3,2,4]
# Now I will give you your task.
# Here is the prompt for the source code: Generate a simple bubble sort algorithm in Java.
# Here is the input to the function [1,2,3]
# Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines.                                                                                          
# '''
# 
# one_shot_generative_prompt_CPP = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
# In the following, I will ask you to generate the source code of a program written in C++. The program may feature different functions, which may call each other.
# To make the task more accessible, please annotate every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
#  instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function prompt, I will give you an initial input and the called function.
# It is your task to return the called lines, in order, as a list. I will give you an example:
# Source Code : """void simple_loop(int x): //1
#                     for(int i=0; i<3; i++): //2
#                         std::cout << (i+x) << //3
#                     return i //4
#               """
# Input: (5)
# Correct solution: [2,3,2,3,2,3,2,4]
# Now I will give you your task.
# Here is the prompt for the source code: Generate a simple bubble sort algorithm in C++.
# Here is the input to the function [1,2,3]
# Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines. 
# '''
# 
# one_shot_prompt_CPP = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
# In the following, I will give you the source code of a program written in C++. The program may feature different functions, which may call each other.
# To make the task more accessible, I have annotated every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
#  instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the source code, I will give you an initial input and the called function.
# It is your task to return the called lines, in order, as a list. I will give you an example:
# Source Code : """void simple_loop(int x): //1
#                     for(int i=0; i<3; i++): //2
#                         std::cout << (i+x) << //3
#                     return i //4
#               """
# Input: (5)
# Correct solution: [2,3,2,3,2,3,2,4]
# Now I will give you your task.
# Here is the source code: .void bubbleSort(int arr[], int n) { //1
#     for (int i = 0; i < n - 1; i++) //2
#         for (int j = 0; j < n - i - 1; j++) //3
#             if (arr[j] > arr[j + 1]) //4
#                 std::swap(arr[j], arr[j + 1]); //5
# } //6
# Here are the inputs to the function arr=[1,2,3], n=3
# Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the lines. 
# '''
# =============================================================================
