# StructuralCodeUnderstanding
In this repository I investigate the capabilities of selected Large Language Models on understanding Structural Code Execution.

This repository contains the different scripts I have used for generating and eliciting traces from Java and Python programs.

Generally, the root contains the first experiments of the different LLMs on HumanEval data. Under Dataset, I have saved the different short programs according to their respective functionality. In addition, this folder contains the majority of traces. The final used traces with the last evaluation settings are also in this directory, under Evaluation and sorted by Model. Complex generally refers to the three advanced topics of OOP, Recursion and Concurrency. 

Models contains specific configuration files for different language models to run locally. Visualizations contains a number of basic visualizations of the different findings.

A basic overview of the findings on HumanEval can be found below:

## Task Performance Overview

The table below summarizes the performance of different models across tasks, evaluated using various metrics. Metrics are grouped under two settings: **\ccot** and **\basic**.

| **Task ID**          | **Acc Hard (%)** | **Acc Mean (%)** | **\ovsimshort** | **False \ovsimshort** | **Acc Hard (%)** | **Acc Mean (%)** | **\ovsimshort** | **False \ovsimshort** |
|-----------------------|------------------|------------------|-----------------|-----------------------|------------------|------------------|-----------------|-----------------------|
| **Gemini1.5-Pro 002** | 47.2            | 66.2            | 0.88           | 0.37                 | 47.0            | 65.7            | 0.89           | 0.37                 |
| **Claude3.5-Sonnet**  | 41.0            | 61.6            | 0.87           | 0.43                 | 41.0            | 58.7            | 0.88           | 0.44                 |
| **GPT4o**             | 16.8            | 39.4            | 0.75           | 0.50                 | 21.2            | 38.8            | 0.75           | 0.50                 |
| **Codestral 22B**     | 9.3             | 25.0            | 0.71           | 0.57                 | 3.1             | 17.8            | 0.66           | 0.59                 |
| **LLama3.1 8B**       | 1.9             | 12.6            | 0.56           | 0.51                 | 0.6             | 10.4            | 0.53           | 0.48                 |

### Explanation of Metrics:
- **Acc Hard (%)**: Accuracy for tasks that are traced correctly across all tests as a percentage.
- **Acc Mean (%)**: Mean accuracy across all tests of all examples as a percentage.
- **\ovsimshort**: Average overall similarity score between predictions and ground truth.
- **False \ovsimshort**: Similarity score based only on incorrect predictions.

### Notes:
- Metrics under **\ccot** and **\basic** represent two different evaluation settings due to the used prompt.
- Values are reported for each task ID, which represents a specific configuration or evaluation scenario.
