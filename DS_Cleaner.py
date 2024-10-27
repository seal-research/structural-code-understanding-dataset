import pandas as pd
import re
from Google_API import calculate_distance

def clean_whitespace(s):
    """Clean double whitespaces from the string."""
    return ' '.join(s.split())

def recompute_metrics(df):
    """Recompute the Matched and Distance metrics for the predictions."""
    results = []
    
    for index, row in df.iterrows():
        predicted = row['Predicted']
        actual = row['Actual']
        human_eval_id = row['HumanEval_ID']
        
        # Clean double whitespaces in predicted and actual
        predicted = clean_whitespace(predicted)
        actual = clean_whitespace(actual)

        # Regular expression to match the expected output format
        pattern = r'\[\d+(?:,\s*\d+)*\s*\]?'

        # Attempt to find a match
        match = re.search(pattern, predicted)
        
        if match:
            cleaned_predicted = match.group(0)
        else:
            # If the predicted ends with a number or a comma without a closing bracket
            if predicted.endswith((' ', ',', *map(str, range(10)))):
                cleaned_predicted = predicted.strip() + ']'  # Add closing bracket
            else:
                cleaned_predicted = "ERROR"

        # Clean any potential double whitespaces in the cleaned predicted
        cleaned_predicted = clean_whitespace(cleaned_predicted)

        # Recompute matching and distance metrics
        matched = cleaned_predicted.strip() == str(actual)
        distance = calculate_distance(actual, cleaned_predicted.strip())
        
        # Append results to the list
        results.append([human_eval_id, row['Name'], row['FunctionCall'], cleaned_predicted, actual, matched, distance])
    
    # Create a DataFrame from the results
    results_df = pd.DataFrame(results, columns=['HumanEval_ID', 'Name', 'FunctionCall', 'Predicted', 'Actual', 'Matched', 'Distance'])
    
    return results_df


