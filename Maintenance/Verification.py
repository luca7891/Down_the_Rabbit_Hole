import pandas as pd

# === Initialize clean_df === #
clean_df = pd.read_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Data/clean_tweets_final.csv")

print(f"Loaded dataset with {len(clean_df)} rows.\n")

# === Dataset Validation === #
print("==== Dataset Validation ====\n")

# 1. Check for missing text or timestamp
missing_text = clean_df['text'].isnull().sum()
missing_timestamp = clean_df['timestamp'].isnull().sum()
print(f"Missing text: {missing_text}")
print(f"Missing timestamp: {missing_timestamp}")

# 2. Check if timestamps are properly datetime
print("\nTimestamp dtype:", clean_df['timestamp'].dtype)

# 3. Check for '[Media or non-standard tweet]'
bad_texts = clean_df[clean_df['text'].str.contains(r'\[Media or non-standard tweet\]', na=False)]
print(f"\nNumber of '[Media or non-standard tweet]' left: {len(bad_texts)}")

# 4. Check duplicate URLs
duplicate_urls = clean_df.duplicated(subset="url").sum()
print(f"\nNumber of duplicate URLs: {duplicate_urls}")

# 5. Check likes, replies, retweets types
print("\nColumn types:")
print(clean_df[['likes', 'replies', 'retweets']].dtypes)

# 6. Check weird empty/whitespace tweets
whitespace_texts = clean_df[clean_df['text'].str.strip() == '']
print(f"\nNumber of empty/whitespace-only tweets: {len(whitespace_texts)}")

clean_df['timestamp'] = pd.to_datetime(clean_df['timestamp'], errors='coerce')
print(clean_df['timestamp'].dtype)

# 7. Check total NaNs in entire dataset
print(f"\nTotal NaN values in dataset: {clean_df.isnull().sum().sum()}")

print("\n==== Validation Done ====")

# Remove empty/whitespace-only tweets
clean_df = clean_df[clean_df['text'].str.strip() != '']

# Drop any rows with NaNs
clean_df = clean_df.dropna()

# Save back to clean file (optional)
clean_df.to_csv("/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Data/clean_tweets_final.csv", index=False)

print(f"After full cleanup, dataset size: {len(clean_df)} rows.")

