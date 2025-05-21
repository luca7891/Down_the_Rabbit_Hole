import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/LLM Data/post_musk_predictions.csv')

# Calculate total engagement
df['total_engagement'] = df['likes'] + df['retweets'] + df['replies']

# Group by label and calculate mean
grouped = df.groupby('predicted_label')['total_engagement'].mean()
grouped.index = grouped.index.map({0: 'Normal', 1: 'Extremist'})
print(grouped)
# Plot
grouped.plot(kind='bar', color=['#1f77b4', '#1f77b4'])
plt.title('Average Total Engagement')
plt.ylabel('Engagement Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()