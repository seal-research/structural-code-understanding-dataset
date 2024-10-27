import logging
import time
import random
import torch
import difflib
import json
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

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

def prompt_model(model_name, prompt):
    """Generate text using the specified model."""
    if "deepseek" in model_name.lower() or "codeqwen" in model_name.lower():
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
        raise ValueError("Unsupported model. Please use either 'deepseek' or 'codeqwen'.")

def process_batch(batch_df, model_name):
    """Process a batch of requests."""
    batch_results = []
    for index, row in batch_df.iterrows():
        try:
            # Create a prompt for the model
            prompt = f"""This task will evaluate your ability to appreciate the control flow of code with a given input.
            Here is the source code: {row['Code_Indices']}
            Here is the called function: {row['Name']}
            Here is the input to the function {row['FunctionCall']}
            Please produce the python list containing the executed line numbers in order now."""
            
            # Use the appropriate model with backoff
            response = exponential_backoff_retry(lambda: prompt_model(model_name, prompt))

            actual_lines = row['ExecutedLines']

            # Calculate similarity or distance (you'll need to define this function)
            distance = calculate_distance(actual_lines, response)

            # Determine if the output matches the expected value
            matching = (response == str(actual_lines) or response == str(actual_lines[1:]))

            # Append result to the list
            batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], response, actual_lines, matching, distance])

        except Exception as e:
            logging.error(f"Error in entry {row['HumanEval_ID']}: {e}")
            batch_results.append([row['HumanEval_ID'], row['Name'], row['FunctionCall'], "ERROR", "ERROR", False, "N/A"])

    return batch_results

def batch_test_llm_on_code(df, model_name, batch_size=10):
    """Test LLM on all entries in the dataset, processing requests in batches."""
    total_results = []
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        batch_df = df[start_idx:end_idx]
        
        logging.info(f"Processing batch {batch_num + 1} of {num_batches}.")
        
        # Process the current batch
        batch_results = process_batch(batch_df, model_name)
        
        # Add batch results to the total results
        total_results.extend(batch_results)

    return total_results

# Save results to CSV
def save_results_to_csv(results, filename="Model_HumanEval.csv"):
    """Save the results to a CSV file."""
    results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Main execution flow
if __name__ == "__main__":
    # Load your DataFrame here (you'll need to adjust this to your dataset)
    df = pd.read_csv("HumanEval_trace_expanded_fixed_reannotated.csv")  # Example line to load data

    model_name = "deepseek-coder-v2-lite-instruct-1729178736840@1"  # Change this as needed
    results = batch_test_llm_on_code(df, model_name)
    save_results_to_csv(results, filename=f"{model_name}_HumanEval.csv")
