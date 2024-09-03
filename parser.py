import threading
import praw
import time
import os
from prawcore.exceptions import PrawcoreException
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read("creds.ini")

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=config["DEFAULT"]["client_id"],
    client_secret=config["DEFAULT"]["client_secret"],
    user_agent=config["DEFAULT"]["user_agent"],
    username=config["DEFAULT"]["username"],
    password=config["DEFAULT"]["password"],
)

print("Logging in...")

# Ensure the parsed_comments directory exists
os.makedirs("parsed_comments", exist_ok=True)

# Use a set for faster lookup
comment_cache = set()


def run_bot(subreddit_name):
    print(f"Parsing comments from {subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    file_name = f"parsed_comments/{subreddit_name}.txt"

    try:
        for submission in subreddit.hot(limit=500):
            try:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if comment.id not in comment_cache:
                        comment_text = comment.body.lower()
                        print(
                            f"{subreddit_name}====={comment_text[:50]}..."
                        )  # Print first 50 chars

                        with open(file_name, "a", encoding="utf-8") as myfile:
                            myfile.write(f"{comment_text}\n")

                        comment_cache.add(comment.id)

                # Respect Reddit's rate limits
                time.sleep(2)

            except PrawcoreException as e:
                print(f"Error processing submission in {subreddit_name}: {e}")
                time.sleep(60)  # Wait a minute before continuing

    except PrawcoreException as e:
        print(f"Error accessing subreddit {subreddit_name}: {e}")


def main():
    subredditsToParse = [
        "funny",
        "teslamotors",
        "TeslaModel3",
        "TeslaLounge",
        "upwork",
        "Catholicism",
        "Fromsoftware",
        "uscg",
    ]  # Add more subreddits as needed

    threads = []
    for subreddit in subredditsToParse:
        thread = threading.Thread(target=run_bot, args=(subreddit,))
        thread.start()
        threads.append(thread)
        time.sleep(2)  # Stagger thread starts

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
