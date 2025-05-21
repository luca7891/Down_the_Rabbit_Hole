import pandas as pd

# Load with error handling and flexible column name detection
def load_tweets(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', engine='python')
    tweet_col = next((col for col in df.columns if 'tweet' in col.lower()), None)
    if tweet_col is None:
        raise ValueError(f"No tweet-like column found in {file_path}")
    return df[[tweet_col]].rename(columns={tweet_col: 'tweet'})

# Load both files
# Load both datasets
train_df = pd.read_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/train.csv')
test_df = pd.read_csv('/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/test.csv')

train_tweets = train_df[['tweet']]
test_tweets = test_df[['tweet']]
# Combine
combined = pd.concat([train_tweets, test_tweets], ignore_index=True)

# Optional: remove null or empty tweets
combined = combined.dropna(subset=['tweet'])
combined = combined[combined['tweet'].str.strip() != '']

print(f"Train tweets: {len(train_tweets)}")
print(f"Test tweets: {len(test_tweets)}")
print(f"Combined before drop: {len(train_tweets) + len(test_tweets)}")
print(f"Combined after dropna/empty: {len(combined)}")

output_path = '/Users/lucadutu/PycharmProjects/Programming for AI/BAP/Data/Pre-Musk Data/all_tweets.csv'
combined.to_csv(output_path, index=False)
print(f"Saved {len(combined)} tweets to {output_path}")