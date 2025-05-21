import os
import pandas as pd

CSV_FOLDER = os.path.expanduser("/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Data")

def deduplicate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if "url" not in df.columns:
            print(f"Skipped (no 'url' column): {file_path}")
            return
        before = len(df)
        df = df.drop_duplicates(subset="url")
        after = len(df)
        if before > after:
            df.to_csv(file_path, index=False)
            print(f"Cleaned {file_path} — Removed {before - after} duplicates")
        else:
            print(f"{file_path} is already clean.")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def clean_all_csvs(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            full_path = os.path.join(folder_path, file)
            deduplicate_csv(full_path)

if __name__ == "__main__":
    clean_all_csvs(CSV_FOLDER)