import os
import shutil

PROFILE_PATHS = [
    "/Users/mirelradoi18/selenium3",
    "/Users/mirelradoi18/selenium4",
    "/Users/mirelradoi19/selenium",
    "/Users/mirelradoi19/selenium2"
]

def clean_profiles():
    for path in PROFILE_PATHS:
        try:
            if os.path.exists(path):
                print(f"Removing: {path}")
                shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)
            print(f"Recreated: {path}")
        except Exception as e:
            print(f"Error with {path}: {e}")

if __name__ == "__main__":
    clean_profiles()