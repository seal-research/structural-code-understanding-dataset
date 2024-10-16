import os
import logging
import pandas as pd
from google.oauth2 import service_account
import google.cloud.aiplatform
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Image
from anthropic import AnthropicVertex
from transformers import pipeline
import vertexai
import json

# Set up logging
logging.basicConfig(
    filename='model_queries.log',  # Log file name
    level=logging.INFO,             # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Read the CSV file using pandas
#df = pd.read_csv('Dataset/sorting_algorithm_trace_results.csv')
df = pd.read_csv('Dataset/HumanEval_trace_results.csv')

# Path to your service account key file
key_path = "cs6158-structuralunderstanding-2647462afe3e.json"

# Create credentials using the service account key
credentials = service_account.Credentials.from_service_account_file(key_path)

# Initialize Google Cloud AI Platform
google.cloud.aiplatform.init(project="CS6158-StructuralUnderstanding", location="us-central1", credentials=credentials)

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

def prompt_gemini(project_id: str, model_name: str, prompt: str, temperature: float = 0., max_tokens: int = 2048):
    """Prompt the Gemini model via Google Vertex AI."""
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(model_name)
        
    response = model.generate_content(prompt)
    
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

# Prompts for testing
one_shot_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #). The following is very important! *Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call, of course.* In addition to the function, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """def simple_loop(x): #1
                    for i in range(3): #2
                        print(c+x) #3
                    return i #4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the source code: {df.loc[7, 'Code_Indices']}
Here is the called function: {df.loc[7, 'Name']}
Here is the input to the function {df.loc[7, 'FunctionCall']}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output.                                                                                          
'''

# Example usage of the functions (uncomment to run)
# claude_response = prompt_claude("cs6158-structuralunderstanding", "us-east5", one_shot_prompt)
# response = prompt_gemini("cs6158-structuralunderstanding", "gemini-1.5-pro-002", one_shot_prompt)
# huggingface_response = prompt_huggingface("gpt2", one_shot_prompt_CPP)

# print("Claude Response:", claude_response)
# print("Gemini Response:", gemini_response)
# print("Huggingface Response:", huggingface_response)

# Make the prediction
#reply = predict_large_language_model_sample("cs6158-structuralunderstanding", "text-bison@002", 0.1, 2048, 0.8, 40, one_shot_prompt_CPP, "us-central1")

#client = AnthropicVertex(region="us-east5", project_id="cs6158-structuralunderstanding")

#message = client.messages.create(
#    max_tokens=1024,
#    messages=[
#      {
#        "role": "user",
#        "content": one_shot_prompt_CPP,
#      }
#    ],
#    model="claude-3-5-sonnet@20240620",
#)

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

def calculate_distance(actual, predicted):
    """Calculate similarity between two lists of lines."""
    actual_str = ','.join(map(str, actual))
    predicted_str = ','.join(map(str, predicted))
    sequence = difflib.SequenceMatcher(a=actual_str, b=predicted_str)
    return sequence.ratio()  # Similarity ratio

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
def prompt_claude_with_backoff(project_id: str, region: str, prompt: str, max_tokens: int = 1024):
    """Wrap Claude prompt with exponential backoff."""
    def call_claude():
        client = AnthropicVertex(region=region, project_id=project_id)
        message = client.messages.create(
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            model="claude-3-5-sonnet@20240620",  # Specify Claude model version
        )
        reply = message.model_dump_json(indent=2)
        return fix_predicted_lines(json.loads(reply)['content'][0]['text'])

    return exponential_backoff_retry(call_claude)

# Generalized prompt function to handle both Gemini and Claude
def prompt_model_with_backoff(project_id: str, model_name: str, prompt: str, region=None):
    """Generalize the model prompt with exponential backoff."""
    if "claude" in model_name.lower():
        return prompt_claude_with_backoff(project_id, region, prompt)
    elif "gemini" in model_name.lower():
        return prompt_gemini_with_backoff(project_id, model_name, prompt)
    else:
        raise ValueError("Unsupported model. Please use either 'claude' or 'gemini'.")

def process_batch(batch_df, model_name, project_id, region):
    """Process a batch of requests."""
    batch_results = []
    for index, row in batch_df.iterrows():
        try:
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
                                    print(c+x) #3
                                return i #4
                          """
            Input: (5)
            Correct solution: [2,3,2,3,2,3,2,4]
            Now I will give you your task.
            Here is the source code: {row['Code_Indices']}
            Here is the called function: {row['Name']}
            Here is the input to the function {row['FunctionCall']}
            Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output.
            '''
            
            
            # Use the appropriate model with backoff
            response = prompt_model_with_backoff(project_id ,model_name, prompt, region)

            actual_lines = row['ExecutedLines']

            # Calculate similarity or distance
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])

        except Exception as e:
            print(f"Error in entry {row['HumanEval_ID']}: {e}")
            logging.error(f"Error in entry {row['HumanEval_ID']}: {e}")
            batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], "ERROR", "ERROR", False, "N/A"])

    return batch_results

def batch_test_llm_on_code(df, model_name, project_id, batch_size=10, region=None):
    """Test LLM on all entries in the dataset, processing requests in batches."""
    total_results = []
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        batch_df = df[start_idx:end_idx]
        
        logging.info(f"Processing batch {batch_num + 1} of {num_batches}.")
        
        # Process the current batch
        batch_results = process_batch(batch_df, model_name, project_id, region)
        
        # Add batch results to the total results
        total_results.extend(batch_results)

    return total_results

# Save results to CSV
def save_results_to_csv(results, filename="Model_HumanEval.csv"):
    """Save the results to a CSV file."""
    results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Example usage with generalized prompt
#model_name = "claude-3-5-sonnet@20240620"  # or use "gemini-1.5-pro-002"
#region = "us-east5"  # Required for Claude
#results = batch_test_llm_on_code(df, model_name, project_id = 'cs6158-structuralunderstanding', batch_size=16, region=region)
#save_results_to_csv(results, "Claude_HumanEval.csv")

def fix_predicted_lines(predicted_str):
    """Fix the predicted lines format to include spaces after commas."""
    return predicted_str.replace(',', ', ')

# Load the existing results from the CSV
results_df = pd.read_csv("Claude_HumanEval_fixed.csv")

# Check for errors in the DataFrame and update with new predictions from Claude
project_id = "cs6158-structuralunderstanding"
region = "us-east5"

# Iterate through the DataFrame to find and fix the specific predicted lines
for index, row in results_df.iterrows():
    if row['Predicted'] == "[16,17,18,19,17,18,19,17,18,19,17,20]":
        # Fix the predicted lines format by adding spaces after commas
        fixed_lines = row['Predicted'].replace(",", ", ")
        
        # Assuming 'Actual' contains the expected lines as a string
        actual_lines = row['Actual']

        # Update the predicted column
        results_df.at[index, 'Predicted'] = fixed_lines
        
        # Recompute match and distance
        match = (fixed_lines == actual_lines)
        distance = calculate_distance(actual_lines, fixed_lines)

        # Update the 'Matched' and 'Distance' columns
        results_df.at[index, 'Matched'] = match
        results_df.at[index, 'Distance'] = distance

# Save the corrected results back to CSV
results_df.to_csv("Claude_HumanEval_fixed_2.csv", index=False)
print("Predicted lines fixed and saved to Claude_HumanEval_fixed.csv")






# =============================================================================
# one_shot_generative_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
# In the following, I will ask you to generate the source code of a program written in Python. The program may feature different functions, which may call each other.
# To make the task more accessible, please annotate every line with its index as comments (those begin with a #). The following is very important! *Please note that the function signatures are generally not called,
#  instead you should start with the first line of the function. This does not apply to the function call, of course.* In addition to the function prompt, I will give you an initial input and the called function.
# It is your task to return the called lines, in order, as a list. I will give you an example:
# Source Code : """def simple_loop(x): #1
#                     for i in range(3): #2
#                         print(c+x) #3
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
