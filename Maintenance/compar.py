import pandas as pd
import matplotlib.pyplot as plt

# Define paths
pre_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/pre_musk_predictions.csv'
post_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv'

# Load datasets
pre_df = pd.read_csv(pre_path)
post_df = pd.read_csv(post_path)

# Count extremist tweets only (label = 1)
pre_extremist_count = (pre_df['predicted_label'] == 1).sum()
post_extremist_count = (post_df['predicted_label'] == 1).sum()

# Total tweets in each set
pre_total = len(pre_df)
post_total = len(post_df)

# Compute percentage
pre_percent = pre_extremist_count / pre_total * 100
post_percent = post_extremist_count / post_total * 100

# Create DataFrame for plotting
df_compare = pd.DataFrame({
    'Extremist %': [pre_percent, post_percent]
}, index=['Pre-Musk', 'Post-Musk'])

# Plot
df_compare.plot(kind='bar', legend=False, rot=0)
plt.title('Percentage of Extremist Tweets (Pre vs Post Musk)')
plt.ylabel('Percentage')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Print summary
print("Summary Statistics:")
print(df_compare.round(2))
