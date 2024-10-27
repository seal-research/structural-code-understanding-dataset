import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import ast  # To safely evaluate the string representation of lists

def generate_accuracy_graph(model_performances: list, min_length: int = 0, save=False):
    models = []
    accuracies = []
    
    for performance in model_performances:
        performance_df = pd.read_csv(performance)
        
        # Extract model name from the file name
        model_name = performance[:str.find(performance, "_")]
        models.append(model_name)

        # Evaluate the "Actual" column to get the list and filter based on min_length
        actual_lists = performance_df['Actual'].apply(ast.literal_eval)  # Convert string to list
        valid_rows = performance_df[actual_lists.apply(len) >= min_length]  # Filter based on length
        
        # Calculate accuracy based on valid rows
        matches = valid_rows['Matched'].value_counts()
        if True in matches:
            accuracies.append(matches[True] / len(valid_rows['Matched']))
        else:
            accuracies.append(0)  # Handle case where there are no True matches
        
    # Set figure size
    plt.figure(figsize=(8, 6))
    
    # Adjust y-axis limit to provide space above the tallest bar
    plt.ylim(0, max(accuracies) + 0.05)
    
    # Create a bar chart
    plt.bar(models, accuracies, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    # Add labels and title
    plt.xlabel('Models')
    plt.ylabel('Accuracy')
    plt.title(f'Model Accuracy Comparison (Minimum Trace length: {min_length})')
    
    # Display percentage above each bar
    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 0.01, f"{acc*100:.1f}%", ha='center', fontsize=12)
    
    # Show gridlines
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot if requested
    if save:
        date_str = datetime.now().strftime('%Y-%m-%d')
        plt.savefig(f'Visualizations/model_accuracy_minlength{min_length}_{date_str}_Reps.png', format='png', dpi=300)
    
    # Display the plot
    plt.show()

    
generate_accuracy_graph(['Claude_HumanEval_expandedNoReps.csv','Gemini_cleaned_humanEval_results_expandedNoReps.csv','GPT4o_expanded_NoReps_cleaned.csv'], min_length=25, save=True)