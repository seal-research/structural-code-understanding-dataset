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
import traceback
import difflib

HE_difficulty = {
    0: [
        "014_all_prefixes",
        "032_find_zero",
        "076_is_simple_power",
        "084_n_digits_in_binary",
        "089_encrypt",
        "108_count_nums",
        "124_valid_date",
        "127_intersection",
        "129_min_path",
        "130_tri",
        "132_is_nested",
        "134_check_if_last_char_is_a_letter",
        "145_order_by_points",
        "151_double_the_difference",
        "161_reverse_string",
        "163_generate_integers",
    ],
    1: [
        "009_rolling_max",
        "083_starts_one_ends",
        "093_encode_swap",
        "095_check_dict_case",
        "113_odd_count",
        "119_match_parens",
        "125_split_words",
        "140_fix_spaces",
    ],
    2: [
        "074_total_match",
        "075_is_multiply_prime",
        "106_f",
        "115_max_fill",
        "122_add_elements",
        "137_compare_one",
        "141_file_name_check",
        "160_do_algebra",
    ],
    3: [
        "010_palindrome_with_append",
        "041_car_race_collision",
        "064_vowels_count",
        "086_anti_shuffle",
        "096_count_up_to",
        "118_get_closest_vowel",
        "123_get_odd_collatz",
        "135_can_arrange",
    ],
    4: [
        "001_separate_paren_groups",
        "026_remove_duplicates",
        "039_prime_fib",
        "049_modp",
        "087_get_row",
        "099_closest_integer",
        "100_make_a_pile",
        "117_select_words",
        "138_is_equal_to_sum_even",
        "139_special_factorial",
        "155_even_odd_count",
    ],
    5: [
        "006_parse_nested_parens",
        "017_parse_music",
        "025_factorize",
        "046_fib4",
        "054_same_chars",
        "062_derivative",
        "065_circular_shift",
        "070_strange_sort_list",
        "091_is_bored",
        "109_move_one_ball",
        "111_histogram",
        "131_count_digits",
        "154_cycpattern_check",
    ],
    6: [
        "033_sort_third",
        "047_median",
        "081_numerical_letter_grade",
        "092_any_int",
        "102_choose_num",
        "121_sum_odd_at_odd",
        "146_specialFilter",
    ],
    7: [
        "004_mean_absolute_deviation",
        "059_largest_prime_factor",
        "144_simplify",
        "153_strongest_extension",
    ],
    8: [
        "005_intersperse",
        "019_sort_numbers",
        "036_fizz_buzz",
        "057_monotonic",
        "067_fruit_distribution",
        "069_search",
        "077_iscube",
        "078_hex_key",
        "079_decimal_to_binary",
        "085_add_even_eles_at_odd_inds",
        "097_multiply_unit_digits",
        "116_sort_array",
        "128_prod_signs",
        "156_int_to_mini_roman",
    ],
    9: [
        "027_flip_case",
        "037_sort_even",
        "044_change_base",
        "066_digitSum",
        "090_next_smallest",
        "104_unique_digits",
        "107_even_odd_palindrome",
        "110_exchange",
        "120_top_k",
        "126_is_sorted",
        "143_words_in_sentence",
        "148_bf",
        "150_x_or_y",
        "162_string_to_md5",
    ],
    10: [
        "000_has_close_elements",
        "011_string_xor",
        "018_how_many_times",
        "045_triangle_area",
        "051_remove_vowels",
        "073_smallest_change",
        "133_sum_squares_round",
        "159_eat",
    ],
    11: [
        "020_find_closest_elements",
        "040_triples_sum_to_zero",
        "043_pairs_sum_to_zero",
        "048_is_palindrome",
        "050_decode_shift",
        "060_sum_to_n",
        "082_prime_length",
        "094_skjkasdkd",
        "112_reverse_delete",
        "114_min_sub_array_sum",
        "157_right_angle_triangle",
    ],
    12: [
        "016_count_distinct_characters",
        "022_filter_integers",
        "024_largest_divisor",
        "030_get_positive",
        "056_correct_angle_bracketing",
        "061_correct_bracketing",
        "063_fibfib",
        "088_sort_array_based_on_head_tail",
        "098_count_upper",
        "103_rounded_avg",
        "142_sum_squares",
        "147_get_max_triples",
        "149_sorted_list_sum",
    ],
    13: [
        "015_string_sequence",
        "034_unique_elements",
        "038_decode_cyclic",
        "042_incr_list",
        "058_common",
        "068_pluck",
        "071_triangle_area3",
        "080_is_happy",
        "101_words_string",
        "105_by_length",
        "136_largest_smallest_integers",
        "152_compare",
        "158_find_max",
    ],
    14: [
        "002_truncate_number",
        "003_below_zero",
        "007_filter_by_substring",
        "013_greatest_common_divisor",
        "031_is_prime",
        "053_add",
        "072_will_it_fly",
    ],
    15: [
        "008_sum_product",
        "012_longest",
        "021_rescale_to_unit",
        "023_strlen",
        "028_concatenate",
        "029_filter_by_prefix",
        "035_max_element",
        "052_below_threshold",
        "055_fib",
    ],
}

def calculate_match_concurrency(actual, predicted):
    """
    Calculate exact match between two lists with special handling for parenthesized content.
    When parentheses overlap in position, only check if elements within them match regardless of order.
    
    Args:
        actual: List or string representation of list containing the actual values
        predicted: List or string representation of list containing the predicted values
        
    Returns:
        bool: True if lists match according to the criteria, False otherwise
    """
    def parse_list(list_input):
        """Convert string representation of list to actual list if needed."""
        if isinstance(list_input, str):
            try:
                return ast.literal_eval(list_input)
            except:
                return list_input
        return list_input
    
    def find_parentheses_sections(lst):
        """Find the start and end indices of parenthesized sections and their content."""
        start_idx = -1
        sections = []
        
        for i, item in enumerate(lst):
            if item == '(':
                start_idx = i
            elif item == ')' and start_idx != -1:
                content = lst[start_idx + 1:i]
                sections.append({
                    'start': start_idx,
                    'end': i,
                    'content': content
                })
                start_idx = -1
        
        return sections
    
    def compare_sections(actual_list, predicted_list):
        """Compare two lists with special handling for parenthesized sections."""
        if len(actual_list) != len(predicted_list):
            return False
            
        actual_sections = find_parentheses_sections(actual_list)
        predicted_sections = find_parentheses_sections(predicted_list)
        
        # If one has parentheses and the other doesn't, require exact match
        if bool(actual_sections) != bool(predicted_sections):
            return actual_list == predicted_list
        
        # If neither has parentheses, require exact match
        if not actual_sections:
            return actual_list == predicted_list
            
        # Track which positions we've handled
        handled_positions = set()
        
        # Check each predicted section against actual sections
        for pred_section in predicted_sections:
            section_matched = False
            pred_start, pred_end = pred_section['start'], pred_section['end']
            
            # Find matching actual section
            for actual_section in actual_sections:
                act_start, act_end = actual_section['start'], actual_section['end']
                
                # Check if positions overlap (allowing for ±1 position difference)
                if abs(pred_start - act_start) <= 1 and abs(pred_end - act_end) <= 1:
                    # Convert content to sets for order-independent comparison
                    actual_content = set(str(x) for x in actual_section['content'])
                    predicted_content = set(str(x) for x in pred_section['content'])
                    
                    if actual_content == predicted_content:
                        # Mark all positions in this section as handled
                        for i in range(min(act_start, pred_start), max(act_end, pred_end) + 1):
                            handled_positions.add(i)
                        section_matched = True
                        break
            
            if not section_matched:
                return False
        
        # Check non-parentheses parts
        for i in range(len(actual_list)):
            if i not in handled_positions:
                if i >= len(predicted_list) or actual_list[i] != predicted_list[i]:
                    return False
                
        return True
    
    # Parse input lists
    actual_list = parse_list(actual)
    predicted_list = parse_list(predicted)
    
    return compare_sections(actual_list, predicted_list)

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
#buckets = ["1-3", "3-5", "5-10", "10-25", "25-40", "40+"]
#model_performances = ['../../Results/LLama/70B/HumanEval/results_HumanEval_llama-3.1-70b_NoReps.csv']
#results = analyze_model_performance(model_performances, buckets)
 
 # Print results
#for model, metrics in results.items():
#    print(f"Model: {model}")
#    for bucket, stats in metrics.items():
#        # Check if stats is a dictionary before accessing its keys
#        if isinstance(stats, dict):
#            accuracy = stats['accuracy']
#            average_similarity = stats['average_similarity']
#            similarity_not_matched = stats['similarity_not_matched']
#            print(f"  {bucket}: Accuracy = {accuracy:.4f}, Average Similarity = {average_similarity:.4f}, Similarity Not Matched = {similarity_not_matched:.4f}")
#    print(f"  Overall Accuracy = {metrics['Overall Accuracy']:.4f}")
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
        # Extract only the last part of the model name from the path
        model_name = os.path.basename(model)

        # Sort data by line count and trace length
        line_count_data = line_count_data.sort_values('Line Count')
        trace_length_data = trace_length_data.sort_values('Trace Length')

        # Plot line count curve
        ax1.plot(line_count_data['Line Count'], line_count_data['Accuracy'], label=f'{model_name} (Line Count)', linestyle='-', linewidth=2)
        
        # Plot trace length curve on the secondary x-axis
        ax2.plot(trace_length_data['Trace Length'], trace_length_data['Accuracy'], label=f'{model_name} (Trace Length)', linestyle='--', linewidth=2)

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
#performance_files = [
#    'Dataset/Evaluation/Gemini/HumanEval/Gemini_HumanEval_CoT_T0_NoReps.csv', 
#    'Dataset/Evaluation/Claude/HumanEval/HumanEval_CoT_T0NoReps.csv', 
#    'Dataset/Evaluation/GPT/HumanEval/HumanEval_CoT_T0_NoReps.csv',
#    'Dataset/Evaluation/Codestral/HumanEval/Codestral_HumanEval_cot_T0_NoReps.csv',
#    'Dataset/Evaluation/LLama/8B/HumanEval/results_HumanEval_llama-3.1-8b_NoReps.csv'
#]
#print(analyze_model_performance(performance_files,["1-3", "3-5", "5-10", "10-25", "25-40", "40+"]))
#analyze_and_plot_learning_curves("Dataset/HumanEval/human-eval-v2-20210705.jsonl", ['Dataset/Evaluation/Gemini/HumanEval/Gemini_HumanEval_CoT_T0_NoReps.csv', 'Dataset/Evaluation/Gemini/HumanEval/HumanEval_CoT_T1_NoReps.csv', 'Dataset/Evaluation/Gemini/HumanEval/Gemini_HumanEval_Trace_Direct_T0_NoReps.csv', 'Dataset/Evaluation/Gemini/HumanEval/HumanEval_Direct_T1_NoReps.csv'])
import os
import pandas as pd

def evaluate_performance(directory_path):
    file_task_performance = {}  # Per-file task-level performance
    file_overall_performance = {}  # Per-file overall performance

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Check if 'HumanEval_ID' exists in the dataframe
            if 'HumanEval_ID' in df.columns:
                task_column = 'HumanEval_ID'
            else:
                task_column = 'Filename'
            
            # Group by task ID (either 'HumanEval_ID' or 'Filename')
            grouped = df.groupby(task_column)

            # Initialize performance metrics for this file
            task_performance = {}
            overall_matched = 0
            overall_distance = 0
            overall_incorrect_distance = 0
            total_tasks = 0

            # Process each task group
            for task_id, group in grouped:
                # Aggregate 'Matched' and 'Distance' values
                matched_count = group['Matched'].sum()  # True = 1, False = 0
                distance_avg = group['Distance'].mean()

                # Calculate the distance for incorrect tasks
                incorrect_tasks = group[group['Matched'] == 0]
                incorrect_distance_avg = incorrect_tasks['Distance'].mean() if not incorrect_tasks.empty else 0

                # Store task-level performance
                task_performance[task_id] = {
                    'Matched': matched_count / len(group['Matched']),
                    'Distance': distance_avg,
                    'Incorrect_Distance': incorrect_distance_avg,
                    'Tests': len(group['Matched'])
                }

                # Update overall performance for this file
                overall_matched += matched_count / len(group['Matched'])
                overall_distance += distance_avg
                overall_incorrect_distance += incorrect_distance_avg
                total_tasks += 1

            # Calculate overall performance for this file
            overall_performance = {
                'Overall_Matched': overall_matched / total_tasks if total_tasks else 0,
                'Overall_Avg_Distance': overall_distance / total_tasks if total_tasks else 0,
                'Overall_Incorrect_Avg_Distance': overall_incorrect_distance / total_tasks if total_tasks else 0
            }

            # Store results keyed by filename
            file_task_performance[filename] = task_performance
            file_overall_performance[filename] = overall_performance

    return file_task_performance, file_overall_performance
#task_performance, overall_performance = evaluate_performance('../../Results/QwenCoder/32B/HumanEval/')

def evaluate_complex_performance(directory_path):
    overall_matched = 0
    overall_distance = 0
    total_test_cases = 0
    category_performance = {}

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            
            # Read the CSV file
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            # Check if the directory path contains 'complex' to determine format
            if 'complex' in directory_path.lower():
                print(f"Processing complex file: {file_path}")
                
                # Ensure columns exist
                if 'Matched' not in df.columns or 'Distance' not in df.columns or 'Category' not in df.columns:
                    print(f"Missing columns in {filename}")
                    continue
                
                # Add an index as a suffix to Filenames to differentiate test cases
                df['Filename'] = df['Filename'] + df.groupby('Filename').cumcount().astype(str)
                
                # Group by 'Category'
                grouped = df.groupby('Category')
                print(f"Grouped by 'Category' in {filename}, found {len(grouped)} categories")

                # Process each category group
                for category, group in grouped:
                    print(f"Processing category: {category}, Group size: {len(group)}")
                    # Ensure correct types
                    group['Matched'] = group['Matched'].astype(bool)
                    group['Distance'] = pd.to_numeric(group['Distance'], errors='coerce')

                    # Aggregate 'Matched' and 'Distance' values
                    matched_count = group['Matched'].sum()  # True = 1, False = 0
                    distance_avg = group['Distance'].mean()

                    # Store category-level performance
                    if category not in category_performance:
                        category_performance[category] = {
                            'Matched': 0,
                            'Distance': 0,
                            'Count': 0
                        }

                    # Update category-level performance
                    category_performance[category]['Matched'] += matched_count
                    category_performance[category]['Distance'] += distance_avg
                    category_performance[category]['Count'] += 1

                    # Update overall performance
                    overall_matched += matched_count
                    overall_distance += distance_avg
                    total_test_cases += 1

    # Calculate overall statistics
    overall_performance = {
        'Overall_Matched': overall_matched,
        'Overall_Avg_Distance': overall_distance / total_test_cases if total_test_cases else 0
    }

    # Aggregate category statistics
    for category, performance in category_performance.items():
        performance['Avg_Distance'] = performance['Distance'] / performance['Count'] if performance['Count'] else 0

    return category_performance, overall_performance

def calculate_distance(actual, predicted):
    """Calculate similarity between two lists of lines."""
    actual_str = ','.join(map(str, actual))
    predicted_str = ','.join(map(str, predicted))
    sequence = difflib.SequenceMatcher(a=actual_str, b=predicted_str)
    return sequence.ratio()  # Similarity ratio

def calculate_distance_concurrency(actual, predicted):
    """
    Calculate similarity between two lists with special handling for parenthesized content.
    Handles mismatched parentheses content gracefully.

    Args:
        actual: List or string representation of list containing the actual values
        predicted: List or string representation of list containing the predicted values

    Returns:
        float: Average similarity ratio between corresponding parts
    """
    def parse_list(list_input):
        """Parse string representation of a list into a Python list, handling parentheses as strings."""
        if isinstance(list_input, str):
            try:
                # Handle parentheses by treating them as strings
                list_input = list_input.replace("(", "'('").replace(")", "')'")
                return ast.literal_eval(list_input)
            except Exception as e:
                print(f"Failed to parse list: {list_input}, Error: {e}")
                return []
        return list_input

    def extract_parentheses_content(lst):
        """Extract content within parentheses and its position."""
        start_idx = -1
        for i, item in enumerate(lst):
            if item == "'('":
                start_idx = i
            elif item == "')'" and start_idx != -1:
                return {
                    'start': start_idx,
                    'end': i,
                    'content': lst[start_idx + 1:i]
                }
        return {'start': -1, 'end': -1, 'content': []}

    def get_similarity(list1, list2):
        """Calculate similarity between two lists using SequenceMatcher."""
        str1 = ','.join(map(str, list1))
        str2 = ','.join(map(str, list2))
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    # Parse input lists
    actual_list = parse_list(actual)
    predicted_list = parse_list(predicted)

    # Extract parentheses sections
    actual_section = extract_parentheses_content(actual_list)
    predicted_section = extract_parentheses_content(predicted_list)

    # Split lists into parts
    before_actual = actual_list[:actual_section['start']] if actual_section['start'] != -1 else actual_list
    before_predicted = predicted_list[:predicted_section['start']] if predicted_section['start'] != -1 else predicted_list

    parentheses_actual = sorted(map(str, actual_section['content']))
    parentheses_predicted = sorted(map(str, predicted_section['content']))

    after_actual = actual_list[actual_section['end'] + 1:] if actual_section['end'] != -1 else []
    after_predicted = predicted_list[predicted_section['end'] + 1:] if predicted_section['end'] != -1 else []

    # Handle mismatched content outside parentheses ranges
    if actual_section['start'] == -1 or predicted_section['start'] == -1:
        # No valid parentheses content in one of the lists
        return get_similarity(actual_list, predicted_list)

    # Ensure all parts are lists before appending
    before_actual = list(before_actual)
    before_predicted = list(before_predicted)
    after_actual = list(after_actual)
    after_predicted = list(after_predicted)

    # Calculate similarities for each part
    before_similarity = get_similarity(before_actual, before_predicted)
    parentheses_similarity = get_similarity(parentheses_actual, parentheses_predicted)
    after_similarity = get_similarity(after_actual, after_predicted)

    # Return average similarity
    return (before_similarity + parentheses_similarity + after_similarity) / 3

task_performance, overall_performance = evaluate_performance('../../Results/QwenCoder/32B/Complex')

def task_performance_plot(task_performance):
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Convert the dictionary into a DataFrame
    table_data = [{'Task': task, **values} for task, values in task_performance.items()]
    df = pd.DataFrame(table_data)
    
    # Step 2: Define Buckets
    bins = [0, 0.25, 0.5, 0.75, 1.0, 1.01]  # Upper limit for 1.0 bucket
    labels = ['0-25%', '25-50%', '50-75%', '75-100%', '100%']
    df['Matched Bucket'] = pd.cut(df['Matched'], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # Step 3: Calculate Fraction of Tasks and Mean Similarity per Bucket
    bucket_counts = df['Matched Bucket'].value_counts(normalize=True, sort=False)  # Fraction of tasks
    bucket_counts = bucket_counts.reindex(labels, fill_value=0)  # Ensure all buckets are represented
    
    mean_similarity = df.groupby('Matched Bucket')['Matched'].mean()  # Mean similarity
    mean_similarity = mean_similarity.reindex(labels, fill_value=0)  # Ensure all buckets are represented
    
    # Step 4: Plot the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(labels))  # X-axis positions
    width = 0.35  # Width of the bars
    
    # Plot Fraction of Tasks
    ax.bar([p - width/2 for p in x], bucket_counts.values, width=width, color='royalblue', label='Fraction of Tasks')
    
    # Plot Mean Similarit
    ax.bar([p + width/2 for p in x], mean_similarity.values, width=width, color='orange', label='Mean Similarity')
    
    # Add labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Average Accuracy on Task')
    ax.set_ylabel('Val')
    ax.set_title('Performance on HumanEval Tasks Gemini1.5 Pro -002 using Direct Prompting')
    ax.legend()
    
    # Add value labels on top of each bar
    for i, v in enumerate(bucket_counts.values):
        ax.text(i - width/2, v + 0.01, f"{v:.2f}", ha='center', fontsize=9)
    for i, v in enumerate(mean_similarity.values):
        ax.text(i + width/2, v + 0.01, f"{v:.2f}", ha='center', fontsize=9)
    
    # Step 5: Show the plot
    plt.tight_layout()
    plt.show()
    
def compute_metrics(file_path):
    """
    Computes average accuracy and similarity for the first test case of each HumanEval_ID in a file.
    """
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Group by 'HumanEval_ID' and select the first test for each unique 'HumanEval_ID'
    first_tests = data.groupby('HumanEval_ID').first()
    
    # Calculate average accuracy (mean of 'Matched') and average similarity
    average_accuracy = first_tests['Matched'].mean()
    average_similarity = first_tests['Distance'].mean()
    
    return average_accuracy, average_similarity

def process_directory(directory_path):
    """
    Processes all files in the given directory and computes accuracy and similarity for each.
    """
    results = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(directory_path, filename)
            accuracy, similarity = compute_metrics(file_path)
            results.append({'File': filename, 'Accuracy': accuracy, 'Similarity': similarity})
    
    # Convert the results into a DataFrame
    results_df = pd.DataFrame(results)
    return results_df

def safe_literal_eval(val):
    """
    Safely evaluate a string representation of a list,
    with additional error handling and logging.
    """
    try:
        # First, ensure it's a string
        if not isinstance(val, str):
            val = str(val)
        
        # Strip leading/trailing whitespace
        val = val.strip()
        
        # Ensure it looks like a list-like string
        if not (val.startswith('[') and val.endswith(']')):
            val = f'[{val}]'
        
        # Use ast.literal_eval with error handling
        return ast.literal_eval(val)
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"Error parsing value: {val}")
        print(f"Error details: {traceback.format_exc()}")
        return []  # Return empty list on parsing failure


def eliminate_repetitions_and_compute_distances_for_directory(input_directory: str):
    """
    Processes all CSV files in the given directory, filters entries with consecutive duplicate lines in 'Actual',
    eliminates those duplicates, recomputes 'Matched' and 'Distance', and writes outputs to new CSVs with '_NoReps' suffix.
    Skips processing if the '_NoReps' file already exists and ensures '_NoReps' files are not processed.
    For files containing "concurrency" in their names, it uses calculate_match_concurrency instead of the normal equivalence check.
    """
    def eliminate_consecutive_duplicates(lines):
        if not lines:
            return "[]"
        cleaned_lines = [lines[0]]
        for line in lines[1:]:
            if line != cleaned_lines[-1]:
                cleaned_lines.append(line)
        return '[' + ', '.join(map(str, cleaned_lines)) + ']'

    for file_name in os.listdir(input_directory):
        # Skip if the file is a '_NoReps.csv' file or does not end with '.csv'
        if file_name.endswith('_NoReps.csv') or not file_name.endswith('.csv'):
            continue

        input_path = os.path.join(input_directory, file_name)
        output_path = os.path.join(input_directory, file_name.replace('.csv', '_NoReps.csv'))

        # Skip processing if the _NoReps file already exists
        if os.path.exists(output_path):
            print(f"Skipping {file_name} as {output_path} already exists.")
            continue

        try:
            # Read the CSV file
            new_results_df = pd.read_csv(input_path)

            filtered_results = []

            for index, entry in new_results_df.iterrows():
                try:
                    # Safely parse Actual lines
                    actual_lines_str = str(entry['Actual'])
                    actual_lines = safe_literal_eval(actual_lines_str)

                    # Check for repetitions
                    has_repetitions = len(actual_lines) != len(set(actual_lines)) or actual_lines != list(dict.fromkeys(actual_lines))
                    cleaned_actual_lines_str = eliminate_consecutive_duplicates(actual_lines) if has_repetitions else actual_lines_str

                    # Determine which distance and match functions to use
                    distance_function = calculate_distance_concurrency if "concurrency" in file_name.lower() else calculate_distance
                    match_function = calculate_match_concurrency if "concurrency" in file_name.lower() else lambda a, p: a == p

                    # Prepare the row based on file type
                    if "humaneval" in file_name.lower():
                        row = {
                            'HumanEval_ID': entry.get('HumanEval_ID', ''),
                            'Name': entry.get('Name', ''),
                            'FunctionCall': entry.get('FunctionCall', ''),
                            'Predicted': str(entry.get('Predicted', '')),
                            'Actual': cleaned_actual_lines_str,
                            'Matched': str(match_function(cleaned_actual_lines_str, str(entry.get('Predicted', '')))),
                            'Distance': distance_function(cleaned_actual_lines_str, str(entry.get('Predicted', '')))
                        }
                    else:
                        row = {
                            'Filename': entry.get('Filename', ''),
                            'Category': entry.get('Category', ''),
                            'Predicted': str(entry.get('Predicted', '')),
                            'Actual': cleaned_actual_lines_str,
                            'Matched': str(match_function(cleaned_actual_lines_str, str(entry.get('Predicted', '')))),
                            'Distance': distance_function(cleaned_actual_lines_str, str(entry.get('Predicted', '')))
                        }

                    filtered_results.append(row)

                except Exception as e:
                    print(f"Error processing entry at index {index} in file {file_name}: {e}")
                    print(f"Entry details: {entry}")
                    print(f"Traceback: {traceback.format_exc()}")

            # Write the filtered results to a new CSV file
            filtered_results_df = pd.DataFrame(filtered_results)
            filtered_results_df.to_csv(output_path, index=False)
            print(f"Processed file saved at {output_path}")

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
            print(f"Traceback: {traceback.format_exc()}")

def analyze_accuracy_by_task(directory_path: str, min_length: int = 0):
    """
    Calculate and print task-level accuracy by grouping rows by 'HumanEval_ID'.
    Accuracy is the percentage of tasks where all rows for a given task are 'Matched'.
    
    Args:
        directory_path (str): Path to the directory containing performance CSV files.
        min_length (int): Minimum trace length for filtering.
    """
    print(f"Analyzing task-level accuracy (Min Trace Length: {min_length})...\n")
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            performance_df = pd.read_csv(file_path)

            # Evaluate "Actual" column and filter by trace length
            performance_df['Actual'] = performance_df['Actual'].apply(ast.literal_eval)
            performance_df = performance_df[performance_df['Actual'].apply(len) >= min_length]

            # Group by 'HumanEval_ID' and calculate task-level accuracy
            task_grouped = performance_df.groupby('HumanEval_ID')
            task_accuracy = task_grouped['Matched'].all().mean()  # All rows for a task must be matched
            
            # Print results for this file
            print(f"File: {filename}")
            print(f"  Total Tasks: {len(task_grouped)}")
            print(f"  Task-Level Accuracy: {task_accuracy * 100:.2f}%\n")
            
def fix_unclosed_lists_in_csv(input_csv_path: str, output_csv_path: str = None):
    """
    Reads a CSV file and ensures all entries in the 'Predicted' column are properly closed lists.
    Handles cases where the list is missing a closing bracket or ends with a comma.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_csv_path (str): Path to save the fixed CSV. If None, modifies the input file.
    """
    if output_csv_path is None:
        output_csv_path = input_csv_path
        
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    
    # Function to fix a single list string
    def fix_list_string(val):
        if not isinstance(val, str):
            return val
            
        # Remove trailing whitespace
        val = val.rstrip()
        
        # If empty or not starting with [, return as is
        if not val or not val.startswith('['):
            return val
            
        # Remove trailing comma if present
        if val.rstrip().endswith(','):
            val = val.rstrip().rstrip(',')
            
        # Add closing bracket if missing
        if not val.rstrip().endswith(']'):
            val = val + ']'
            
        return val
    
    # Fix the Predicted column
    df['Predicted'] = df['Predicted'].apply(fix_list_string)
    
    # Save the fixed CSV
    df.to_csv(output_csv_path, index=False)
    
    print(f"Fixed CSV saved to {output_csv_path}")
    
    # Return count of fixed entries for verification
    return len(df[df['Predicted'].str.endswith(']', na=False)])



    
#generate_accuracy_graph(performance_files)