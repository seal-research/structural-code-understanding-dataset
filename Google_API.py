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

def prompt_gemini(project_id: str, model_name: str, prompt: str, temperature: float = 0.7, max_tokens: int = 2048, top_p: float = 0.9, top_k: int = 40, tuned_model_name: str = ""):
    """Prompt the Gemini model via Google Vertex AI."""
    vertexai.init(project=project_id, location="us-central1")
    model = TextGenerationModel.from_pretrained(model_name)
    
    if tuned_model_name:
        model = model.get_tuned_model(tuned_model_name)
        
    response = model.predict(
        prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_k=top_k,
        top_p=top_p,
    )
    
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

# Example usage of the functions (uncomment to run)
claude_response = prompt_claude("cs6158-structuralunderstanding", "us-east5", one_shot_prompt)
# gemini_response = prompt_gemini("cs6158-structuralunderstanding", "text-bison@002", one_shot_prompt_CPP)
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
  
reply_dict = json.loads(claude_response)

# Extract the text content
reply = reply_dict['content'][0]['text']

# Check if the output matches the expected value
expected_value = str(df.loc[7, 'ExecutedLines'])
matching = (reply == expected_value or reply == expected_value[1:])

# Log the details
logging.info(
    "Model: %s, Algorithm: %s, Input: %s, Output: %s, Matched: %s",
    "CLAUDE-3,5",
    df.loc[0, 'Name'],
    df.loc[0, 'FunctionCall'],
    reply,
    matching
)

print(matching)
