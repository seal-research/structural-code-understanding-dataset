import json
import matplotlib.pyplot as plt

# Function to count lines of code in the canonical solution
def count_lines_of_code(solution):
    lines = solution.split('\n')
    # Exclude empty lines and lines that are just function definitions or docstrings
    meaningful_lines = [line for line in lines if line.strip() and not line.strip().startswith(('def', '"""', 'return'))]
    return len(meaningful_lines)

# Initialize a list to store line counts
line_counts = []

# Open the .jsonl file and process it line by line
with open("Dataset/HumanEval/human-eval-v2-20210705.jsonl", "r") as f:
    for line in f:
        # Parse each line as a separate JSON object
        data = json.loads(line)
        
        # Extract the canonical solution
        solution = data.get("canonical_solution", "")
        
        # Count the lines of code in the solution and store it
        loc = count_lines_of_code(solution)
        line_counts.append(loc)

# Create a stretched histogram of line counts
plt.figure(figsize=(10, 6))  # Increase width to stretch along the x-axis
plt.hist(line_counts, bins=range(1, max(line_counts)+2), edgecolor='black')
plt.title("Histogram of Line Lengths in HumanEval Solutions")
plt.xlabel("Number of Lines in Solution")
plt.ylabel("Frequency")
plt.xticks(range(1, max(line_counts)+1))

# Ensure y-axis labels are integers
plt.gca().yaxis.get_major_locator().set_params(integer=True)

plt.tight_layout()

# Save the figure
plt.savefig("HumanEval_Length_FullNumbers.png")  # Save the figure locally

# Display the plot
plt.show()
