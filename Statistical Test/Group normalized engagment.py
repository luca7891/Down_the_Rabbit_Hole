import pandas as pd
import matplotlib.pyplot as plt

# === Load Data ===
df = pd.read_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv')

# === Ensure required columns exist ===
required_cols = ['predicted_label', 'likes', 'retweets', 'replies']
if not all(col in df.columns for col in required_cols):
    raise ValueError("Dataset must contain: predicted_label, likes, retweets, replies")

# === Replace label values for clarity ===
df['predicted_label'] = df['predicted_label'].map({0: 'Normal', 1: 'Extremist'})

# === Group raw averages ===
grouped = df.groupby('predicted_label')[['likes', 'retweets', 'replies']].mean()

# === Normalize within each row (engagement proportion per group) ===
normalized = grouped.div(grouped.sum(axis=1), axis=0)

# === Function to plot each metric separately ===
def plot_metric(df, title_prefix, output_prefix, ylabel):
    for col in df.columns:
        ax = df[[col]].plot(kind='bar', legend=False, figsize=(6, 4))
        plt.title(f"{title_prefix} {col.capitalize()}")
        plt.ylabel(ylabel)
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f"{output_prefix}_{col}.png")
        plt.close()

# === Plot raw averages ===
plot_metric(grouped, "Average", "Plots/avg_engagement", "Average Count")

# === Plot normalized proportions ===
plot_metric(normalized, "Normalized", "Plots/normalized_engagement", "Proportion")