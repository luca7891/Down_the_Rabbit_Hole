import pandas as pd
import matplotlib.pyplot as plt

# === Load dataset ===
post_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv'
df = pd.read_csv(post_path)

# === Ensure necessary columns exist ===
engagement_cols = ['likes', 'retweets', 'replies']
label_col = 'predicted_label'  # or 'label' if that's your column

missing = [col for col in engagement_cols + [label_col] if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

# === Group and compute means ===
grouped_means = df.groupby(label_col)[engagement_cols].mean()

# === Plotting ===
grouped_means.T.plot(kind='bar', figsize=(10, 6))
plt.title('Average Engagement Metrics: Normal vs Extremist Tweets (Post-Musk)')
plt.xlabel('Engagement Metric')
plt.ylabel('Average Count')
plt.xticks(rotation=0)
plt.legend(title='Label (0 = Normal, 1 = Extremist)')
plt.tight_layout()
plt.savefig("post_musk_engagement_comparison.png", dpi=300)
plt.show()