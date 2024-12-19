import json

# Load JSON data from a file
with open('problemSiteData.json', 'r') as file:
    data = json.load(file)

import ast
import inspect
import builtins
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Optional
import os
import shutil

tagged = [
    "1671 - Minimum Number of Removals to Make Mountain Array",
    "0002 - Add Two Numbers",
    "0010 - Regular Expression Matching",
    "0021 - Merge Two Sorted Lists",
    "0024 - Swap Nodes in Pairs",
    "0025 - Reverse Nodes in k-Group",
    "0044 - Wildcard Matching",
    "0050 - Pow(x, n)",
    "0060 - Permutation Sequence",
    "0143 - Reorder List",
    "0203 - Remove Linked List Elements",
    "0206 - Reverse Linked List",
    "0224 - Basic Calculator",
    "0231 - Power of Two",
    "0233 - Number of Digit One",
    "0234 - Palindrome Linked List",
    "0241 - Different Ways to Add Parentheses",
    "0247 - Strobogrammatic Number II",
    "0248 - Strobogrammatic Number III",
    "0255 - Verify Preorder Sequence in Binary Search Tree",
    "0273 - Integer to English Words",
    "0326 - Power of Three",
    "0342 - Power of Four",
    "0390 - Elimination Game",
    "0394 - Decode String",
    "0439 - Ternary Expression Parser",
    "0486 - Predict the Winner",
    "0509 - Fibonacci Number",
    "0544 - Output Contest Matches",
    "0736 - Parse Lisp Expression",
    "0761 - Special Binary String",
    "0770 - Basic Calculator IV",
    "0772 - Basic Calculator III",
    "0776 - Split BST",
    "0779 - K-th Symbol in Grammar",
    "0894 - All Possible Full Binary Trees",
    "1106 - Parsing A Boolean Expression",
    "1265 - Print Immutable Linked List in Reverse",
    "1545 - Find Kth Bit in Nth Binary String",
    "1808 - Maximize Number of Nice Divisors",
    "1823 - Find the Winner of the Circular Game",
    "1922 - Count Good Numbers",
    "1969 - Minimum Non-Zero Product of the Array Elements",
    "2487 - Remove Nodes From Linked List",
    "2550 - Count Collisions of Monkeys on a Polygon",
    "3304 - Find the K-th Character in String Game I",
    "3307 - Find the K-th Character in String Game II",
]



import requests
from pathlib import Path
import json
import re

# Function to check if any function in the code is recursive
def is_any_function_recursive(code: str):
    try:
        tree = ast.parse(code)
    except (SyntaxError, NameError) as e:
        print(f"Error parsing code: {e}")
        return False

    class RecursiveCallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.recursive_functions = set()

        def visit_FunctionDef(self, node):
            # Check for recursion within this function
            self.current_function = node.name
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if node.func.id == self.current_function:
                    self.recursive_functions.add(self.current_function)
                    print(f"Recursive call detected in {self.current_function} on line {node.lineno}.")
            self.generic_visit(node)

    visitor = RecursiveCallVisitor()
    visitor.visit(tree)

    return bool(visitor.recursive_functions)

# Set up the directory
download_dir = Path('Dataset/Recursion_LeetCode')
download_dir.mkdir(parents=True, exist_ok=True)

# Base URL for the GitHub repository
repo_url = "https://api.github.com/repos/neetcode-gh/leetcode/contents"
folders = ['python', 'java']

def extract_statements(if_statement):
    statements = []

    # Extract statements from the then part
    if if_statement.then_statement:
        if isinstance(if_statement.then_statement, javalang.tree.BlockStatement):
            statements.extend(if_statement.then_statement.statements)
        else:
            statements.append(if_statement.then_statement)

    # Extract statements from the else part
    if if_statement.else_statement:
        if isinstance(if_statement.else_statement, javalang.tree.BlockStatement):
            statements.extend(if_statement.else_statement.statements)
        else:
            statements.append(if_statement.else_statement)

    return statements


# Example usage:

import javalang

def check_java_for_recursion(java_code):
    """
    Checks Java code for recursion by parsing the code and analyzing method calls.

    Args:
        java_code (str): The Java code to analyze.

    Returns:
        list: A list of potentially recursive method names.
    """
    try:
        # Parse the Java code
        tree = javalang.parse.parse(java_code)
    except javalang.parser.JavaSyntaxError as e:
        print(f"Syntax error in the provided Java code: {e}")
        return []

    recursive_methods = []
    method_map = {node.name: node for _, node in tree.filter(javalang.tree.MethodDeclaration)}

    def contains_recursion(method_node, method_name):
        """Recursively check if the method node calls itself."""
        statements = getattr(method_node, 'statements', getattr(method_node, 'body', []))
        if statements == []:
            if(isinstance(method_node, javalang.tree.IfStatement)):
                statements = extract_statements(method_node)
            elif(isinstance(method_node, javalang.tree.StatementExpression)):
                print(method_node)
        for statement in statements:

            if isinstance(statement, javalang.tree.StatementExpression):
                invocation = statement.expression
                if isinstance(invocation, javalang.tree.MethodInvocation) and invocation.member == method_name:
                    return True
                elif isinstance(invocation, javalang.tree.MemberReference) and invocation.member == method_name:
                    return True

            elif isinstance(statement, javalang.tree.IfStatement):
                if contains_recursion(statement.then_statement, method_name):
                    return True
                if statement.else_statement and contains_recursion(statement.else_statement, method_name):
                    return True
            elif isinstance(statement, javalang.tree.BlockStatement):
                if contains_recursion(statement, method_name):
                    return True

            elif isinstance(statement, (javalang.tree.ForStatement, javalang.tree.WhileStatement)):
                if contains_recursion(statement.body, method_name):
                    return True
            
            elif isinstance(statement, javalang.tree.LocalVariableDeclaration):
                # Check for method calls in local variable declarations
                for variable in statement.declarators:  # Use declarators to access the declared variables
                    if hasattr(variable, 'initializer'):
                        initializer = variable.initializer
                        if isinstance(initializer, javalang.tree.MethodInvocation) and initializer.member == method_name:
                            return True
                        elif isinstance(initializer, javalang.tree.MemberReference) and initializer.member == method_name:
                            return True

            # Check if the statement has a body and recursively check that
            elif hasattr(statement, 'body'):
                body_statements = getattr(statement, 'body', [])
                for stmt in body_statements:
                    if contains_recursion(stmt, method_name):
                        return True

        return False


    # Check each method for recursion
    for method_name, method_node in method_map.items():
        if contains_recursion(method_node, method_name):
            recursive_methods.append(method_name)

    return len(recursive_methods) > 0


def sanitize_code(code):
    # Remove non-ASCII characters
    return ''.join(filter(lambda x: ord(x) < 128, code))

def Download_Recursion_LeetCode():
    # Download files if they meet criteria
    for folder in folders:
        if(folder == 'java'):
            continue
        response = requests.get(f"{repo_url}/{folder}")
        if response.status_code == 200:
            files = response.json()
            for file in files:
                file_id = file['name'].split('-')[0] 
                python_file_url = None
                java_file_url = None
                
                # Check if files are already downloaded
                already_downloaded = list(download_dir.glob(f"{file_id}*"))
                if already_downloaded:
                    print(f"Skipping {file['name']} as it is already downloaded.")
                    continue

                # Check for Python and Java files
                python_file_url = file['download_url']
                python_response = requests.get(python_file_url)
                sanitized_code = sanitize_code(python_response.text)  # Sanitize code

                # Dynamically define the function from response for checking
                try:
                    exec(sanitized_code, globals())  # Use exec to define the function in global scope
                except NameError as e:
                    print(f"NameError while executing {file['name']}: {e}")
                    python_file_url = None
                except SyntaxError as e:
                    print(f"SyntaxError while executing {file['name']}: {e}")
                    python_file_url = None
                if not is_any_function_recursive(sanitized_code):  # file_id corresponds to function name
                    print(f"{file_id} Python function is not recursive. Skipping.")
                    continue

                java_file_url = file['download_url'].replace('python', 'java').replace('.py', '.java')
                java_response = requests.get(java_file_url)
                if java_response.status_code == 404 or not check_java_for_recursion(java_response.text):
                    print(f"{file_id} Java function is not recursive. Skipping.")
                    continue
                
                # Download files only if both Python and Java versions are recursive
                for url in (python_file_url, java_file_url):
                    if(not url == None and not url == 'None'):
                        file_response = requests.get(url)
                        filename = url.split('/')[-1]
                        file_path = download_dir / filename
                        with open(file_path, 'wb') as f:
                            f.write(file_response.content)
                        print(f"Downloaded {filename} to {download_dir}")

        else:
            print(f"Failed to access {folder} directory.")

# Base URL for the GitHub repository
# Base URL for raw user content
base_url = "https://raw.githubusercontent.com/walkccc/LeetCode/main/solutions"
# Directories for saving downloaded files
python_download_dir = Path("Dataset/Concurrency/Python")  # Directory for Python files
java_download_dir = Path("Dataset/Concurrency/Java")      # Directory for Java files

# Ensure download directories exist
python_download_dir.mkdir(parents=True, exist_ok=True)
java_download_dir.mkdir(parents=True, exist_ok=True)

# List of tagged Concurrency IDs and their descriptions
tagged_Concurrency = [
    "1279. Traffic Light Controlled Intersection",
    "1242. Web Crawler Multithreaded",
    "1226. The Dining Philosophers",
    "1195. Fizz Buzz Multithreaded",
    "1188. Design Bounded Blocking Queue",
    "1117. Building H2O",
    "1116. Print Zero Even Odd",
    "1115. Print FooBar Alternately",
    "1114. Print in Order"
]

def Download_Concurrency_LeetCode():
    """Download Python and Java files for specified concurrency problems."""
    
    for problem in tagged_Concurrency:
        problem_id = problem.split('.')[0]  # Extract the ID from the problem description
        
        # Construct URLs for Python and Java files
        python_file_url = f"{base_url}/{problem}/{problem_id}.py"
        java_file_url = f"{base_url}/{problem}/{problem_id}.java"

        # Download Python file
        python_response = requests.get(python_file_url)
        if python_response.status_code == 200:
            with open(python_download_dir / f"{problem_id}.py", 'wb') as f:
                f.write(python_response.content)
            print(f"Downloaded Python file for ID {problem_id}: {problem_id}.py")
        else:
            print(f"Failed to download Python file for ID {problem_id}: {python_response.status_code} - {python_file_url}")

        # Download Java file
        java_response = requests.get(java_file_url)
        if java_response.status_code == 200:
            with open(java_download_dir / f"{problem_id}.java", 'wb') as f:
                f.write(java_response.content)
            print(f"Downloaded Java file for ID {problem_id}: {problem_id}.java")
        else:
            print(f"Failed to download Java file for ID {problem_id}: {java_response.status_code} - {java_file_url}")

# Call the function
Download_Concurrency_LeetCode()


def get_problems():
    """Return a list of problem names to extract."""
    return [
        "Active-object",
        "Atomic-updates",
        "Checkpoint-synchronization",
        "Concurrent-computing",
        "Determine-if-only-one-instance-is-running",
        "Dining-philosophers",
        "Events",
        "Handle-a-signal",
        "Metered-concurrency",
        "Rendezvous",
        "Synchronous-concurrency"
    ]

def get_recursion_problems():
    """Return a list of recursion problem names to extract."""
    return [
        "Ackermann-function",
        "Anonymous-recursion",
        "Arithmetic-evaluation",
        "Binary-search",
        "Determine-sentence-type",
        "Dragon-curve",
        "Factorial",
        "Fibonacci-sequence",
        "FizzBuzz",
        "Fractal-tree",
        "General-FizzBuzz",
        "Greatest-common-divisor",
        "Least-common-multiple",
        "Longest-common-subsequence",
        "Man-or-boy-test",
        "Maze-solving",
        "Mutual-recursion",
        "Palindrome-detection",
        "Parse-EBNF",
        "Partition-function-P",
        "Power-set",
        "Ramer-Douglas-Peucker-line-simplification",
        "Sorting-algorithms/Merge-sort",
        "Sorting-algorithms/Quicksort",
        "Sudan-function",
        "Towers-of-Hanoi",
        "Tree-traversal",
        "Variadic-fixed-point-combinator",
        "Y-combinator"
    ]

def get_languages():
    """Return a dictionary of languages and their corresponding directory names and file extensions."""
    return {
        "Python": ("Python", "py"),
        "Java": ("Java", "java")
    }

def create_output_directory(base_dir):
    """Create the base output directory if it does not exist."""
    os.makedirs(base_dir, exist_ok=True)

def construct_raw_file_url(base_raw_url, task_name, language, version_suffix=""):
    """Construct the raw file URL for a given task and language, with an optional version suffix."""
    return f"{base_raw_url}/Task/{task_name}/{language[0]}/{task_name.lower()}{version_suffix}.{language[1]}"

def download_and_save_file(url, save_path):
    """Download the file from a URL and save it locally."""
    print(f"Downloading from: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "w") as file:
            file.write(response.text)
        print(f"Saved to: {save_path}")
        return True
    else:
        print(f"Failed to download {url} with status code: {response.status_code}")
    return False

def extract_code_files(base_raw_url, output_dir, type=0):
    """Main function to extract code files for the specified problems and languages."""
    if(type==0):
        problems = get_problems()
    elif(type==1):
        problems = get_recursion_problems()
    languages = get_languages()
    create_output_directory(output_dir)

    for problem in problems:
        for language, (lang_dir, extension) in languages.items():
            # Create language-specific directory
            language_dir = os.path.join(output_dir, lang_dir)
            os.makedirs(language_dir, exist_ok=True)

            # Attempt to download the standard file
            raw_file_url = construct_raw_file_url(base_raw_url, problem, (lang_dir, extension))
            save_path = os.path.join(language_dir, f"{problem.lower()}.{extension}")

            if not download_and_save_file(raw_file_url, save_path):
                # If the standard file fails, try the first enumerated option (e.g., -1)
                enumerated_file_url = construct_raw_file_url(base_raw_url, problem, (lang_dir, extension), "-1")
                save_path = os.path.join(language_dir, f"{problem.lower()}-1.{extension}")
                download_and_save_file(enumerated_file_url, save_path)

def fetch_rosetta_concurrency():
    """Fetch Rosetta Code concurrency examples from GitHub."""
    base_raw_url = "https://raw.githubusercontent.com/acmeism/RosettaCodeData/main"
    output_dir = "Dataset/Concurrency"
    extract_code_files(base_raw_url, output_dir)
    print("Download completed.")

def fetch_rosetta_recursion():
    """Fetch Rosetta Code concurrency examples from GitHub."""
    base_raw_url = "https://raw.githubusercontent.com/acmeism/RosettaCodeData/main"
    output_dir = "Dataset/Recursion"
    extract_code_files(base_raw_url, output_dir, type=1)
    print("Download completed.")

def sort_files_into_recursion_directory(source_dir, target_dir):
    """Sort Python and Java files from the source directory into the target recursion directory."""
    # Define the target directories for Python and Java files
    python_target_dir = os.path.join(target_dir, "Python")
    java_target_dir = os.path.join(target_dir, "Java")

    # Create the target directories if they do not exist
    os.makedirs(python_target_dir, exist_ok=True)
    os.makedirs(java_target_dir, exist_ok=True)

    # Iterate through files in the source directory
    for filename in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_file_path):  # Check if it's a file
            if filename.endswith(".py"):
                # Move Python files
                shutil.move(source_file_path, os.path.join(python_target_dir, filename))
                print(f"Moved: {filename} to {python_target_dir}")
            elif filename.endswith(".java"):
                # Move Java files
                shutil.move(source_file_path, os.path.join(java_target_dir, filename))
                print(f"Moved: {filename} to {java_target_dir}")
