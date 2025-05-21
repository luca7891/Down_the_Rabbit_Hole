import pandas as pd

# Load the dataset
df = pd.read_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv')

# Ensure required columns exist
required_cols = ['predicted_label', 'likes', 'retweets', 'replies']
if not all(col in df.columns for col in required_cols):
    raise ValueError("Dataset must contain: predicted_label, likes, retweets, replies")

# Compute variance grouped by label
variance_df = df.groupby('predicted_label')[['likes', 'retweets', 'replies']].var()

# Rename index for readability
variance_df.index = variance_df.index.map({0: 'Normal', 1: 'Extremist'})

# Display result
print("Variance of Engagement Metrics by Tweet Type:")
print(variance_df.round(2))