import json
import requests
import time
import random
import logging
import os
import re
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

def load_api_key():
    try:
        with open("cs6158_Azure.json", "r") as file:
            data = json.load(file)
            return data["secret_key"]
    except Exception as e:
        logging.error(f"Error loading API key: {str(e)}")
        raise

AZURE_OPENAI_API_KEY = load_api_key()

def get_file_base_name(filename: str) -> str:
    base = os.path.splitext(filename)[0]
    base = re.sub(r'_trace_\d+$', '', base.lower())  # Remove trace number
    base = re.sub(r'_(java|py|python|java)$', '', base)
    return base

def find_test_files(base_dirs: List[str]) -> Dict[str, Dict[str, List[str]]]:
    """Find all test files in the prepared directories."""
    test_files = {}
    
    for base_dir in base_dirs:
        py_dir = os.path.join(f"{base_dir}_prepared", 'Python')
        java_dir = os.path.join(f"{base_dir}_prepared", 'Java')
        
        for dir_path in [py_dir, java_dir]:
            if not os.path.exists(dir_path):
                continue
                
            lang = 'Python' if 'Python' in dir_path else 'Java'
            files = [f for f in os.listdir(dir_path) if f.endswith('.py' if lang == 'Python' else '.java')]
            
            for file in files:
                base_name = get_file_base_name(file)
                if base_name not in test_files:
                    test_files[base_name] = {'Python': [], 'Java': []}
                test_files[base_name][lang].append(os.path.join(dir_path, file))
    
    return test_files

def prompt_gpt4o_with_backoff(prompt: str, max_tokens: int = 4096):
    """Wrap GPT-4 prompt with exponential backoff."""
    def call_gpt4o():
        try:
            headers = {
                "Content-Type": "application/json",
                "api-key": f"{AZURE_OPENAI_API_KEY}"
            }

            payload = {
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0,
                "top_p": 1.0,
                "max_tokens": max_tokens
            }

            ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()
            return reply['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"Error in GPT-4 call: {str(e)}")
            raise

    return exponential_backoff_retry(call_gpt4o)

def exponential_backoff_retry(func, retries=10, backoff_factor=2, max_wait=120):
    wait = 1
    last_exception = None
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if "429" in str(e) or "529" in str(e):
                wait_time = min(wait * (1 + random.uniform(-0.1, 0.1)), max_wait)
                logging.warning(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}. Retrying in {wait_time:.1f} seconds.")
                time.sleep(wait_time)
                wait = min(wait * backoff_factor, max_wait)
            else:
                logging.warning(f"Error on attempt {attempt + 1}: {str(e)}. Retrying...")
                time.sleep(1)
    
    logging.error(f"Failed after {retries} attempts. Last error: {str(last_exception)}")
    raise last_exception

def read_file_with_fallback(file_path: str) -> str:
    """Read file content with multiple encoding attempts."""
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1', 'ascii']
    errors = ['strict', 'ignore', 'replace']
    
    for encoding in encodings:
        for error_handling in errors:
            try:
                with open(file_path, 'r', encoding=encoding, errors=error_handling) as file:
                    content = file.read()
                    if content.strip():
                        return content
            except Exception:
                continue
    
    raise ValueError(f"Could not read file {file_path} with any encoding method")

def generate_validation_prompt(content: str, file_type: str, category: str) -> str:
    """Generate prompt to validate test cases based on category."""
    base_prompt = f"""Analyze this {'Python' if file_type == 'py' else 'Java'} test case and verify:

{content}

For this {category} implementation, check:
"""

    if category == "OOP":
        base_prompt += """
1. Are the majority of class methods being tested?
2. Is the object-oriented structure (inheritance, encapsulation, etc.) being properly exercised?
3. Is all testing code properly wrapped in the main method (except for method/class definitions)?
4. Can this code be executed correctly with Python3/Java?
5. Are there any syntax errors or runtime errors?

Provide a JSON response with these fields:
{
    "methods_tested": boolean,
    "oop_structure_tested": boolean,
    "main_method_correct": boolean,
    "executable": boolean,
    "errors": list of strings or empty list,
    "suggestions": list of strings or empty list
}"""

    elif category == "Concurrency":
        base_prompt += """
1. Does the test actually invoke concurrent execution (threads/processes)?
2. Is proper synchronization being tested?
3. Is all testing code properly wrapped in the main method (except for thread/class definitions)?
4. Can this code be executed correctly with Python3/Java?
5. Are there any syntax errors or runtime errors?

Provide a JSON response with these fields:
{
    "concurrent_execution": boolean,
    "synchronization_tested": boolean,
    "main_method_correct": boolean,
    "executable": boolean,
    "errors": list of strings or empty list,
    "suggestions": list of strings or empty list
}"""

    return base_prompt

def validate_test_file(file_path: str, category: str) -> Dict:
    """Validate a single test file."""
    try:
        content = read_file_with_fallback(file_path)
        file_type = 'py' if file_path.endswith('.py') else 'java'
        
        prompt = generate_validation_prompt(content, file_type, category)
        response = prompt_gpt4o_with_backoff(prompt)
        
        try:
            validation_result = json.loads(response)
            return validation_result
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON response for {file_path}")
            return {
                "executable": False,
                "errors": ["Invalid response format from GPT"],
                "suggestions": ["Please retry validation"]
            }
            
    except Exception as e:
        logging.error(f"Error validating {file_path}: {str(e)}")
        return {
            "executable": False,
            "errors": [str(e)],
            "suggestions": ["Error during validation"]
        }

def process_test_files(base_name: str, file_paths: Dict[str, List[str]], category: str) -> None:
    """Process and validate test files for a given implementation."""
    try:
        for lang, files in file_paths.items():
            if not files:
                continue
            
            logging.info(f"Validating {len(files)} test files for {base_name} ({lang})")
            
            for file_path in files:
                logging.info(f"Validating {file_path}")
                validation_result = validate_test_file(file_path, category)
                
                # Log validation results
                if validation_result.get("executable", False):
                    if category == "OOP":
                        if not validation_result.get("methods_tested", False):
                            logging.warning(f"{file_path}: Not all methods are being tested")
                        if not validation_result.get("oop_structure_tested", False):
                            logging.warning(f"{file_path}: OOP structure not fully tested")
                    elif category == "Concurrency":
                        if not validation_result.get("concurrent_execution", False):
                            logging.warning(f"{file_path}: No proper concurrent execution")
                        if not validation_result.get("synchronization_tested", False):
                            logging.warning(f"{file_path}: Synchronization not properly tested")
                
                if validation_result.get("errors"):
                    logging.error(f"Errors in {file_path}:")
                    for error in validation_result["errors"]:
                        logging.error(f"  - {error}")
                
                if validation_result.get("suggestions"):
                    logging.info(f"Suggestions for {file_path}:")
                    for suggestion in validation_result["suggestions"]:
                        logging.info(f"  - {suggestion}")
                
    except Exception as e:
        logging.error(f"Error processing test files for {base_name}: {str(e)}")

def main():
    base_dirs = ['Concurrency', 'OOP']
    
    # Find all test files
    test_files = find_test_files(base_dirs)
    
    logging.info(f"Found {len(test_files)} implementations to validate")
    
    # Process each implementation's test files
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for base_name, file_paths in test_files.items():
            # Determine category from directory
            category = next((dir_name for dir_name in base_dirs if dir_name in file_paths['Python'][0] or dir_name in file_paths['Java'][0]), None)
            if category:
                futures.append(
                    executor.submit(process_test_files, base_name, file_paths, category)
                )
        
        # Wait for all tasks to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in validation task: {str(e)}")

if __name__ == "__main__":
    main()