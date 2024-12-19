import os
import logging
import pandas as pd
from openai import AzureOpenAI
import requests
import openai
import json
import time
import random
from datasets import load_dataset

random.seed(77)


def load_api_key():
    with open("cs6158_Azure.json", "r") as file:
        data = json.load(file)
        return data["secret_key"]

# Azure configuration
AZURE_OPENAI_API_KEY = load_api_key()  # Get the key from the JSON file
AZURE_OPENAI_ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/"#"https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
AZURE_DEPLOYMENT_NAME = "gpt-4o"

# Exponential backoff function
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

# Function to call GPT-4o with exponential backoff
def prompt_gpt4o_with_backoff(prompt: str, max_tokens: int = 4096):
    """Wrap GPT-4 prompt with exponential backoff."""
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

    return exponential_backoff_retry(call_gpt4o)

# Function to clean the GPT-4o response
def clean_python_code(response: str) -> str:
    """Removes extraneous text like Python''' or code block markers."""
    # Remove any text like "Python'''" or triple backticks
    lines = response.splitlines()
    clean_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block  # Toggle code block status
            continue
        if in_code_block or line.strip():  # Keep lines inside code blocks or non-empty lines
            clean_lines.append(line)

    return "\n".join(clean_lines).strip()

# Directories for input and output
directory = 'Dataset/OOP'
java_output_dir = os.path.join(directory, 'Java')
python_output_dir = os.path.join(directory, 'Python')

# Create output directories if they don't exist
os.makedirs(java_output_dir, exist_ok=True)
os.makedirs(python_output_dir, exist_ok=True)

# Iterate over Java files and translate them to Python
# Iterate over Java files and translate them to Python
for filename in os.listdir(directory):
    if filename.endswith('.java'):
        java_file_path = os.path.join(directory, filename)

        try:
            # Try reading the Java file with utf-8 encoding
            with open(java_file_path, 'r', encoding='utf-8') as file:
                java_code = file.read()

            # Generate the translation prompt
            prompt = f"Translate the following Java code to Python:\n\n{java_code}"

            # Call GPT-4o to translate the Java code
            raw_python_code = prompt_gpt4o_with_backoff(prompt)

            # Clean the Python code
            python_code = clean_python_code(raw_python_code)

            # Save the Java file in the 'Java' folder
            java_output_path = os.path.join(java_output_dir, filename)
            with open(java_output_path, 'w', encoding='utf-8') as file:
                file.write(java_code)

            # Save the translated Python code in the 'Python' folder
            python_filename = filename.replace('.java', '.py')
            python_output_path = os.path.join(python_output_dir, python_filename)
            with open(python_output_path, 'w', encoding='utf-8') as file:
                file.write(python_code)

        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError for file {filename}: {e}")
            continue  # Skip this file and move to the next one
        except Exception as e:
            logging.error(f"An error occurred while processing file {filename}: {e}")
            continue  # Skip this file and move to the next one

print("Translation completed. Java and Python files are saved in their respective folders.")