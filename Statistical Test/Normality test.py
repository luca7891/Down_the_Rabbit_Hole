import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# === Load dataset ===
df = pd.read_csv("/Data/LLM Data/post_musk_predictions.csv")

# === Output path ===
output_dir = "/Statistical Test/Plots"
os.makedirs(output_dir, exist_ok=True)

# === Split groups ===
normal = df[df['predicted_label'] == 0]
extremist = df[df['predicted_label'] == 1]

# === Engagement metrics ===
metrics = ['likes', 'retweets', 'replies']

# === Generate and save Q-Q plots ===
for metric in metrics:
    plt.figure(figsize=(6, 6))
    stats.probplot(normal[metric].dropna(), dist="norm", plot=plt)
    plt.title(f"Q-Q Plot (Normal) - {metric}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"qqplot_normal_{metric}.png"))
    plt.close()

    plt.figure(figsize=(6, 6))
    stats.probplot(extremist[metric].dropna(), dist="norm", plot=plt)
    plt.title(f"Q-Q Plot (Extremist) - {metric}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"qqplot_extremist_{metric}.png"))
    plt.close()