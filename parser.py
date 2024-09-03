import threading
import praw
import time
import os
from queue import Queue
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

# Create a thread-safe queue for subreddits
subreddit_queue = Queue()


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
                        print(f"{subreddit_name}====={comment_text[:50]}...")

                        with open(file_name, "a", encoding="utf-8") as myfile:
                            myfile.write(f"{comment_text}\n")

                        comment_cache.add(comment.id)

                time.sleep(2)  # Respect Reddit's rate limits

            except PrawcoreException as e:
                print(f"Error processing submission in {subreddit_name}: {e}")
                time.sleep(60)  # Wait a minute before continuing

    except PrawcoreException as e:
        print(f"Error accessing subreddit {subreddit_name}: {e}")


def worker():
    while True:
        subreddit = subreddit_queue.get()
        if subreddit is None:
            break
        run_bot(subreddit)
        subreddit_queue.task_done()


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
        "conservative",
        "democrats",
        "Republican",
        "politics",
        "worldnews",
        "news",
        "solarpunk",
        "AskReddit",
        "science",
        "books",
        "movies",
        "television",
        "music",
        "art",
        "history",
        "travel",
        "food",
        "cooking",
        "DIY",
        "gardening",
        "fitness",
        "loseit",
        "health",
        "mentalhealth",
        "depression",
        "anxiety",
        "bipolar",
        "schizophrenia",
        "autism",
    ]

    # Number of worker threads
    num_worker_threads = 4

    # Create worker threads
    threads = []
    for _ in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
        time.sleep(10)  # Stagger thread starts

    # Add subreddits to the queue
    for subreddit in subredditsToParse:
        subreddit_queue.put(subreddit)

    # Block until all tasks are done
    subreddit_queue.join()

    # Stop workers
    for _ in range(num_worker_threads):
        subreddit_queue.put(None)
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
