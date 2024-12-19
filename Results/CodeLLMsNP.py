import logging
import time
import random
import torch
import difflib
import json
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers
import os
import re
from huggingface_hub import login

login(token="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")

# Set up logging
logging.basicConfig(level=logging.INFO)

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

def prompt_model(model_name, prompt, model, tokenizer):
    """Generate text using the specified model."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if "deepseek" in model_name.lower() or "qwen" in model_name.lower():
        
        messages = [{"role": "user", "content": prompt}]
        
        inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(device)

        #inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
        
        if 'token_type_ids' in inputs:
            del inputs['token_type_ids']

        with torch.no_grad():
            input_ids = inputs.input_ids
            input_length = input_ids.shape[1]
            outputs = model.generate(**inputs, max_new_tokens=1024, temperature=0.)[0, input_length:]

        return tokenizer.decode(outputs, skip_special_tokens=True)
    elif 'llama' in model_name.lower():
        with torch.no_grad():
            messages = [{"role": "user", "content": prompt}]


            outputs = model(
                    messages,
                    max_new_tokens=4096,
                    do_sample=False
                  )
        generated_text = outputs[0]["generated_text"][-1]['content']
        return generated_text
    else:
        raise ValueError("Unsupported model. Please use either 'deepseek' or 'codeqwen'.")

def extract_last_python_list_open(text):
    # Use regex to find all lists in the format of Python lists,
    # allowing for the last list to be unclosed if at the end of the string.
    matches = re.findall(r'\[.*?(?:\]|\s*$)', text)
    # Return the last match if available, otherwise None
    return matches[-1] if matches else None

def process_batch(batch_df, model_name, model, tokenizer, cot=False, topic='HumanEval'):
    """Process a batch of requests."""
    batch_results = []
    for index, row in batch_df.iterrows():
        try:
            if(topic=='HumanEval'):
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
                       '''
                    else:
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
                       Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines.  Think about the solution step-by-step,
                       going through execution steps one at a time. Finally, print the solution as a list of executed steps.
                       '''
            elif(topic=='Recursion' or topic=='OOP'):
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
                Do not produce any other output.
                '''
            elif(topic=='Concurrency'):
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
                Do not produce any other output.
                '''
            # Use the appropriate model with backoff
            response = exponential_backoff_retry(lambda: prompt_model(model_name, prompt, model, tokenizer))
            actual_lines = row['ExecutedLines']
            
            response = extract_last_python_list_open(response)

            # Calculate similarity or distance (you'll need to define this function)
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            if(topic == 'HumanEval'):
               batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])
            else:
               batch_results.append([row['Filename'], row['Category'], response, actual_lines, matching, distance])

        except Exception as e:
            logging.error(f"Error in entry {row['']}: {e}")
            if(topic == 'HumanEval'):
               batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], "ERROR", "ERROR", False, "N/A"])
            else:
               batch_results.append([row['Filename'], row['Category'], "ERROR", "ERROR", False, "N/A"])

    return batch_results

def batch_test_llm_on_code(df, model_name, batch_size=2, cot=False, topic='HumanEval'):
    """Test LLM on all entries in the dataset."""
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")
    if not 'llama' in model_name.lower():
       model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True).to(device)
       tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    else:
       model = transformers.pipeline(
       "text-generation",
       model=model_name,
       framework='pt',
       model_kwargs={"torch_dtype": torch.bfloat16},
       device_map="auto",
       )
       tokenizer = None
    total_results = []
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    batches = [df[i * batch_size:(i + 1) * batch_size] for i in range(num_batches)]

    counter = 0

    for batch_df in batches:
        logging.info(f"Starting batch: {counter}")
        counter = counter + 1
        results = process_batch(batch_df, model_name, model, tokenizer, cot, topic)
        total_results.extend(results)

    return total_results

# Save results to CSV
def save_results_to_csv(results, filename="Model_HumanEval.csv", topic='HumanEval'):
    """Save the results to a CSV file."""
    if(topic=='HumanEval'):
       results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    else:
       results_df = pd.DataFrame(results, columns=['Filename', 'Category', 'Predicted', 'Actual', 'Matched', 'Distance'])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Main execution flow
if __name__ == "__main__":
    # Load your DataFrame here
    df = pd.read_csv("program_traces_Python_Concurrency_Lines.csv")

    if torch.cuda.is_available():
      num_gpus = torch.cuda.device_count()
      for i in range(num_gpus):
        print(f"Device {i}: {torch.cuda.get_device_name(i)}")
    else:
      print("CUDA is not available.")
    model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    #model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"  # Change this as needed
    results = batch_test_llm_on_code(df, model_name, cot=True, topic='Concurrency')
    save_results_to_csv(results, filename=f"LLama8B_Concurrency_CoT_T0.csv")
