import json
import requests
import time
import random
import logging
import os
import re
from typing import List, Set, Dict
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

# Azure configuration
AZURE_OPENAI_API_KEY = load_api_key()
AZURE_OPENAI_ENDPOINT = "https://cs6158structuralunderstanding.openai.azure.com/"
AZURE_DEPLOYMENT_NAME = "gpt-4o"

def get_file_base_name(filename: str) -> str:
    """Get the base name of a file without extension and potential language suffix."""
    base = os.path.splitext(filename)[0]
    # Remove potential language-specific suffixes if they exist
    base = re.sub(r'_(java|py|python|java)$', '', base.lower())
    return base

def find_matching_files(base_dirs: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Find matching files across Python and Java directories.
    Returns a dict of {base_name: {'Python': python_path, 'Java': java_path}}
    """
    matches = {}
    
    for base_dir in base_dirs:
        py_dir = os.path.join(base_dir, 'Python')
        java_dir = os.path.join(base_dir, 'Java')
        
        if not (os.path.exists(py_dir) and os.path.exists(java_dir)):
            continue
            
        # Get all Python and Java files
        py_files = {get_file_base_name(f): os.path.join(py_dir, f) 
                   for f in os.listdir(py_dir) if f.endswith('.py')}
        java_files = {get_file_base_name(f): os.path.join(java_dir, f) 
                     for f in os.listdir(java_dir) if f.endswith('.java')}
        
        # Find matches
        for base_name in set(py_files.keys()) | set(java_files.keys()):
            if base_name not in matches:
                matches[base_name] = {}
            if base_name in py_files:
                matches[base_name]['Python'] = py_files[base_name]
            if base_name in java_files:
                matches[base_name]['Java'] = java_files[base_name]
    
    return matches

def get_expected_output_files(src_path: str, dest_dir: str, file_type: str) -> List[str]:
    """Generate the list of expected output files for a given source file."""
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    ext = '.py' if file_type == 'py' else '.java'
    return [os.path.join(dest_dir, f"{base_name}_trace_{i}{ext}") for i in range(1, 6)]

def get_missing_files(src_path: str, dest_dir: str, file_type: str) -> List[str]:
    """Check which of the expected output files are missing."""
    expected_files = get_expected_output_files(src_path, dest_dir, file_type)
    return [f for f in expected_files if not os.path.exists(f)]

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
                time.sleep(1)  # Brief pause before retry
    
    logging.error(f"Failed after {retries} attempts. Last error: {str(last_exception)}")
    raise last_exception

def read_file_with_fallback(file_path: str) -> str:
    """Read file content with multiple encoding attempts and error handling."""
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1', 'ascii']
    errors = ['strict', 'ignore', 'replace']
    
    for encoding in encodings:
        for error_handling in errors:
            try:
                with open(file_path, 'r', encoding=encoding, errors=error_handling) as file:
                    content = file.read()
                    if content.strip():  # Check if content is not empty
                        return content
            except Exception as e:
                continue
    
    raise ValueError(f"Could not read file {file_path} with any encoding method")

def modify_existing_version(version: str) -> str:
    """Modify an existing test case version to create a variation."""
    # Simple modification: add a random number to any numeric literals
    import random
    modified = version
    
    # Find numeric literals
    numbers = re.findall(r'\b\d+\b', version)
    for number in numbers:
        # Modify each number slightly
        new_number = str(int(number) + random.randint(1, 10))
        modified = modified.replace(number, new_number, 1)  # Replace only first occurrence
    
    return modified


def sanitize_response(response: str) -> str:
    """Clean and validate GPT response."""
    # Remove common problematic elements
    cleaned = re.sub(r'```[^`]*```', '', response, flags=re.DOTALL)
    cleaned = re.sub(r'```.*?\n', '', cleaned)
    cleaned = re.sub(r'\n```', '', cleaned)
    cleaned = re.sub(r'^.*?Here are.*?\n', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'^.*?versions:.*?\n', '', cleaned, flags=re.DOTALL)
    
    return cleaned.strip()

def extract_code_blocks(response: str) -> List[str]:
    """Extract code blocks using various methods."""
    versions = []
    
    # Method 1: Try splitting by explicit separators
    for separator in ['###', '---', '===', '\n\n\n']:
        candidates = [v.strip() for v in response.split(separator) if v.strip()]
        if len(candidates) >= 1:
            versions = candidates
            break
    
    # Method 2: If no luck with separators, try to identify code blocks by structure
    if not versions:
        # For Java files
        if 'public class' in response or 'class' in response:
            blocks = re.split(r'(?=public class|class\s+\w+)', response)
            versions = [b.strip() for b in blocks if b.strip()]
        
        # For Python files
        elif 'def ' in response:
            blocks = re.split(r'(?=def\s+\w+)', response)
            versions = [b.strip() for b in blocks if b.strip()]
    
    # Method 3: If still no versions, try to extract anything that looks like code
    if not versions:
        # Look for indented blocks
        blocks = re.split(r'\n(?=\S)', response)
        versions = [b.strip() for b in blocks if b.strip() and len(b.split('\n')) > 3]
    
    return versions

def split_versions(response: str) -> List[str]:
    """Enhanced version splitting with multiple fallback methods."""
    try:
        # Clean the response first
        cleaned_response = sanitize_response(response)
        
        # Try to extract code blocks
        versions = extract_code_blocks(cleaned_response)
        
        if not versions:
            # If we still don't have versions, log the response for debugging
            logging.error(f"Failed to extract versions from response: {cleaned_response[:200]}...")
            raise ValueError("No valid versions found in response")
        
        # Ensure we have valid code in each version
        valid_versions = []
        for v in versions:
            if len(v.split('\n')) > 3:  # Basic validation: more than 3 lines
                valid_versions.append(v)
        
        if not valid_versions:
            raise ValueError("No valid code blocks found in versions")
        
        return valid_versions[:5]
        
    except Exception as e:
        logging.error(f"Error splitting versions: {str(e)}")
        raise

def generate_test_prompt(content: str, file_type: str, attempt: int = 0) -> str:
    """Generate prompt with additional clarity for retry attempts."""
    base_prompt = f"""Generate exactly 5 complete versions of the following {'Python' if file_type == 'py' else 'Java'} code.
Each version should be the complete code with a different test case.

Original code:
{content}

Requirements:
1. Return exactly 5 complete versions of the code
2. Each version must include ALL the original code
3. Each version must have exactly ONE test case in the main {'block' if file_type == 'py' else 'method'}
4. Separate each version with ### on a new line
5. Do not add any explanations or comments between versions
6. Do not use markdown formatting

Format:
[Complete code version 1]
###
[Complete code version 2]
###
[Complete code version 3]
###
[Complete code version 4]
###
[Complete code version 5]"""

    if attempt > 0:
        base_prompt += "\n\nCRITICAL: Ensure each version is a complete, compilable code file. Separate versions ONLY with ### on a new line."
    
    return base_prompt

def process_file_pair(base_name: str, file_paths: Dict[str, str], base_dirs: List[str]) -> None:
    """Process a pair of matching Python and Java files with enhanced error recovery."""
    try:
        for lang, src_path in file_paths.items():
            if not src_path:
                continue
                
            file_type = 'py' if lang == 'Python' else 'java'
            base_dir = next(bd for bd in base_dirs if bd in src_path)
            dest_dir = os.path.join(f"{base_dir}_prepared", lang)
            
            os.makedirs(dest_dir, exist_ok=True)
            missing_files = get_missing_files(src_path, dest_dir, file_type)
            
            if not missing_files:
                logging.info(f"All test cases exist for {src_path}")
                continue
                
            logging.info(f"Generating {len(missing_files)} missing test cases for {src_path}")
            
            max_attempts = 3
            success = False
            
            for attempt in range(max_attempts):
                try:
                    content = read_file_with_fallback(src_path)
                    prompt = generate_test_prompt(content, file_type, attempt)
                    
                    response = prompt_gpt4o_with_backoff(prompt)
                    versions = split_versions(response)
                    
                    if len(versions) < 5:
                        # Pad with modified versions if needed
                        base_version = versions[0]
                        while len(versions) < 5:
                            modified = modify_existing_version(base_version)
                            versions.append(modified)
                    
                    # Write the files
                    expected_files = get_expected_output_files(src_path, dest_dir, file_type)
                    for output_file, version in zip(expected_files, versions):
                        if output_file in missing_files:
                            try:
                                with open(output_file, 'w', encoding='utf-8') as file:
                                    file.write(version)
                                logging.info(f"Created test case file: {output_file}")
                            except Exception as e:
                                logging.error(f"Error writing {output_file}: {str(e)}")
                                continue
                    
                    success = True
                    break
                    
                except Exception as e:
                    if attempt < max_attempts - 1:
                        logging.warning(f"Attempt {attempt + 1} failed for {src_path}: {str(e)}. Retrying...")
                        time.sleep(2 * (attempt + 1))  # Increasing delay between attempts
                    else:
                        logging.error(f"Failed to process {src_path} after {max_attempts} attempts: {str(e)}")
            
            if not success:
                logging.error(f"Failed to generate test cases for {src_path}")
                
    except Exception as e:
        logging.error(f"Error processing file pair {base_name}: {str(e)}")

def main():
    base_dirs = ['Recursion', 'Concurrency', 'OOP']
    
    # Find matching files across languages
    matching_files = find_matching_files(base_dirs)
    
    logging.info(f"Found {len(matching_files)} matching file pairs")
    
    # Process each pair of files
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for base_name, file_paths in matching_files.items():
            futures.append(
                executor.submit(process_file_pair, base_name, file_paths, base_dirs)
            )
        
        # Wait for all tasks to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in processing task: {str(e)}")

if __name__ == "__main__":
    main()