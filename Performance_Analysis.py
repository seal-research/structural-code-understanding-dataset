import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime
import json
from scipy.interpolate import UnivariateSpline

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
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

def analyze_model_performance(model_performances: list, buckets: list):
    results = {}

    for performance in model_performances:
        performance_df = pd.read_csv(performance)
        
        # Extract model name from the file name
        model_name = performance[:str.find(performance, "_")]
        results[model_name] = {}
        
        # Evaluate the "Actual" column to get the list
        actual_lists = performance_df['Actual'].apply(ast.literal_eval)  # Convert string to list
        
        # Calculate overall accuracy
        matches = performance_df['Matched'].value_counts()
        overall_accuracy = matches.get(True, 0) / len(performance_df['Matched']) if len(performance_df['Matched']) > 0 else 0
        results[model_name]['Overall Accuracy'] = overall_accuracy
        
        # Initialize results for each bucket
        for bin_range in buckets:
            results[model_name][bin_range] = {'accuracy': 0, 'average_similarity': 0, 'similarity_not_matched': 0}
            lower, upper = map(int, bin_range.split('-')) if '-' in bin_range else (int(bin_range[:-1]), float('inf'))
            
            # Filter valid rows for the current bucket
            bucket_rows = performance_df[(actual_lists.apply(len) >= lower) & (actual_lists.apply(len) < upper)]
            
            # Calculate accuracy for the bucket
            if not bucket_rows.empty:
                total_rows = len(bucket_rows)
                bucket_matches = bucket_rows['Matched'].value_counts()
                accurate_matches = bucket_matches.get(True, 0)

                # Ensure the total_rows is greater than 0 to avoid division by zero
                if total_rows > 0:
                    results[model_name][bin_range]['accuracy'] = accurate_matches / total_rows

                # Calculate average similarity
                similarities = bucket_rows['Distance'] * 100  # Scale from 0 to 100
                results[model_name][bin_range]['average_similarity'] = similarities.mean()
                
                # Calculate average similarity for not matched rows
                not_matched_similarities = bucket_rows[bucket_rows['Matched'] == False]['Distance'] * 100
                if not not_matched_similarities.empty:
                    results[model_name][bin_range]['similarity_not_matched'] = not_matched_similarities.mean()
    
    return results



# Example usage
# =============================================================================
# buckets = ["1-3", "3-5", "5-10", "10-20", "25-40", "40+"]
# model_performances = ['Claude_HumanEval_expandedNoReps.csv','Gemini_cleaned_humanEval_results_expandedNoReps.csv','GPT4o_expanded_NoReps_cleaned.csv']
# results = analyze_model_performance(model_performances, buckets)
# 
# # Print results
# for model, metrics in results.items():
#     print(f"Model: {model}")
#     for bucket, stats in metrics.items():
#         # Check if stats is a dictionary before accessing its keys
#         if isinstance(stats, dict):
#             accuracy = stats['accuracy']
#             average_similarity = stats['average_similarity']
#             similarity_not_matched = stats['similarity_not_matched']
#             print(f"  {bucket}: Accuracy = {accuracy:.4f}, Average Similarity = {average_similarity:.4f}, Similarity Not Matched = {similarity_not_matched:.4f}")
#     print(f"  Overall Accuracy = {metrics['Overall Accuracy']:.4f}")
# =============================================================================

def analyze_and_plot_learning_curves(jsonl_file: str, performance_files: list):
    # Load line counts from the JSONL file
    line_counts = load_line_counts(jsonl_file)

    # Initialize a dictionary to hold average accuracies
    average_accuracies = {}

    # Calculate average accuracies from the performance files
    average_accuracies = calculate_average_accuracies(performance_files, line_counts)

    # Plot the learning curves
    plot_learning_curves(average_accuracies)

def load_line_counts(jsonl_file: str):
    line_counts = {}
    
    with open(jsonl_file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            task_id = entry['task_id']
            code = entry['canonical_solution']
            line_count = code.count('\n') + 1  # Count lines
            line_counts[task_id] = line_count
            
    return line_counts

def calculate_average_accuracies(performance_files: list, line_counts: dict):
    accuracies = {name: {'line_count': [], 'trace_length': []} for name in performance_files}

    for performance_file in performance_files:
        performance_df = pd.read_csv(performance_file)

        # Calculate average accuracy based on line count and trace length
        for index, row in performance_df.iterrows():
            task_id = row['HumanEval_ID']  # Adjust this if necessary
            trace_length = len(ast.literal_eval(row['Actual']))
            accuracy = row['Matched']

            # Append accuracy to line count and trace length
            if task_id in line_counts:
                accuracies[performance_file]['line_count'].append((line_counts[task_id], accuracy))
                accuracies[performance_file]['trace_length'].append((trace_length, accuracy))

    # Average the accuracies
    average_accuracies = {}
    for name, data in accuracies.items():
        avg_line_count = pd.DataFrame(data['line_count'], columns=['Line Count', 'Accuracy']).groupby('Line Count').mean().reset_index()
        avg_trace_length = pd.DataFrame(data['trace_length'], columns=['Trace Length', 'Accuracy']).groupby('Trace Length').mean().reset_index()
        average_accuracies[name] = (avg_line_count, avg_trace_length)

    return average_accuracies

def plot_learning_curves(average_accuracies):
    plt.figure(figsize=(12, 6))

    # Create a primary x-axis for trace length
    ax1 = plt.gca()

    # Create a secondary x-axis for line count
    ax2 = ax1.twiny()

    # Iterate through models to plot both curves
    for model, (line_count_data, trace_length_data) in average_accuracies.items():
        # Sort data by line count and trace length
        line_count_data = line_count_data.sort_values('Line Count')
        trace_length_data = trace_length_data.sort_values('Trace Length')

        # Plot line count curve
        ax1.plot(line_count_data['Line Count'], line_count_data['Accuracy'], label=f'{model} (Line Count)', linestyle='-', linewidth=2)
        
        # Plot trace length curve on the secondary x-axis
        ax2.plot(trace_length_data['Trace Length'], trace_length_data['Accuracy'], label=f'{model} (Trace Length)', linestyle='--', linewidth=2)

    # Set labels and title
    ax1.set_xlabel('Line Count')
    ax1.set_ylabel('Accuracy')
    ax2.set_xlabel('Trace Length')
    plt.title('Learning Curves for Each Model')

    # Create legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    plt.grid()
    plt.show()

def analyze_and_plot_learning_curves(jsonl_file: str, performance_files: list):
    # Load line counts from the JSONL file
    line_counts = load_line_counts(jsonl_file)

    # Calculate average accuracies from the performance files
    average_accuracies = calculate_average_accuracies(performance_files, line_counts)

    # Plot the learning curves
    plot_learning_curves(average_accuracies)

def load_line_counts(jsonl_file: str):
    line_counts = {}
    
    with open(jsonl_file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            task_id = entry['task_id']
            code = entry['canonical_solution']
            line_count = code.count('\n')  # Count lines
            line_counts[task_id] = line_count
            
    return line_counts

def plot_learning_curves(average_accuracies):
    # Create a plot for Line Count
    plt.figure(figsize=(12, 6))
    for model, (line_count_data, _) in average_accuracies.items():
        # Sort data by line count
        line_count_data = line_count_data.sort_values('Line Count')

        # Extract x and y values
        line_count_x = line_count_data['Line Count']
        line_count_y = line_count_data['Accuracy']

        # Apply spline interpolation with adjusted smoothing
        spline = UnivariateSpline(line_count_x, line_count_y, s=0.05)  # Adjusted smoothing factor
        new_x_line_count = np.linspace(line_count_x.min(), line_count_x.max(), num=500)
        
        # Evaluate spline and clip values to ensure they don't go below 0
        spline_y_line_count = np.clip(spline(new_x_line_count), 0, None)
        plt.plot(new_x_line_count, spline_y_line_count, label=model[:model.find('_')], linestyle='-', linewidth=2)

    plt.xlabel('Line Count')
    plt.ylabel('Average Accuracy')
    plt.title('Accuracy by Solution Line Count')
    plt.legend()
    plt.grid()
    plt.show()

    # Create a separate plot for Trace Length
    plt.figure(figsize=(12, 6))
    for model, (_, trace_length_data) in average_accuracies.items():
        # Sort data by trace length
        trace_length_data = trace_length_data.sort_values('Trace Length')

        # Extract x and y values
        trace_length_x = trace_length_data['Trace Length']
        trace_length_y = trace_length_data['Accuracy']

        # Apply spline interpolation with adjusted smoothing
        spline = UnivariateSpline(trace_length_x, trace_length_y, s=0.2)  # Adjusted smoothing factor
        new_x_trace_length = np.linspace(trace_length_x.min(), trace_length_x.max(), num=500)
        
        # Evaluate spline and clip values to ensure they don't go below 0
        spline_y_trace_length = np.clip(spline(new_x_trace_length), 0, None)
        plt.plot(new_x_trace_length, spline_y_trace_length, label=model[:model.find('_')], linestyle='--', linewidth=2)

    plt.xlim(0, 50)  # Limit the x-axis to 50
    plt.xlabel('Trace Length')
    plt.ylabel('Average Accuracy')
    plt.title('Solution Accuracy by Trace Length')
    plt.legend()
    plt.grid()
    plt.show()
    
def print_model_statistics_with_weighted_accuracy(performance_files: list, buckets: list):
    for performance_file in performance_files:
        performance_df = pd.read_csv(performance_file)

        # Extract model name from the file name
        model_name = performance_file.split("_")[0]
        print(f"--- {model_name} ---")

        # Calculate overall accuracy
        overall_accuracy = performance_df['Matched'].mean()

        # Calculate weighted accuracy based on buckets
        total_bucket_accuracy = 0
        bucket_count = 0

        for bin_range in buckets:
            lower, upper = map(int, bin_range.split('-')) if '-' in bin_range else (int(bin_range[:-1]), float('inf'))
            
            # Filter rows within the current bucket
            bucket_rows = performance_df[
                (performance_df['Actual'].apply(lambda x: len(ast.literal_eval(x))) >= lower) &
                (performance_df['Actual'].apply(lambda x: len(ast.literal_eval(x))) < upper)
            ]
            
            if not bucket_rows.empty:
                bucket_accuracy = bucket_rows['Matched'].mean()
                total_bucket_accuracy += bucket_accuracy
                bucket_count += 1

        # Compute weighted accuracy as average across non-empty buckets
        weighted_accuracy = total_bucket_accuracy / bucket_count if bucket_count > 0 else 0

        # Calculate similarity metrics
        average_similarity = (performance_df['Distance'] * 100).mean()
        similarity_not_matched = (performance_df[performance_df['Matched'] == False]['Distance'] * 100).mean()

        # Print results
        print("\nOverall Statistics:")
        print(f"  Overall Accuracy: {overall_accuracy:.2%}")
        print(f"  Weighted Accuracy: {weighted_accuracy:.2%}")
        print(f"  Average Similarity: {average_similarity:.2f}")
        print(f"  Similarity for Incorrect Cases: {similarity_not_matched:.2f}")
        print()  # Blank line for separation
        
def analyze_model_performance_with_nonlinear_weights(model_performances: list):
    overall_results = {}

    for performance in model_performances:
        performance_df = pd.read_csv(performance)

        # Extract model name from the file name
        model_name = performance[:str.find(performance, "_")]
        
        # Evaluate the "Actual" column to get the list
        actual_lists = performance_df['Actual'].apply(ast.literal_eval)  # Convert string to list
        
        # Calculate average accuracy and similarity per trace length
        grouped_data = performance_df.groupby(performance_df['Actual'].apply(lambda x: len(ast.literal_eval(x)))).agg(
            Average_Accuracy=('Matched', 'mean'),
            Average_Similarity=('Distance', lambda x: (x * 100).mean())  # Scale similarity to 0-100
        ).reset_index()

        # Initialize totals for weighted calculations
        total_weighted_accuracy = 0
        total_weighted_similarity = 0
        total_weight = 0
        total_weighted_incorrect_similarity = 0  # For wrong predictions

        for index, row in grouped_data.iterrows():
            trace_length = row['Actual']  # Trace length
            
            # Skip rows where the trace length is more than 50
            if trace_length > 50:
                continue
            
            weight = trace_length ** 0.5  # Square root weight
            accuracy = row['Average_Accuracy']
            similarity = row['Average_Similarity']

            # Calculate weighted accuracy
            total_weighted_accuracy += accuracy * weight

            # Weighted similarity for all predictions
            total_weighted_similarity += similarity * weight
            
            # Only calculate weighted similarity for wrong predictions
            if accuracy < 1.0:  # Check if the prediction is wrong
                total_weighted_incorrect_similarity += similarity * weight

            total_weight += weight

        # Calculate overall weighted averages
        overall_accuracy = total_weighted_accuracy / total_weight if total_weight > 0 else 0
        overall_similarity = total_weighted_similarity / total_weight if total_weight > 0 else 0
        overall_incorrect_similarity = total_weighted_incorrect_similarity / total_weight if total_weight > 0 else 0
        
        # Store results
        overall_results[model_name] = {
            'Overall Weighted Accuracy': overall_accuracy,  # Convert to percentage
            'Overall Weighted Similarity': overall_similarity,
            'Overall Weighted Incorrect Similarity': overall_incorrect_similarity
        }
    
    return overall_results

def print_weighted_accuracy_results(model_performances: list):
    results = analyze_model_performance_with_nonlinear_weights(model_performances)
    
    print(f"{'Model':<20} {'Overall Weighted Accuracy':<30} {'Overall Weighted Similarity':<30} {'Overall Weighted Incorrect Similarity'}")
    print("-" * 110)
    for model, metrics in results.items():
        overall_accuracy_percent = metrics['Overall Weighted Accuracy']  # Already in percentage
        overall_similarity = metrics['Overall Weighted Similarity']
        overall_incorrect_similarity = metrics['Overall Weighted Incorrect Similarity']
        print(f"{model:<20} {overall_accuracy_percent:<30.4f} {overall_similarity:<30.4f} {overall_incorrect_similarity:.4f}")

# Example usage
performance_files = [
    'Claude3.5-Sonnet_HumanEval_expandedNoReps.csv', 
    'Gemini1.5Pro_cleaned_humanEval_results_expandedNoReps.csv', 
    'GPT4o_expanded_NoReps_cleaned.csv'
]
print(analyze_model_performance(performance_files,["1-3", "3-5", "5-10", "10-25", "25-40", "40+"]))
#analyze_and_plot_learning_curves(jsonl_file, performance_files)


    
#generate_accuracy_graph(performance_files)