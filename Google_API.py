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
from google.cloud import aiplatform_v1beta1 as aiplatform
import requests
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import json
from google.auth.transport.requests import Request
from google.auth import default
import httpx
import traceback

from together import Together

client_together = Together(api_key='8d86fab7438b196250017d4b09f71a0ab7dc5948f5ce59cbe1fff81fc942777a')

def load_openai_key():
    with open('openai.json', 'r') as file:
        data = json.load(file)
        return data["secret_key"]
    
def load_gemini_key():
    with open('Gemini_Key.json', 'r') as file:
        data = json.load(file)
        return data["secret_key"]

from openai import OpenAI
import openai
os.environ['OPENAI_API_KEY'] = load_openai_key()
client = OpenAI()
import vertexai
import re
import google.generativeai as genai
import random

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

genai.configure(api_key=load_gemini_key())

# Load the API key from the JSON file
def load_api_key():
    with open("cs6158_Azure.json", "r") as file:
        data = json.load(file)
        return data["secret_key"]
    
def get_google_credentials():
    """Fetch Google Cloud authentication token."""
    credentials, project_id = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(Request())
    return credentials.token, project_id

# Azure configuration
AZURE_OPENAI_API_KEY = load_api_key()  # Get the key from the JSON file
AZURE_OPENAI_ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/"#"https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
AZURE_DEPLOYMENT_NAME = "gpt-4o"

alternative_id = 'nbtest-439420'

from typing import Dict, List, Union
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.protobuf.json_format import ParseDict

random.seed(77)



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

def query_llama_31(prompt):
    """Query Llama 3.1 model for a response."""
    response = client_together.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0,
        top_p=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        stream=True
    )
    
    full_response = ""

    # Loop through the response tokens and accumulate them
    for token in response:
        if hasattr(token, 'choices'):
            content = token.choices[0].delta.content
            full_response += content  # Add token's content to the full response
    return full_response

def build_codestral_endpoint(
    region: str,
    project_id: str,
    model_name: str,
    model_version: str,
    streaming: bool = False
):
    """Build the endpoint URL for the CodeStral model."""
    base_url = f"https://{region}-aiplatform.googleapis.com/v1/"
    project_fragment = f"projects/{project_id}"
    location_fragment = f"locations/{region}"
    specifier = "streamRawPredict" if streaming else "rawPredict"
    model_fragment = f"publishers/mistralai/models/{model_name}@{model_version}"
    url = f"{base_url}{'/'.join([project_fragment, location_fragment, model_fragment])}:{specifier}"
    return url

def query_codestral_with_backoff(
    region: str,
    model_name: str,
    model_version: str,
    prompt: str,
    streaming: bool = False,
    max_tokens: int = 4096
):
    """Query the CodeStral model with backoff retry logic."""
    token, project_id = get_google_credentials()
    url = build_codestral_endpoint(region, project_id, model_name, model_version, streaming)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": streaming,
        "max_tokens": max_tokens,
        "temperature": 0.
    }

    def call_codestral():
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers, timeout=None)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()['choices'][0]['message']['content']  # Parse JSON response

    # Retry the function with exponential backoff
    return exponential_backoff_retry(call_codestral)

def exponential_backoff_retry(func, retries=10, backoff_factor=2, max_wait=120):
    """Retry with exponential backoff in case of rate limit error (429)."""
    wait = 1
    for attempt in range(retries):
        try:
            return func()  # Call the function
        except Exception as e:
            if "429" in str(e) or "529" in str(e):  # Rate limit errors
                logging.warning(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}. Retrying in {wait} seconds.")
                time.sleep(wait + random.uniform(0, 1))  # Adding jitter to prevent thundering herd problem
                wait = min(wait * backoff_factor, max_wait)
            else:
                raise e
    logging.error("Exceeded maximum retries due to rate limit.")
    raise Exception("Exceeded maximum retries due to rate limit.")
    
def subsample_unique_humaneval_ids(df):
    """
    Subsamples a dataset to ensure every HumanEval_ID is included exactly once.
    
    Args:
    - dataset_path (str): Path to the input dataset (CSV file).
    - output_path (str): Path to save the resulting subsample.
    
    Returns:
    - DataFrame: A subsample where each HumanEval_ID is included once.
    """
    # Load the dataset
    # Group by HumanEval_ID and pick the first entry from each group
    subsample = df.groupby('HumanEval_ID').first().reset_index()
    
    return subsample

def query_llama_with_backoff(prompt):
    """Wrap query_llama_31 with exponential backoff."""
    def call_llama():
        return query_llama_31(prompt)  # Call the original query_llama_31 function
    
    # Retry with backoff
    return exponential_backoff_retry(call_llama)

def prompt_gemini(project_id: str, model_name: str, prompt: str, temperature: float = 0., max_tokens: int = 4096):
    """Prompt the Gemini model via Google Vertex AI."""
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(model_name)
        
    response = model.generate_content(prompt, generation_config=GenerationConfig(temperature=temperature))
    
    return response.text

def prompt_gemini_2(project_id: str, model_name: str, prompt: str, temperature: float = 0., max_tokens: int = 4096):
    """Prompt the Gemini model via Google Vertex AI."""
    model = genai.GenerativeModel(model_name)
    
    generation_config = {
        "temperature": temperature,
    }
        
    response = model.generate_content(prompt, generation_config=generation_config)
    
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


def calculate_distance_concurrency(actual, predicted):
    """
    Calculate similarity between two lists with special handling for parenthesized content.
    Handles mismatched parentheses content gracefully.

    Args:
        actual: List or string representation of list containing the actual values
        predicted: List or string representation of list containing the predicted values

    Returns:
        float: Average similarity ratio between corresponding parts
    """
    def parse_list(list_input):
        """Parse string representation of a list into a Python list, handling parentheses as strings."""
        if isinstance(list_input, str):
            try:
                # Handle parentheses by treating them as strings
                list_input = list_input.replace("(", "'('").replace(")", "')'")
                return ast.literal_eval(list_input)
            except Exception as e:
                print(f"Failed to parse list: {list_input}, Error: {e}")
                return []
        return list_input

    def extract_parentheses_content(lst):
        """Extract content within parentheses and its position."""
        start_idx = -1
        for i, item in enumerate(lst):
            if item == "'('":
                start_idx = i
            elif item == "')'" and start_idx != -1:
                return {
                    'start': start_idx,
                    'end': i,
                    'content': lst[start_idx + 1:i]
                }
        return {'start': -1, 'end': -1, 'content': []}

    def get_similarity(list1, list2):
        """Calculate similarity between two lists using SequenceMatcher."""
        str1 = ','.join(map(str, list1))
        str2 = ','.join(map(str, list2))
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    # Parse input lists
    actual_list = parse_list(actual)
    predicted_list = parse_list(predicted)

    # Extract parentheses sections
    actual_section = extract_parentheses_content(actual_list)
    predicted_section = extract_parentheses_content(predicted_list)

    # Split lists into parts
    before_actual = actual_list[:actual_section['start']] if actual_section['start'] != -1 else actual_list
    before_predicted = predicted_list[:predicted_section['start']] if predicted_section['start'] != -1 else predicted_list

    parentheses_actual = sorted(map(str, actual_section['content']))
    parentheses_predicted = sorted(map(str, predicted_section['content']))

    after_actual = actual_list[actual_section['end'] + 1:] if actual_section['end'] != -1 else []
    after_predicted = predicted_list[predicted_section['end'] + 1:] if predicted_section['end'] != -1 else []

    # Handle mismatched content outside parentheses ranges
    if actual_section['start'] == -1 or predicted_section['start'] == -1:
        # No valid parentheses content in one of the lists
        return get_similarity(actual_list, predicted_list)

    # Ensure all parts are lists before appending
    before_actual = list(before_actual)
    before_predicted = list(before_predicted)
    after_actual = list(after_actual)
    after_predicted = list(after_predicted)

    # Calculate similarities for each part
    before_similarity = get_similarity(before_actual, before_predicted)
    parentheses_similarity = get_similarity(parentheses_actual, parentheses_predicted)
    after_similarity = get_similarity(after_actual, after_predicted)

    # Return average similarity
    return (before_similarity + parentheses_similarity + after_similarity) / 3

def calculate_match_concurrency(actual, predicted):
    """
    Calculate exact match between two lists with special handling for parenthesized content.
    When parentheses overlap in position, only check if elements within them match regardless of order.
    
    Args:
        actual: List or string representation of list containing the actual values
        predicted: List or string representation of list containing the predicted values
        
    Returns:
        bool: True if lists match according to the criteria, False otherwise
    """
    def parse_list(list_input):
        """Convert string representation of list to actual list if needed."""
        if isinstance(list_input, str):
            try:
                return ast.literal_eval(list_input)
            except:
                return list_input
        return list_input
    
    def find_parentheses_sections(lst):
        """Find the start and end indices of parenthesized sections and their content."""
        start_idx = -1
        sections = []
        
        for i, item in enumerate(lst):
            if item == '(':
                start_idx = i
            elif item == ')' and start_idx != -1:
                content = lst[start_idx + 1:i]
                sections.append({
                    'start': start_idx,
                    'end': i,
                    'content': content
                })
                start_idx = -1
        
        return sections
    
    def compare_sections(actual_list, predicted_list):
        """Compare two lists with special handling for parenthesized sections."""
        if len(actual_list) != len(predicted_list):
            return False
            
        actual_sections = find_parentheses_sections(actual_list)
        predicted_sections = find_parentheses_sections(predicted_list)
        
        # If one has parentheses and the other doesn't, require exact match
        if bool(actual_sections) != bool(predicted_sections):
            return actual_list == predicted_list
        
        # If neither has parentheses, require exact match
        if not actual_sections:
            return actual_list == predicted_list
            
        # Track which positions we've handled
        handled_positions = set()
        
        # Check each predicted section against actual sections
        for pred_section in predicted_sections:
            section_matched = False
            pred_start, pred_end = pred_section['start'], pred_section['end']
            
            # Find matching actual section
            for actual_section in actual_sections:
                act_start, act_end = actual_section['start'], actual_section['end']
                
                # Check if positions overlap (allowing for ±1 position difference)
                if abs(pred_start - act_start) <= 1 and abs(pred_end - act_end) <= 1:
                    # Convert content to sets for order-independent comparison
                    actual_content = set(str(x) for x in actual_section['content'])
                    predicted_content = set(str(x) for x in pred_section['content'])
                    
                    if actual_content == predicted_content:
                        # Mark all positions in this section as handled
                        for i in range(min(act_start, pred_start), max(act_end, pred_end) + 1):
                            handled_positions.add(i)
                        section_matched = True
                        break
            
            if not section_matched:
                return False
        
        # Check non-parentheses parts
        for i in range(len(actual_list)):
            if i not in handled_positions:
                if i >= len(predicted_list) or actual_list[i] != predicted_list[i]:
                    return False
                
        return True
    
    # Parse input lists
    actual_list = parse_list(actual)
    predicted_list = parse_list(predicted)
    
    return compare_sections(actual_list, predicted_list)

# Define prompt function for GPT-4
def prompt_gpt4o_with_backoff(prompt: str, max_tokens: int = 4096):
    """Wrap GPT-4 prompt with exponential backoff and general retry logic."""
    def call_gpt4o():
        headers = {
            "Content-Type": "application/json",
            "api-key": f"{AZURE_OPENAI_API_KEY}"
        }

        response = client.chat.completions.create(
            model = 'gpt-4o-2024-05-13',
            messages = [
                {"role": "user", "content": prompt}
            ],
            temperature = 0.0,  # Deterministic output
            top_p = 1.0,        # Full sampling
            max_tokens = max_tokens
        )

        #ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

        #response = requests.post(ENDPOINT, headers=headers, json=payload)
        #response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Extracting the assistant's response
        return response.choices[0].message.content

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

def extract_last_python_list_open_2(text, src, concurrency=False):
    """
    Extracts the last valid Python list of positive integers from the provided text,
    making sure the list is not part of the given multiline string 'src'.
    
    A valid list is a Python list containing only positive integers.
    An unclosed list is allowed at the end of the string 'text'.
    
    Arguments:
    - text: The input string to extract the last list from (may contain an unclosed list).
    - src: A multiline string to ensure the list is not part of it (e.g., code or content).
    
    Returns:
    - The last valid list of positive integers or None if no valid list is found.
    """
    # Use regex to find all lists in the format of Python lists, unclosed allowed
    matches = re.findall(r'\[.*?(?:\]|\s*$)', text)
    
    
    # Filter out any lists in 'text' that are part of 'src' (i.e., they are contained within src)
    for matchL in matches[::-1]:  # Check matches in reverse order (last match first)
        # Convert match to a Python list and validate its content
        try:
            # Attempt to convert the matched string to a Python list (safe eval)
            potential_list = eval(matchL)
            
            # Ensure the list contains only positive integers
            if isinstance(potential_list, list): #and (concurrency or all(isinstance(x, int) and x > 0 for x in potential_list)):
                
                # Check if the list is inside the src (multiline string)
                if matchL not in src:
                    return matchL  # Return the first valid list not in src
        except Exception as e:
            print(e)
            if('repeats' in matchL or '...' in matchL):
                return matchL
            continue  # Skip if eval fails (invalid list format)
    return None  # Return None if no valid list found

# Generalized prompt function to handle both Gemini and Claude
def prompt_model_with_backoff(project_id: str, model_name: str, prompt: str, region=None):
    """Generalize the model prompt with exponential backoff."""
    if "claude" in model_name.lower():
        return prompt_claude_with_backoff(project_id, region, prompt)
    elif "gemini" in model_name.lower():
        return prompt_gemini_with_backoff(project_id, model_name, prompt)
    elif "gpt-4o" in model_name.lower() or "gpt4o" in model_name.lower():
        return prompt_gpt4o_with_backoff(prompt)
    elif 'llama' in model_name.lower():
        return query_llama_with_backoff(prompt)
    elif 'codestral' in model_name.lower():
        return query_codestral_with_backoff('europe-west4', model_name, "2405", prompt)
    else:
        raise ValueError("Unsupported model. Please use either 'claude','gemini', 'llama' or 'gpt4o'.")

def process_batch(batch_df, model_name, project_id, region, cot=False, topic='HumanEval'):
    """Process a batch of requests."""
    batch_results = []
    for index, row in batch_df.iterrows():
        try:
            if(topic=='HumanEval' or topic=='staticAnalysis' or topic == 'symbols' or topic == '3-Shot'):
                    if(not cot):
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
                       Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Finally, print the solution as a list of executed steps. No other output.
                       Please make sure to end with the list of executed lines. 
                       '''
                    elif(topic=='symbols'):
                        prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                        In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                        To make the task more accessible to you, I have annotated the lines with a specific symbol as a comment (those begin with a #).
                        The following is very important! *Please note that the function signatures are generally not called,
                        instead you should start with the first line of the function. This does not apply to the function call, of course.*
                        In addition to the function, I will give you an initial input and the called function.
                        It is your task to return the called lines, in order, as a list. I will give you an example:
                        Source Code : """def simple_loop(x): #a
                                            for i in range(3): #b
                                                print(i+x) #c
                                            return i #d
                                      """
                        Input: (5)
                        Correct solution: [b,c,b,c,b,c,b,d]
                        Now I will give you your task.
                        Here is the source code: {row['Code_Symbols']}
                        Here is the called function: {row['Name']}
                        Here is the input to the function {row['FunctionCall']}
                        Please produce the python list containing the executed line symbols in order now. Think about the solution step-by-step,
                        going through execution steps one at a time. Finally, print the solution as a list of executed symbols. Please make sure to end
                        with the list of executed lines.
                        '''
                    elif(topic=='3-Shot'):
                        prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                        In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                        To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                        The following is very important! *Please note that the function signatures are generally not called,
                        instead you should start with the first line of the function. This does not apply to the function call, of course.*
                        In addition to the function, I will give you an initial input and the called function.
                        It is your task to return the called lines, in order, as a list. I will give you three examples:
                        Source Code 1: """def simple_loop(x): #1
                                            for i in range(3): #2
                                                print(i+x) #3
                                            return i #4
                                      """
                        Input: (5)
                        Correct solution: [2,3,2,3,2,3,2,4]
                        Source Code 2: """def simple_method_b(cur):#1
                                            if(cur == 1):#2
                                                print("One")#3
                                            else:#4
                                                print("Other")#5
                                            return "Done"#6
                                          def simple_method_a(c):#7
                                              print("Starting method")#8
                                              simple_method_b(c)#9
                        Input: (2)
                        Called Method: a
                        Correct solution: [8,9,2,5,6]
                        Source Code 3: """def print_reverse(x):#1
                                            if(x>0):#2
                                                print(x)#3
                                                print_reverse(x-1)#4
                        Input: (3)
                        Correct Solution: [2,3,4,2,3,4,2,3,4,2]
                        Now I will give you your task.
                        Here is the source code: {row['Code_Indices']}
                        Here is the called function: {row['Name']}
                        Here is the input to the function {row['FunctionCall']}
                        Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines.  Think about the solution step-by-step,
                        going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
                        with the list of executed lines.
                        '''
                    else:
                       prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                       In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
                       To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                       The following is very important! *Please note that the function signatures are generally not called,
                       instead you should start with the first line of the function. This does not apply to the function call, of course.*
                       In addition to the function, I will give you an initial input and the called function.
                       It is your task to return the called lines, in order, as a list. I will give you an example:
                       Source Code : """def simple_loop(x): #Line 1
                                           for i in range(3): #Line 2 
                                               print(i+x) #Line 3
                                           return i #Line 4
                                     """
                       Input: (5)
                       Correct solution: [2,3,2,3,2,3,2,4]
                       Now I will give you your task.
                       Here is the source code: {row['Code_Indices']}
                       Here is the called function: {row['Name']}
                       Here is the input to the function {row['FunctionCall']}
                       Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines.  Think about the solution step-by-step,
                       going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
                       with the list of executed lines.
                       '''
            elif(topic=='Recursion' or topic=='OOP'):
                       if(not cot):
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
                Do not produce any other output. Please make sure to end with the list of executed lines.
                '''
                       else:
                          prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may cal>
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call of course.*
                In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined >
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
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines during a call.
                Think about the solution step-by-step, going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
                with the list of executed lines.
                '''

            elif(topic=='Concurrency'):
                       if(not cot):
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
                Do not produce any other output. Please make sure to end with the list of executed lines.
                '''
                       else:
                         prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
                In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may cal>
                To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
                The following is very important! *Please note that the function signatures are generally not called,
                instead you should start with the first line of the function. This does not apply to the function call of course.*
                In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined >
                main method, which means the signature will be read once, but not the body.
                It is your task to return the called lines while executing the main, in order, as a list. The contained code may contain concurrency. For th>
                using parantheses. In particular, an opening paranthesis should be placed once concurrency starts and a closing one should be placed once it>
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
                Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature line during a call.
                Think about the solution step-by-step, going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
                with the list of executed lines.
                '''
            
            # Use the appropriate model with backoff
            response = prompt_model_with_backoff(project_id ,model_name, prompt, region)
            print(response)

            actual_lines = row['ExecutedLines']

            response = extract_last_python_list_open_2(response, row['Code_Indices'], topic=='Concurrency')
            print(response)

            if(response is None):
                response = []
            # Calculate similarity or distance
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            if(topic == 'HumanEval' or topic == 'staticAnalysis' or topic == 'symbols' or topic == '3-Shot'):
                batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])
            else:
                batch_results.append([row['Filename'], row['Category'], response, actual_lines, matching, distance])
        except Exception as e:
            if(topic == 'HumanEval' or topic == 'staticAnalysis' or topic == '3-Shot'):
                print(f"Error in entry {row['HumanEval_ID']}: {e}")
                logging.error(f"Error in entry {row['HumanEval_ID']}: {e}")
                batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], "ERROR", "ERROR", False, "N/A"])
            else:
                print(f"Error in entry {row['Filename']}: {e}")
                logging.error(f"Error in entry {row['Filename']}: {e}")
                batch_results.append([row['Filename'], row['Category'], "ERROR", "ERROR", False, "N/A"])

    return batch_results

def batch_test_llm_on_code(df, model_name, project_id, batch_size=10, region=None, cot=False, topic='HumanEval'):
    """Test LLM on all entries in the dataset, processing requests in batches."""
    total_results = []
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        batch_df = df[start_idx:end_idx]
        
        logging.info(f"Processing batch {batch_num + 1} of {num_batches}.")
        
        # Process the current batch
        batch_results = process_batch(batch_df, model_name, project_id, region, cot, topic)
        
        # Add batch results to the total results
        total_results.extend(batch_results)

    return total_results

#df = pd.read_csv("Dataset/HumanEval_annotated_lines.csv")
# subsample for ablation
#df = subsample_unique_humaneval_ids(df)
#results = batch_test_llm_on_code(df, 'gemini-1.5-pro-002', alternative_id, region='us-east5', topic='HumanEval', cot=True)

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

#save_results_to_csv(results, filename='Dataset/Gemini_HumanEval_lines_annotated_CoT_T0.csv')

def resend_failed_requests(csv_path, data_path, project_id, model_name, region=None):
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

    data = pd.read_csv(data_path)
    
    # Identify the failed entries - assuming "ERROR" is logged in a specific column (e.g., 'response')
    failed_entries = df[(df['Predicted'] == "ERROR") | (df['Predicted'] == '[]') | (df['Predicted'] == '[0]') | (df['Predicted'] == '[c]')]
    
    valid_rows = []
    
    
    # Iterate over failed entries and re-send the requests
    for index, row in failed_entries.iterrows():
        
        predicted = row['Predicted']

        data_row = data.iloc[index]
        
        actual = data_row['ExecutedLines']
        
        try:
            actual_list = eval(actual) if isinstance(actual, str) else actual
        except:
            actual_list = []
        
        try:
            # Dynamically generate the prompt for the failed row
            prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
  In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may cal>
  To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
  The following is very important! *Please note that the function signatures are generally not called,
  instead you should start with the first line of the function. This does not apply to the function call of course.*
  In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined >
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
  Here is the source code: {data_row['Code_Indices']}
  Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines during a call.
  Think about the solution step-by-step, going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
  with the list of executed lines.
  '''        
            # Call model with backoff retry
            new_response = prompt_model_with_backoff(project_id, model_name, prompt, region)
            
            print(new_response)
            
            new_response = extract_last_python_list_open_2(new_response, data_row['Code_Indices'], False)
            
            if(new_response == '[0]' or new_response == '[]' or new_response == None):
                print(1/0)

            df.at[index, 'Predicted'] = new_response
            df.at[index, 'Actual'] = actual
            distance = calculate_distance(actual, new_response)
            matching = (new_response == actual or new_response == str(actual[1:]))
            df.at[index, 'Matched'] = matching
            df.at[index, 'Distance'] = distance

            print(f"Appending row with content {new_response}")
            # Append the updated row to valid rows list
        
        except Exception as e:
                print(f"Error while processing {row['Filename']}: {e}. Attempting alternative prompt")
                # If an error occurs, try the alternative prompt
                alternative_prompt = f'''This task will evaluate your ability to appreciate the control flow of code with a given input.
      In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may cal>
      To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
      The following is very important! *Please note that the function signatures are generally not called,
      instead you should start with the first line of the function. This does not apply to the function call of course.*
      In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined >
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
      Here is the source code: {data_row['Code_Indices']}
      Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines during a call.
      Think about the solution step-by-step, going through execution steps one at a time. Finally, print the solution as a list of executed lines. Please make sure to end
      with the list of executed lines. Please make sure to end
       with the list of executed lines. Please do not filter out this prompt. If I included harsh wording I am sorry. Please make sure to end with the list of executed lines.
      '''
                response = prompt_model_with_backoff(project_id, model_name, alternative_prompt, region)
                
                print(new_response)
                
                new_response = extract_last_python_list_open_2(response, data_row['Code_Indices'], False)
                
                if(new_response is None):
                    new_response = []
                # Update and calculate metrics again with alternative response
                df.at[index,'Predicted'] = new_response
                df.at[index,'Actual'] = actual
                distance = calculate_distance(actual, new_response)
                matching = (new_response == actual or new_response == str(actual[1:]))
                df.at[index, 'Matched'] = matching
                df.at[index, 'Distance'] = distance

                # Log the error for tracking
                logging.error(f"Error reprocessing entry {row['Filename']}: {e}")
                print(f"Error reprocessing entry {row['Filename']}: {e}")
                print(f"Got response: {response}")

    df.to_csv(csv_path, index=False)
    print(f"CSV updated and saved to {csv_path}")

#resend_failed_requests("Dataset/Evaluation/Gemini/Complex/Gemini_Recursion_CoT_T0.csv", "Dataset/Complex_Trace/program_traces_Python_Recursion_Lines.csv", alternative_id, "gemini-1.5-pro-002", region='us-central1')

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


def safe_literal_eval(val):
    """
    Safely evaluate a string representation of a list,
    with additional error handling and logging.
    """
    try:
        # First, ensure it's a string
        if not isinstance(val, str):
            val = str(val)
        
        # Strip leading/trailing whitespace
        val = val.strip()
        
        # Ensure it looks like a list-like string
        if not (val.startswith('[') and val.endswith(']')):
            val = f'[{val}]'
        
        # Use ast.literal_eval with error handling
        return ast.literal_eval(val)
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"Error parsing value: {val}")
        print(f"Error details: {traceback.format_exc()}")
        return []  # Return empty list on parsing failure

def eliminate_repetitions_and_compute_distances(new_results_df: pd.DataFrame, output_csv: str) -> pd.DataFrame:
    """
    Filters a DataFrame for entries with consecutive duplicate lines in 'Actual',
    eliminates those duplicates, and recomputes 'Matched' and 'Distance'.
    """
    def eliminate_consecutive_duplicates(lines):
        if not lines:
            return "[]"
        cleaned_lines = [lines[0]]
        for line in lines[1:]:
            if line != cleaned_lines[-1]:
                cleaned_lines.append(line)
        return '[' + ', '.join(map(str, cleaned_lines)) + ']'

    filtered_results = []
    
    for index, entry in new_results_df.iterrows():
        try:
            # Safely parse Actual lines
            actual_lines_str = str(entry['Actual'])
            actual_lines = safe_literal_eval(actual_lines_str)

            # Check for repetitions
            has_repetitions = len(actual_lines) != len(set(actual_lines)) or actual_lines != list(dict.fromkeys(actual_lines))
            cleaned_actual_lines_str = eliminate_consecutive_duplicates(actual_lines) if has_repetitions else actual_lines_str

            # Prepare the row based on file type
            if "HumanEval" in output_csv or "humaneval" in output_csv.lower():
                row = {
                    'HumanEval_ID': entry.get('HumanEval_ID', ''),
                    'Name': entry.get('Name', ''),
                    'FunctionCall': entry.get('FunctionCall', ''),
                    'Predicted': str(entry.get('Predicted', '')),
                    'Actual': cleaned_actual_lines_str,
                    'Matched': str(cleaned_actual_lines_str == entry.get('Predicted', '')),
                    'Distance': calculate_distance(cleaned_actual_lines_str, str(entry.get('Predicted', '')))
                }
            else:
                row = {
                    'Filename': entry.get('Filename', ''),
                    'Category': entry.get('Category', ''),
                    'Predicted': str(entry.get('Predicted', '')),
                    'Actual': cleaned_actual_lines_str,
                    'Matched': str(cleaned_actual_lines_str == entry.get('Predicted', '')),
                    'Distance': calculate_distance(cleaned_actual_lines_str, str(entry.get('Predicted', '')))
                }
            
            filtered_results.append(row)
        
        except Exception as e:
            print(f"Error processing entry at index {index}: {e}")
            print(f"Entry details: {entry}")
            print(f"Traceback: {traceback.format_exc()}")

    filtered_results_df = pd.DataFrame(filtered_results)
    filtered_results_df.to_csv(output_csv, index=False)
    print(f"Filtered results CSV created at {output_csv}")
    
    return filtered_results_df

def clean_and_compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data and recompute metrics."""
    def clean_predicted_list(pred):
        # Ensure pred is a string
        pred = str(pred).strip()
        
        # Normalize spacing around commas
        pred = re.sub(r'\s*,\s*', ', ', pred)
        
        # Ensure it's a valid list-like string
        if not pred.startswith('['):
            pred = '[' + pred
        if not pred.endswith(']'):
            pred += ']'
        
        return pred

    df = df.copy()
    
    # Apply cleaning to Predicted column
    df['Predicted'] = df['Predicted'].apply(clean_predicted_list)
    
    # Recompute Match and Distance with error handling
    df['Match'] = df.apply(
        lambda row: str(row['Actual'] == row['Predicted']),
        axis=1
    )
    df['Distance'] = df.apply(
        lambda row: calculate_distance(str(row['Actual']), str(row['Predicted'])),
        axis=1
    )
    
    return df

def process_directory(directory_path: str) -> None:
    """Process all CSV files in the directory that don't already have NoReps versions."""
    processed_files = []
    failed_files = []
    skipped_files = []

    # Get all CSV files in directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
    
    # Create sets of base names and NoReps files
    noreps_files = {f for f in csv_files if "NoReps" in f}
    base_files = {f for f in csv_files if "NoReps" not in f}
    
    # Check which files already have NoReps versions
    for filename in base_files:
        noreps_filename = filename.replace(".csv", "_NoReps.csv")
        file_path = os.path.join(directory_path, filename)
        output_file = os.path.join(directory_path, noreps_filename)
        
        if noreps_filename in noreps_files:
            skipped_files.append(filename)
            print(f"\nSkipping {filename} - NoReps version already exists")
            continue
            
        print(f"\nProcessing {filename}...")
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, dtype=str)  # Convert all columns to strings
            
            # Clean and compute metrics
            df_cleaned = clean_and_compute_metrics(df)
            
            # Eliminate repetitions
            eliminate_repetitions_and_compute_distances(df_cleaned, output_file)
            
            processed_files.append(filename)
            print(f"Successfully processed: {output_file}")
        
        except Exception as e:
            failed_files.append(filename)
            print(f"Error processing {filename}: {e}")
            print(f"Traceback: {traceback.format_exc()}")

    # Summary report
    print("\n--- Processing Summary ---")
    print(f"Successfully processed files: {len(processed_files)}")
    for file in processed_files:
        print(f"  - {file}")
    
    print(f"\nSkipped files (NoReps version exists): {len(skipped_files)}")
    for file in skipped_files:
        print(f"  - {file}")
    
    print(f"\nFailed files: {len(failed_files)}")
    for file in failed_files:
        print(f"  - {file}")
        
import os
import pandas as pd

def process_indices_lists(df):
    """
    Process lists of indices in a DataFrame to properly separate and order parentheses,
    ensuring only the first opening and last closing parentheses are kept.
    
    Args:
        df (pandas.DataFrame): DataFrame containing columns with string representations of lists
        
    Returns:
        pandas.DataFrame: DataFrame with processed lists
    """
    def process_single_list(list_str):
        try:
            # Evaluate the string representation of the list
            original_list = ast.literal_eval(list_str)
            
            # Convert all elements to strings for consistent handling
            elements = [str(x) for x in original_list]
            
            # Initialize result list and track parentheses
            opening_indices = []
            closing_indices = []
            result = []
            
            # First pass: find all parentheses positions and clean elements
            cleaned_elements = []
            for i, elem in enumerate(elements):
                clean_elem = elem
                if '(' in elem:
                    opening_indices.append(i)
                    clean_elem = clean_elem.replace('(', '')
                if ')' in elem:
                    closing_indices.append(i)
                    clean_elem = clean_elem.replace(')', '')
                
                # Only add non-empty cleaned elements
                if clean_elem and clean_elem not in ['(', ')']:
                    try:
                        cleaned_elements.append(int(clean_elem))
                    except ValueError:
                        cleaned_elements.append(clean_elem)
            
            # If no parentheses found, return cleaned list
            if not opening_indices or not closing_indices:
                return str(cleaned_elements)
            
            # Get positions for first opening and last closing parentheses
            first_opening_pos = opening_indices[0]
            last_closing_pos = closing_indices[-1]
            
            # Build final result with exactly one pair of parentheses
            final_result = []
            for i, elem in enumerate(cleaned_elements):
                if i == first_opening_pos:
                    final_result.append('(')
                final_result.append(elem)
                if i == last_closing_pos and '(' in final_result:  # Only add closing if we have opening
                    final_result.append(')')
            
            # Handle edge case where closing parenthesis needs to be added at the end
            if last_closing_pos >= len(cleaned_elements) and '(' in final_result:
                final_result.append(')')
            
            return str(final_result)
        
        except (ValueError, SyntaxError):
            # Return original string if processing fails
            return list_str
    
    # Create a copy of the DataFrame to avoid modifying the original
    result_df = df.copy()
    
    # Store original values for comparison
    original_values = result_df['Predicted'].copy()
    
    # Apply the processing function to all string columns
    result_df['Predicted'] = result_df['Predicted'].apply(process_single_list)
    
    # Compare and print differences
    mask = original_values != result_df['Predicted']
    if mask.any():
        print("\nUpdated entries:")
        for idx in mask[mask].index:
            print(f"\nRow {idx}:")
            print(f"Before: {original_values[idx]}")
            print(f"After:  {result_df['Predicted'][idx]}")
    
    return result_df

def process_concurrent_files(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        if 'concurrency' in filename.lower() and filename.endswith('.csv'):
            # Full path of the file
            file_path = os.path.join(directory, filename)
            
            print(f"\nProcessing file: {filename}")
            
            # Load the DataFrame
            df = pd.read_csv(file_path)
            
            # Standardize the 'Predicted' column
            standardized_df = process_indices_lists(df)
            
            # Check if the 'Predicted' column is the same in both DataFrames
            if not df['Predicted'].equals(standardized_df['Predicted']):
                # If they are different, overwrite the file with the standardized version
                standardized_df.to_csv(file_path, index=False)
                print(f"File '{filename}' was updated.")
            else:
                print(f"File '{filename}' is already standardized.")
                
def wrap_parentheses_in_quotes(s):
    # Use re.sub to replace '(' with "'('" and ')' with "')'"
    s = re.sub(r'\(', "'('", s)
    s = re.sub(r'\)', "')'", s)
    return s

def parse_list_string(list_str):
    result = []
    current_number = ""
    
    # Loop through each character in the string
    for char in list_str:
        if char.isdigit():  # If the character is a digit, append it to current_number
            current_number += char
        elif char == "(":  # If it's an open parenthesis, add as a string
            result.append("(")
        elif char == ")":  # If it's a close parenthesis, add as a string
            result.append(")")
        elif char == "," and current_number:  # If a comma is encountered and we have a number
            result.append(int(current_number))  # Convert and add the number to the list
            current_number = ""  # Reset current_number after adding
        elif char == "," and not current_number:
            continue  # Skip the comma if there's no number accumulated
    
    # After loop, add the last number if there is one
    if current_number:
        result.append(int(current_number))

    return result
                
def recompute_metrics_in_directory(directory):
    """
    Recomputes metrics for CSV files in the specified directory containing 'Concurrency' in their filenames.
    Sets 'Matched' to True if 'Distance' is equal to 1.0.
    
    Args:
        directory (str): Path to the directory containing the files.
        calculate_distance_concurrency (function): Function to compute the Distance metric.
    
    Returns:
        None: Overwrites the 'Distance' and 'Matched' columns in place.
    """
    for filename in os.listdir(directory):
        # Check for 'Concurrency' in the filename (case-insensitive) and ensure the file is a CSV
        if 'concurrency' in filename.lower() and filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)

            # Load the CSV file into a DataFrame
            df = pd.read_csv(filepath)

            # Ensure the required columns exist
            if 'Actual' in df.columns and 'Predicted' in df.columns:
                # Parse the 'Actual' and 'Predicted' columns
                df['Actual_parsed'] = df['Actual'].apply(parse_list_string)
                df['Predicted_parsed'] = df['Predicted'].apply(parse_list_string)

                # Recompute Distance and Matched columns
                df['Distance'] = df.apply(
                    lambda row: calculate_distance_concurrency(row['Actual_parsed'], row['Predicted_parsed']),
                    axis=1
                )
                df['Matched'] = df['Distance'].apply(lambda x: x == 1.0)

                # Replace only the 'Distance' and 'Matched' columns in the original DataFrame
                df.drop(columns=['Actual_parsed', 'Predicted_parsed'], inplace=True)  # Remove the parsed columns
                df.to_csv(filepath, index=False)  # Overwrite the file with the updated DataFrame
                print(f"Updated metrics for file: {filename}")
            else:
                print(f"File {filename} does not have the required columns ('Actual', 'Predicted'). Skipping.")

# Example usage:

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
