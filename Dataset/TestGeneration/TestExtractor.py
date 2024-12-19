import os
import logging
import json
import time
import random
import requests
from typing import List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass
class JavaTestCase:
    source_python: str
    source_java: str
    test_code: str
    description: str

class TestAdapter:
    def __init__(self, config_path: str = "openai.json"):
        self.api_key = self._load_api_key(config_path)
        
    def _load_api_key(self, path: str) -> str:
        try:
            with open(path, "r") as file:
                return json.load(file)["secret_key"]
        except Exception as e:
            logging.error(f"Error loading API key: {str(e)}")
            raise

    def _call_gpt(self, prompt: str, retries: int = 5) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4-turbo-preview",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        
        for attempt in range(retries):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                if attempt < retries - 1:
                    logging.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to get response after {retries} attempts: {str(e)}")

    def adapt_test_case(self, python_code: str, java_code: str) -> str:
        """Adapt a Python test to Java based on both source files."""
        prompt = f"""
Given these equivalent programs in Python and Java:

Python source:
```python
{python_code}
```

Java source:
```java
{java_code}
```

Create a Java main method that tests the functionality in a way equivalent to the Python test code (in the if __name__ == '__main__': block).

Requirements:
1. Only modify/replace the main method content
2. Keep all existing class definitions and methods
3. Use System.out.println for output
4. Include comments explaining the test
5. Maintain equivalent test coverage and functionality
6. Handle Java-specific requirements (e.g., explicit typing)

Return ONLY the complete main method code block, nothing else.
"""
        response = self._call_gpt(prompt)
        logging.debug(f"Generated Java test:\n{response}")
        return response

    def process_files(self, topic: str) -> List[JavaTestCase]:
        """Process matching Python and Java files for a given topic."""
        python_dir = os.path.join(f"{topic}_prepared", "Python")
        java_dir = os.path.join(f"{topic}_prepared", "Java")
        test_cases = []

        if not os.path.exists(python_dir) or not os.path.exists(java_dir):
            logging.error(f"Directory not found for topic {topic}")
            return test_cases

        for py_file in os.listdir(python_dir):
            if not py_file.endswith('.py'):
                continue

            base_name = os.path.splitext(py_file)[0]
            java_file = f"{base_name}.java"
            java_path = os.path.join(java_dir, java_file)

            if not os.path.exists(java_path):
                logging.warning(f"No matching Java file for {py_file}")
                continue

            try:
                # Read both source files
                with open(os.path.join(python_dir, py_file), 'r', encoding='utf-8') as f:
                    python_source = f.read()
                with open(java_path, 'r', encoding='utf-8') as f:
                    java_source = f.read()

                logging.info(f"Processing {base_name}...")
                
                # Generate Java test
                java_test = self.adapt_test_case(python_source, java_source)
                
                test_cases.append(JavaTestCase(
                    source_python=python_source,
                    source_java=java_source,
                    test_code=java_test,
                    description=f"Adapted test for {base_name}"
                ))
                
            except Exception as e:
                logging.error(f"Error processing {base_name}: {str(e)}")

        return test_cases

    def update_java_files(self, topic: str, test_cases: List[JavaTestCase]):
        """Update Java files with the new test code."""
        java_dir = os.path.join(f"{topic}_prepared", "Java")
        
        for test_case in test_cases:
            # Extract the original file name from the Java source
            class_name = None
            for line in test_case.source_java.split('\n'):
                if 'public class' in line:
                    class_name = line.split('public class')[1].split('{')[0].strip()
                    break
            
            if not class_name:
                logging.error("Could not find class name in Java source")
                continue
                
            file_path = os.path.join(java_dir, f"{class_name}.java")
            
            try:
                # Read the original file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the main method
                import re
                new_content = re.sub(
                    r'public static void main\(String\[\] args\)[^}]*}',
                    f'public static void main(String[] args) {{\n{test_case.test_code}\n}}',
                    content,
                    flags=re.DOTALL
                )
                
                # Write the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                logging.info(f"Updated {file_path}")
                
            except Exception as e:
                logging.error(f"Error updating {file_path}: {str(e)}")

def main():
    adapter = TestAdapter()
    topics = ['Recursion', 'OOP', 'Concurrency']
    
    for topic in topics:
        logging.info(f"Processing {topic} test cases...")
        test_cases = adapter.process_files(topic)
        
        if test_cases:
            adapter.update_java_files(topic, test_cases)
        else:
            logging.warning(f"No test cases generated for {topic}")

if __name__ == "__main__":
    main()