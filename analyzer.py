import re
from textblob import TextBlob
import glob
from collections import Counter
import os


class AnalysisClient:
    @staticmethod
    def clean_comment(comment):
        return " ".join(
            re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment
            ).split()
        )

    @staticmethod
    def get_comment_sentiment(comment):
        analysis = TextBlob(AnalysisClient.clean_comment(comment))
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

    @staticmethod
    def analyze_comments(filename):
        with open(filename, "r", encoding="utf-8") as file:
            comments = file.readlines()

        sentiments = [
            AnalysisClient.get_comment_sentiment(comment) for comment in comments
        ]
        return Counter(sentiments)


def get_subreddit_name(filename):
    base_name = os.path.basename(filename)
    return f"/r/{os.path.splitext(base_name)[0]}"


def main():
    txt_file_list = glob.glob("parsed_comments/*.txt")

    for file in txt_file_list:
        subreddit = get_subreddit_name(file)
        sentiment_counts = AnalysisClient.analyze_comments(file)

        total = sum(sentiment_counts.values())

        print(f"\nAnalysis for {subreddit}:")
        print(f"Total comments analyzed: {total}")

        for sentiment in ["positive", "negative", "neutral"]:
            count = sentiment_counts[sentiment]
            percentage = (count / total) * 100
            print(f"{sentiment.capitalize()} comments: {count} ({percentage:.2f}%)")

        print("-" * 40)


if __name__ == "__main__":
    main()
