import os
import google.cloud.aiplatform
from google.oauth2 import service_account
import pandas as pd
import logging

from vertexai.preview.generative_models import GenerativeModel, Image

# Set up logging
logging.basicConfig(
    filename='model_queries.log',  # Log file name
    level=logging.INFO,             # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Read the CSV file using pandas
df = pd.read_csv('Dataset/sorting_algorithm_trace_results.csv')

# Path to your service account key file
key_path = "cs6158-structuralunderstanding-2647462afe3e.json"

# Create credentials using the service account key
credentials = service_account.Credentials.from_service_account_file(key_path)

google.cloud.aiplatform.init(project="CS6158-StructuralUnderstanding", location="us-central1", credentials=credentials)

import vertexai
from vertexai.preview.language_models import TextGenerationModel

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
) :
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

zero_shot_prompt = f''' This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #). The following is very important !*Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """def simple_loop(x): #1
                    for i in range(3): #2
                        print(c+x) #3
                    return i #4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the source code: {df.loc[2, 'Source Code']}
Here is the called function: {df.loc[2, 'Algorithm']}
Here is the input to the function {df.loc[2, 'Test Case']}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output.                                                                                          
'''

one_shot_generative_prompt = f''' This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will ask you to generate the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible, please annotate every line with its index as comments (those begin with a #). The following is very important !*Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function prompt, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """def simple_loop(x): #1
                    for i in range(3): #2
                        print(c+x) #3
                    return i #4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the prompt for the source code: Generate a simple bubble sort algorithm.
Here is the input to the function {df.loc[0, 'Test Case']}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines.                                                                                          
'''

one_shot_generative_prompt_java = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will ask you to generate the source code of a program written in Java. The program may feature different functions, which may call each other.
To make the task more accessible, please annotate every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function prompt, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """public static void simple_loop(int x): //1
                    for(int i=0; i<3; i++): //2
                        System.out.println(c+x) //3
                    return i //4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the prompt for the source code: Generate a simple bubble sort algorithm in Java.
Here is the input to the function [1,2,3]
Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines.                                                                                          
'''

one_shot_generative_prompt_CPP = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will ask you to generate the source code of a program written in C++. The program may feature different functions, which may call each other.
To make the task more accessible, please annotate every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the function prompt, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """void simple_loop(int x): //1
                    for(int i=0; i<3; i++): //2
                        std::cout << (i+x) << //3
                    return i //4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the prompt for the source code: Generate a simple bubble sort algorithm in C++.
Here is the input to the function [1,2,3]
Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the code and the lines. 
'''

one_shot_prompt_CPP = '''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in C++. The program may feature different functions, which may call each other.
To make the task more accessible, I have annotated every line with its index as comments (those begin with a //). The following is very important !*Please note that the function signatures are generally not called,
 instead you should start with the first line of the function. This does not apply to the function call of course.* In addition to the source code, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """void simple_loop(int x): //1
                    for(int i=0; i<3; i++): //2
                        std::cout << (i+x) << //3
                    return i //4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the source code: .void bubbleSort(int arr[], int n) { //1
    for (int i = 0; i < n - 1; i++) //2
        for (int j = 0; j < n - i - 1; j++) //3
            if (arr[j] > arr[j + 1]) //4
                std::swap(arr[j], arr[j + 1]); //5
} //6
Here are the inputs to the function arr=[1,2,3], n=3
Please produce the list containing the executed line numbers in order now. Remember not to include the function signature lines. No other output besides the lines. 
'''

# Make the prediction
#reply = predict_large_language_model_sample("cs6158-structuralunderstanding", "text-bison@002", 0.1, 2048, 0.8, 40, one_shot_prompt_CPP, "us-central1")


from anthropic import AnthropicVertex

client = AnthropicVertex(region="us-east5", project_id="cs6158-structuralunderstanding")
 
message = client.messages.create(
    max_tokens=1024,
    messages=[
      {
        "role": "user",
        "content": one_shot_prompt_CPP,
      }
],
  model="claude-3-5-sonnet@20240620",
)
  
reply = message.model_dump_json(indent=2)


# Check if the output matches the expected value
expected_value = str(df.loc[2, 'Executed Lines'])
match = (reply == expected_value or reply == expected_value[1:])

# Log the details
logging.info(
    "Model: %s, Algorithm: %s, Input: %s, Output: %s, Matched: %s",
    "text-bison@002",
    df.loc[0, 'Algorithm'],
    df.loc[0, 'Test Case'],
    reply,
    match
)

print(match)
