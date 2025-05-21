import os
import shutil
import time
import random
import pandas as pd
import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from dateutil import parser

# === CONFIG === #
PROFILE_PATHS = ["", ""]
TWITTER_HOME_URL = "https://twitter.com/i/flow/login"
TWITTER_HOME = "https://x.com/home"
GMAIL_EMAIL = ""
GMAIL_PASSWORD = ""
OUTPUT_FILE = "Data/foryou_tweets_bot2.csv"
BOT_NAME = "bot2"
STATUS_FILE = "Maintenance/status_file.lock"
PROFILE_STATE_FILE = "Maintenance/profile_state_bot2.txt"

# === Profile  === #
def load_profile_index():
    if os.path.exists(PROFILE_STATE_FILE):
        try:
            with open(PROFILE_STATE_FILE, "r") as f:
                idx = int(f.read().strip())
                if idx in (0, 1):
                    return idx
        except:
            pass
    return 0
current_index = load_profile_index()

def clean_profile(profile_path):
    try:
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)
        os.makedirs(profile_path, exist_ok=True)
    except Exception as e:
        print(f"Failed to clean profile at {profile_path}: {e}")

# === Coordination  === #
def update_status(status):
    with open(STATUS_FILE, "a") as f:
        f.write(f"{BOT_NAME}: {status}\n")

def last_bot_status(bot_name):
    if not os.path.exists(STATUS_FILE):
        return None
    with open(STATUS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        for line in reversed(lines):
            if line.startswith(f"{bot_name}:"):
                return line.split(":")[1].strip()
    return None

def wait_for_other_bot(other_bot, timeout=90):
    print(f"[{BOT_NAME}] Waiting for {other_bot} to login...")
    start = time.time()
    while time.time() - start < timeout:
        status = last_bot_status(other_bot)
        print(f"[{BOT_NAME}] Checking {other_bot}: {status}")
        if status == "in":
            print(f"[{BOT_NAME}] {other_bot} is ready. Continuing...")
            return
        time.sleep(2)
    print(f"[{BOT_NAME}] Timeout waiting for {other_bot}. Continuing anyway.")
def should_wait_on_start():
    if BOT_NAME == "bot2":
        return True
    return False

# === Login  === #
def ensure_chrome_closed(profile_path):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                if cmdline and profile_path in ' '.join(cmdline):
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def find_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    addr, port = s.getsockname()
    s.close()
    return port


def create_driver(profile_path):
    options = Options()
    port = find_free_port()
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/122.0.0.0 Safari/537.36")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.2, 0.5))


def login_through_google(driver, profile_path, retries=6):
    try:
        print("Opening Twitter login page...")
        driver.get(TWITTER_HOME_URL)
        time.sleep(5)

        # Basic sanity check
        if "CAPTCHA" in driver.page_source or "verify it's you" in driver.page_source.lower():
            raise Exception("CAPTCHA detected – restart required.")

        print("Waiting for Google login container...")
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="google_sign_in_container"]'))
        )
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="google_sign_in_container"]//iframe'))
        )
        driver.switch_to.frame(iframe)

        try:
            login_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" or @id][@tabindex="0"]'))
            )
            time.sleep(1)
            login_btn.click()
        except Exception:
            print("Standard click failed, trying JavaScript click...")
            time.sleep(5)
            login_btn = driver.find_element(By.XPATH, '//div[@role="button" or @id][@tabindex="0"]')
            driver.execute_script("arguments[0].click();", login_btn)

        driver.switch_to.default_content()
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to Google login window...")

        email_input = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))
        )
        type_like_human(email_input, GMAIL_EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        password_input = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
        )
        type_like_human(password_input, GMAIL_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(15)
        driver.get(TWITTER_HOME)
        print(f"[{GMAIL_EMAIL}] Twitter is ready — signal written.")
        update_status("in")
        time.sleep(5)
        return True

    except Exception as e:
        print(f"Login failed: {e}")
        try:
            driver.quit()
            update_status("out")
        except:
            pass
        clean_profile(profile_path)
        if retries > 0:
            print("Retrying login...")
            return login_through_google(create_driver(profile_path), profile_path, retries - 1)
        return False

# ===Configuration Scrapping=== #
SCROLL_PAUSE = 2
LONG_PAUSE_EVERY = 25
LONG_PAUSE_TIME = 20
NO_NEW_TWEETS_LIMIT = 3
SAVE_EVERY = 1
current_index = load_profile_index()

# ===Scrapping=== #
def extract_engagement(tweet):
    def get_count(testid):
        try:
            el = tweet.find_element(By.XPATH, f'.//button[@data-testid="{testid}"]//span')
            text = el.text.strip().replace(',', '').upper()
            if not text: return 0
            if 'K' in text: return int(float(text.replace('K', '')) * 1_000)
            if 'M' in text: return int(float(text.replace('M', '')) * 1_000_000)
            return int(text)
        except Exception:
            return 0

    return get_count("reply"), get_count("retweet"), get_count("like")


def save_progress(data):
    df = pd.DataFrame(data)
    file_exists = os.path.exists(OUTPUT_FILE)
    df.to_csv(OUTPUT_FILE, mode='a', index=False, header=not file_exists)
    print(f"[{GMAIL_EMAIL}] Appended {len(data)} new tweets — Total now: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")


def start_scraping():
    global current_index

    if should_wait_on_start():
        wait_for_other_bot("bot1")  # Only bot2 waits ONCE for bot1 at start

    while True:
        active_profile = PROFILE_PATHS[current_index]
        inactive_profile = PROFILE_PATHS[1 - current_index]
        ensure_chrome_closed(active_profile)
        clean_profile(inactive_profile)

        try:
            driver = create_driver(active_profile)
            time.sleep(5)

            if not login_through_google(driver, active_profile):
                continue

            tweet_ids = set()
            tweets_data = []
            if os.path.exists(OUTPUT_FILE):
                existing_df = pd.read_csv(OUTPUT_FILE)
                tweet_ids.update(existing_df["url"].apply(lambda u: u.split("/")[-1]))
                tweets_data.extend(existing_df.to_dict("records"))

            no_new_tweet_rounds = 0
            rounds = 0
            while no_new_tweet_rounds < NO_NEW_TWEETS_LIMIT:
                new_tweets = []  # track tweets per scroll
                prev_count = len(tweet_ids)
                driver.execute_script(f"window.scrollBy(0, {random.randint(3000, 6000)});")
                time.sleep(random.uniform(5.0, 8.0))
                WebDriverWait(driver, 10).until(
                    lambda d: len(d.find_elements(By.XPATH, '//article[@role="article"]')) > 0)

                tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')
                for tweet in tweets:
                    try:
                        timestamp_el = tweet.find_element(By.XPATH, './/time')
                        tweet_time = parser.parse(timestamp_el.get_attribute("datetime")).replace(tzinfo=None)
                        content = tweet.find_element(By.XPATH,
                                                     './/div[@data-testid="tweetText"]').text if tweet.find_elements(
                            By.XPATH, './/div[@data-testid="tweetText"]') else "[Media or non-standard tweet]"
                        tweet_url = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute(
                            "href")
                        tweet_id = tweet_url.split("/")[-1]

                        if tweet_id not in tweet_ids:
                            replies, retweets, likes = extract_engagement(tweet)

                            tweet_data = {
                                "text": content,
                                "timestamp": tweet_time.isoformat(),
                                "url": tweet_url,
                                "likes": likes,
                                "replies": replies,
                                "retweets": retweets
                            }

                            tweets_data.append(tweet_data)
                            tweet_ids.add(tweet_id)
                            new_tweets.append(tweet_data)

                            if len(new_tweets) >= SAVE_EVERY:
                                save_progress(new_tweets)
                                new_tweets = []

                    except Exception:
                        continue

                if new_tweets:
                    save_progress(new_tweets)
                    new_tweets = []

                curr_count = len(tweet_ids)
                if curr_count == prev_count:
                    no_new_tweet_rounds += 1
                    for _ in range(3):
                        driver.execute_script(f"window.scrollBy(0, {-random.randint(2000, 4000)});")
                        time.sleep(random.uniform(5.0, 7.0))
                else:
                    no_new_tweet_rounds = 0

                rounds += 1
                if rounds % LONG_PAUSE_EVERY == 0:
                    print(f"Long pause for {LONG_PAUSE_TIME}s")
                    time.sleep(LONG_PAUSE_TIME)

            print(f"No new tweets detected. {len(tweets_data)} tweets collected.")

        except Exception as e:
            print(f"[{BOT_NAME}] Exception: {e}")

        finally:
            update_status("out")
            try:
                driver.quit()
            except:
                pass
            ensure_chrome_closed(active_profile)
            current_index = 1 - current_index
            with open(PROFILE_STATE_FILE, "w") as f:
                f.write(str(current_index))
            time.sleep(10)


if __name__ == "__main__":
    start_scraping()
