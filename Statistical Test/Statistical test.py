import os
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, levene
from cliffs_delta import cliffs_delta

# Load dataset
df_path = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv"
df = pd.read_csv(df_path)

# Split groups
extremist = df[df['predicted_label'] == 1]
normal = df[df['predicted_label'] == 0]

# Target metrics
metrics = ['likes', 'replies', 'retweets']
results = {
    "metric": [],
    "cliffs_delta": [],
    "cliffs_effect": [],
    "ks_statistic": [],
    "ks_pvalue": [],
    "levene_statistic": [],
    "levene_pvalue": [],
    "bootstrap_ci_lower": [],
    "bootstrap_ci_upper": [],
}


# Bootstrap CI function
def bootstrap_ci(data1, data2, n_boot=5000, ci=95):
    boot_diff = []
    for _ in range(n_boot):
        s1 = np.random.choice(data1, size=len(data1), replace=True)
        s2 = np.random.choice(data2, size=len(data2), replace=True)
        boot_diff.append(np.mean(s1) - np.mean(s2))
    lower = np.percentile(boot_diff, (100 - ci) / 2)
    upper = np.percentile(boot_diff, 100 - (100 - ci) / 2)
    return lower, upper


# Run tests
for metric in metrics:
    e_values = extremist[metric].dropna()
    n_values = normal[metric].dropna()

    delta, size = cliffs_delta(e_values, n_values)
    ks_stat, ks_p = ks_2samp(e_values, n_values)
    levene_stat, levene_p = levene(e_values, n_values)
    ci_lower, ci_upper = bootstrap_ci(e_values, n_values)

    results["metric"].append(metric)
    results["cliffs_delta"].append(delta)
    results["cliffs_effect"].append(size)
    results["ks_statistic"].append(ks_stat)
    results["ks_pvalue"].append(ks_p)
    results["levene_statistic"].append(levene_stat)
    results["levene_pvalue"].append(levene_p)
    results["bootstrap_ci_lower"].append(ci_lower)
    results["bootstrap_ci_upper"].append(ci_upper)

# Save to CSV
results_df = pd.DataFrame(results)
output_path = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Statistical Test/statistical_tests_summary.csv"
results_df.to_csv(output_path, index=False)
print(f"[+] All test results saved to: {output_path}")