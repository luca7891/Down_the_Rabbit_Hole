import pandas as pd

# Load full dataset
full_data_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/all_tweets.csv'
df = pd.read_csv(full_data_path)

# Randomly sample 40,000 rows
sampled_df = df.sample(n=40000, random_state=42)  # use a seed for reproducibility

# Save to new CSV
sampled_df.to_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/sampled_.csv', index=False)