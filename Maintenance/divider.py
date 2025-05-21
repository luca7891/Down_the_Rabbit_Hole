import pandas as pd

# Paths to your prediction files
pre_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/pre_musk_predictions.csv'
post_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv'

# Load datasets
pre_df = pd.read_csv(pre_path)
post_df = pd.read_csv(post_path)

# Filter extremist tweets (label = 1)
pre_extremist = pre_df[pre_df['predicted_label'] == 1]
post_extremist = post_df[post_df['predicted_label'] == 1]

# Save new datasets
pre_extremist.to_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/pre_musk_extremist.csv', index=False)
post_extremist.to_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Post-Musk Data/post_musk_extremist.csv', index=False)

print("Filtered extremist datasets saved.")
