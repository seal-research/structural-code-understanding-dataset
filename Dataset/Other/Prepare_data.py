import pandas as pd

def balance_traces_with_deduplication(input_file, output_file, max_traces_per_task=10):
    """
    Balances and deduplicates a dataset of execution traces, ensuring at most max_traces_per_task
    per HumanEval_ID and primarily removing duplicates based on 'HumanEval_ID' and 'FunctionCall'.

    Parameters:
    - input_file (str): Path to the input CSV file containing the dataset.
    - output_file (str): Path to the output CSV file to save the processed dataset.
    - max_traces_per_task (int): Maximum number of samples per HumanEval_ID (default is 10).

    The dataset should contain the following columns:
    - HumanEval_ID, Name, FunctionCall, ExecutedLines, ExecutedLines_Symbols, Code_Indices, Code_Symbols
    """

    # Load the dataset
    df = pd.read_csv(input_file)

    # Remove duplicate traces based on 'HumanEval_ID' and 'FunctionCall' columns
    df_unique = df.drop_duplicates(subset=["HumanEval_ID", "FunctionCall"])

    # Group by HumanEval_ID and keep only up to max_traces_per_task unique traces per group
    balanced_df = (
        df_unique.groupby("HumanEval_ID")
        .apply(lambda x: x.head(max_traces_per_task))
        .reset_index(drop=True)
    )

    # Save the balanced and deduplicated dataset
    #balanced_df.to_csv(output_file, index=False)
    #print(f"Balanced and deduplicated dataset saved to {output_file}")
    return balanced_df

# Example usage:
new_df = balance_traces_with_deduplication("HumanEval_trace_expanded_fixed_reannotated.csv", "balanced_dataset.csv")