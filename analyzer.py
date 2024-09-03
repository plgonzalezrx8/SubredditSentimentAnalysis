import re
from collections import Counter
import os
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(comment)
        if sentiment["compound"] >= 0.05:
            return "positive"
        elif sentiment["compound"] <= -0.05:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def analyze_comments(filename, keywords=None):
        with open(filename, "r", encoding="utf-8") as file:
            comments = file.readlines()

        overall_sentiments = [
            AnalysisClient.get_comment_sentiment(comment) for comment in comments
        ]

        keyword_sentiments = {}
        if keywords:
            for keyword in keywords:
                keyword_comments = [
                    comment
                    for comment in comments
                    if keyword.lower() in comment.lower()
                ]
                keyword_sentiments[keyword] = Counter(
                    [
                        AnalysisClient.get_comment_sentiment(comment)
                        for comment in keyword_comments
                    ]
                )

        return Counter(overall_sentiments), keyword_sentiments


def get_subreddit_name(filename):
    base_name = os.path.basename(filename)
    return f"/r/{os.path.splitext(base_name)[0]}"


def print_sentiment_analysis(sentiment_counts, total, label=""):
    print(f"{label}Total comments analyzed: {total}")
    for sentiment in ["positive", "negative", "neutral"]:
        count = sentiment_counts[sentiment]
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{sentiment.capitalize()} comments: {count} ({percentage:.2f}%)")


def main():
    txt_file_list = [f for f in os.listdir("parsed_comments") if f.endswith(".txt")]
    keywords = sys.argv[1].split() if len(sys.argv) > 1 else None

    for file in txt_file_list:
        subreddit = get_subreddit_name(file)
        overall_sentiments, keyword_sentiments = AnalysisClient.analyze_comments(
            os.path.join("parsed_comments", file), keywords
        )

        print(f"\nAnalysis for {subreddit}:")
        print_sentiment_analysis(overall_sentiments, sum(overall_sentiments.values()))

        if keywords:
            print(f"\nKeyword analysis for {subreddit}:")
            for keyword, sentiments in keyword_sentiments.items():
                total = sum(sentiments.values())
                print(f"\nKeyword: '{keyword}'")
                print_sentiment_analysis(sentiments, total)

        print("-" * 40)


if __name__ == "__main__":
    main()
