import pandas as pd
from scipy.stats import mannwhitneyu
import os

# Load your dataset
df = pd.read_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv")

# Define output path
output_path = "/Statistical Test/Mann-Whitney U Test"
os.makedirs(output_path, exist_ok=True)

# Separate the groups
extremist = df[df['predicted_label'] == 1]
normal = df[df['predicted_label'] == 0]

# Define engagement metrics
metrics = ['likes', 'replies', 'retweets']

# Perform Mann-Whitney U tests
results = []
for metric in metrics:
    u_stat, p_value = mannwhitneyu(extremist[metric], normal[metric], alternative='two-sided')
    results.append({
        "metric": metric,
        "U statistic": u_stat,
        "p-value": f"{p_value:.10f}",
        "significant (α=0.05)": "Yes" if p_value < 0.05 else "No"
    })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(output_path, "mann_whitney_results.csv"), index=False)

# Display
print(results_df)