""" This will parse all the comments from the specified subreddits
and will organize them in text files, formatted the following way
    1) Each line is a comment
    2) Comments will have no attribution for privacy reasons
    3) Comments should not be duplicated
    4) All the text files should be inside a folder named "Parsed Data"
    in order to keep the main application folder from getting crowded
"""

"""This application will go through all the comments on a specific subreddit and parse all
the comments and save them to a local text file"""
import threading
import praw
import time
import cleaner
import glob

import configparser

config = configparser.ConfigParser()
config.read('creds.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']
client_id = config['DEFAULT']['client_id']
client_secret = config['DEFAULT']['client_secret']
user_agent = config['DEFAULT']['user_agent']

# reffer to the praw documentation for more info on clientID and client_secret. (API Keys)
r = praw.Reddit(username=username, password=password, client_id=client_id, client_secret=client_secret,
                user_agent=user_agent)
print("Logging in...")

counter = 0
cache = []  # cache to keep track of parsed comments


# this will get all the comments for the last 500 posts for that specific subreddit.
def run_bot(subreddit_name):
    print("Parsing comments from " + subreddit_name)
    # just type the subreddit name, do not use /r/ or anything else
    subreddit = r.subreddit(subreddit_name)
    file_name = "parsed_comments/" + subreddit_name + ".txt"
    print("Grabbing comments from " + subreddit_name)
    submissions = subreddit.hot(limit=500)
    for submission in submissions:
        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]

        while comment_queue:
            comment = comment_queue.pop(0)
            comment_text = comment.body.lower()
            if comment.id not in cache:
                print(subreddit_name + "=====" + comment_text)
                with open(file_name, "a", encoding="utf8") as myfile:
                    try:
                        myfile.write(" " + comment_text + "\n")
                    except UnicodeEncodeError:
                        pass
                    myfile.close()
                cache.append(comment.id)


# this is a 10 minute break to give reddit servers a break.
# THe action above will be executed 1000 times, but duplicates will be ignored using the cache variable.


subredditsToParse = ["trumpgret", "sandersforpresident", "funny", "wholesomememes", "news", "todayilearned",
                     "interestingasfuck", "wtf", "gifs", "highqualitygifs", "jokes", "the_donald", "keepournetfree",
                     "nintendoswitch", "atbge",
                     "mildlyinfuriating", "rage", "blackpeoplegifs", "pcmasterrace", "evilbuildings", "upliftingnews",
                     "fellowkids",
                     "whitepeopletwitter", "atheism", "beholdthemasterrace", "enoughtrumpspam", "political_revolution",
                     "worldnews",
                     "hillaryforprison", "liberal", "politics", "esist", "fuckthealtright",
                     "imgoingtohellforthis", "pandr", "unexpected", "mensrights", "me_irl"]

while counter < 1:
    for i in subredditsToParse:
        threading.Thread(name=i, target=run_bot, args=(i,)).start()

    print("Taking a little break")
    time.sleep(60 * 15)
    counter += 1

# this line will gather all the txt files in the directory, might need some tweaking to work in your environment.
txt_file_list = glob.glob("*.txt")

# this will clean all the txt files in the current directory.
# By cleaning I mean removing all the spaces and unsupported symbols.
for i in txt_file_list:
    cleaner.cleanemptylines(i)
