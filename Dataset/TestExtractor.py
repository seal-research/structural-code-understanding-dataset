import os
import logging
import requests
import time
import random
from typing import List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass
class TestCase:
    difficulty: int
    code: str
    description: str

class TestRefactorer:
    def __init__(self, api_key_path: str):
        self.api_key = self._load_api_key(api_key_path)
        
    def _load_api_key(self, path: str) -> str:
        try:
            with open(path, "r") as file:
                import json
                return json.load(file)["secret_key"]
        except Exception as e:
            logging.error(f"Error loading API key: {str(e)}")
            raise

    def _call_gpt4(self, prompt: str, retries: int = 5) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 4096
        }
        
        endpoint = "https://cs6158structuralunderstanding.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
        
        for attempt in range(retries):
            try:
                response = requests.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                if attempt < retries - 1:
                    logging.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to get response after {retries} attempts: {str(e)}")

    def generate_test_case(self, source_code: str, difficulty: int) -> str:
        """Generate a single test case with specified difficulty."""
        prompt = f"""
Given this Python source code:

{source_code}

Create a single test case with difficulty level {difficulty} (1=basic, 5=complex).
The test should be a complete, runnable Python program.

Requirements:
1. Keep all original class definitions
2. Put the test code in the if __name__ == "__main__": block
3. Use print statements to show test results
4. No test frameworks (unittest/pytest)
5. Include comments explaining the test

ONLY return the complete Python code, nothing else.
"""
        response = self._call_gpt4(prompt)
        logging.debug(f"Generated test case:\n{response}")
        return response

    def generate_test_cases(self, source_code: str, num_tests: int = 5) -> List[TestCase]:
        """Generate multiple test cases with increasing difficulty."""
        test_cases = []
        
        for difficulty in range(1, num_tests + 1):
            try:
                code = self.generate_test_case(source_code, difficulty)
                
                # Basic validation - check if it looks like Python code
                if 'def ' not in code and 'class ' not in code:
                    logging.warning(f"Test case {difficulty} appears invalid")
                    continue
                    
                test_cases.append(TestCase(
                    difficulty=difficulty,
                    code=code,
                    description=f"Complexity Level {difficulty} Test"
                ))
                logging.info(f"Successfully generated test case {difficulty}")
                
            except Exception as e:
                logging.error(f"Error generating test case {difficulty}: {str(e)}")
                
        return test_cases

    def save_test_cases(self, base_name: str, test_cases: List[TestCase], output_dir: str):
        """Save generated test cases to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        for i, test_case in enumerate(test_cases, 1):
            file_name = f"{base_name}_trace_{i}.py"
            file_path = os.path.join(output_dir, file_name)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Test Case {i} - Difficulty Level: {test_case.difficulty}\n")
                    f.write(f"# {test_case.description}\n\n")
                    f.write(test_case.code)
                logging.info(f"Saved test case {i} to {file_path}")
                
            except Exception as e:
                logging.error(f"Error saving test case {i} to {file_path}: {str(e)}")

def process_directory(input_dir: str, output_dir: str, refactorer: TestRefactorer):
    """Process all Python files in the input directory."""
    for file_name in os.listdir(input_dir):
        if not file_name.endswith('.py'):
            continue
            
        input_path = os.path.join(input_dir, file_name)
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            logging.info(f"Processing {file_name}...")
            logging.debug(f"Source code:\n{source_code}")
            
            base_name = os.path.splitext(file_name)[0]
            test_cases = refactorer.generate_test_cases(source_code)
            
            if test_cases:
                refactorer.save_test_cases(base_name, test_cases, output_dir)
            else:
                logging.error(f"No valid test cases generated for {file_name}")
            
        except Exception as e:
            logging.error(f"Error processing {file_name}: {str(e)}")

def main():
    # Enable debug logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    refactorer = TestRefactorer("cs6158_Azure.json")
    base_dirs = ['OOP', 'Concurrency']
    
    for base_dir in base_dirs:
        input_dir = os.path.join(f"{base_dir}", 'Python')
        output_dir = os.path.join(f"{base_dir}_refactored", 'Python')
        
        if not os.path.exists(input_dir):
            logging.warning(f"Input directory {input_dir} does not exist")
            continue
            
        logging.info(f"Processing {base_dir} test cases...")
        process_directory(input_dir, output_dir, refactorer)

if __name__ == "__main__":
    main()