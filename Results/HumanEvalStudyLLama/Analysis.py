import pandas as pd
import json
from scipy.stats import spearmanr

# Load CSV Files
csv1 = pd.read_csv("HumanEvalGenerativeResults.csv")
csv2 = pd.read_csv("HumanEvalGenerativeResultsDirect.csv")

# Load JSON File
with open("llama_results/eval_results.json", "r") as f:
    json_data = json.load(f)

# Extract JSON-based difficulty rankings
json_difficulty = []
for task, evaluations in json_data["eval"].items():
    for evaluation in evaluations:
        total_tests = len(evaluation["base_tests"])  # Assuming total_tests refers to the total number of tests (base_tests or plus_tests)
        base_fails = len(evaluation["base_fail_tests"])
        plus_fails = len(evaluation["plus_fail_tests"])

        # Calculate the fraction of failures
        base_fail_fraction = base_fails / total_tests if total_tests > 0 else 0
        plus_fail_fraction = plus_fails / total_tests if total_tests > 0 else 0
        
        json_difficulty.append({
            "HumanEval_ID": task,
            "base_fail_fraction": base_fail_fraction,
            "plus_fail_fraction": plus_fail_fraction
        })
json_df = pd.DataFrame(json_difficulty)

# Rank tasks by failure fraction
csv1['rank_fraction_matched'] = csv1['fraction_matched'].rank(ascending=False)
csv1['rank_avg_similarity'] = csv1['average_similarity'].rank(ascending=False)

csv2['rank_fraction_matched'] = csv2['fraction_matched'].rank(ascending=False)
csv2['rank_avg_similarity'] = csv2['average_similarity'].rank(ascending=False)

# Rank by the fraction of failed tests (base_fail_fraction and plus_fail_fraction)
json_df['base_rank'] = json_df['base_fail_fraction'].rank(ascending=False)
json_df['plus_rank'] = json_df['plus_fail_fraction'].rank(ascending=False)

# Merge datasets to ensure matching HumanEval_IDs
csv1_json_base = pd.merge(csv1, json_df[['HumanEval_ID', 'base_rank']], on='HumanEval_ID', how='inner')
csv1_json_plus = pd.merge(csv1, json_df[['HumanEval_ID', 'plus_rank']], on='HumanEval_ID', how='inner')

csv2_json_base = pd.merge(csv2, json_df[['HumanEval_ID', 'base_rank']], on='HumanEval_ID', how='inner')
csv2_json_plus = pd.merge(csv2, json_df[['HumanEval_ID', 'plus_rank']], on='HumanEval_ID', how='inner')

# Compute Spearman Rank Correlations
correlations = {
    "csv1_fraction_vs_csv2_fraction": spearmanr(csv1['rank_fraction_matched'], csv2['rank_fraction_matched'])[0],
    "csv1_similarity_vs_csv2_similarity": spearmanr(csv1['rank_avg_similarity'], csv2['rank_avg_similarity'])[0],
    "csv1_fraction_vs_json_base": spearmanr(csv1_json_base['rank_fraction_matched'], csv1_json_base['base_rank'])[0],
    "csv1_fraction_vs_json_plus": spearmanr(csv1_json_plus['rank_fraction_matched'], csv1_json_plus['plus_rank'])[0],
    "csv2_fraction_vs_json_base": spearmanr(csv2_json_base['rank_fraction_matched'], csv2_json_base['base_rank'])[0],
    "csv2_fraction_vs_json_plus": spearmanr(csv2_json_plus['rank_fraction_matched'], csv2_json_plus['plus_rank'])[0],
}

# Identify overlapping failing tasks
json_base_failing = set(json_df[json_df['base_fail_fraction'] > 0]['HumanEval_ID'])
json_plus_failing = set(json_df[json_df['plus_fail_fraction'] > 0]['HumanEval_ID'])

csv1_failing = set(csv1[csv1['fraction_matched'] < 1.0]['HumanEval_ID'])
csv2_failing = set(csv2[csv2['fraction_matched'] < 1.0]['HumanEval_ID'])

overlap_counts = {
    "csv1_csv2": len(csv1_failing.intersection(csv2_failing)),
    "csv1_json_base": len(csv1_failing.intersection(json_base_failing)),
    "csv1_json_plus": len(csv1_failing.intersection(json_plus_failing)),
    "csv2_json_base": len(csv2_failing.intersection(json_base_failing)),
    "csv2_json_plus": len(csv2_failing.intersection(json_plus_failing)),
}

# Print Results
print("Rank Correlations:")
for key, value in correlations.items():
    print(f"{key}: {value:.4f}")

# Calculate and print the overlapping failing tasks as fractions of the total failing tasks
total_csv1_failing = len(csv1_failing)
total_csv2_failing = len(csv2_failing)
total_json_base_failing = len(json_base_failing)
total_json_plus_failing = len(json_plus_failing)

print("\nOverlapping Failing Tasks:")
for key, value in overlap_counts.items():
    if key.startswith('csv1'):
        total_failing = total_csv1_failing
    elif key.startswith('csv2'):
        total_failing = total_csv2_failing
    elif key.startswith('json_base'):
        total_failing = total_json_base_failing
    elif key.startswith('json_plus'):
        total_failing = total_json_plus_failing

    fraction_overlap = value / total_failing if total_failing > 0 else 0
    print(f"{key}: {value} ({fraction_overlap:.4f})")
