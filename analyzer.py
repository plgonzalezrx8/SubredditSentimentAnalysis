import re
# import praw Remove if unneeded
from textblob import TextBlob
import glob


class AnalysisClient(object):

    """The Get Comments method is a clusterfuck, I need to fix it and make it work
    with the comments from the txt files"""

    def get_comments(self, count=10):
        # Main function to fetch comments and parse them.
        # empty list to store parsed comments
        comments = []

        with open("parsed_comments/enoughtrumpspam.txt", encoding='utf8') as li:
            comments = li.readlines()
            li.close()


        fetched_comments = comments  # and places them in a list

        comments_to_return = []

        # parsing tweets one by one
        for comment in range(len(fetched_comments)):
            # empty dictionary to store required params of a comment
            parsed_comment = {}
            # saving text of comment
            parsed_comment['text'] = fetched_comments[comment]
            # saving sentiment of comment
            parsed_comment['sentiment'] = self.get_comment_sentiment(fetched_comments[comment])  # maybe just 'comment' since
            # it doesn't have a text attribute

            comments_to_return.append(parsed_comment)

            # return parsed tweets
        return comments_to_return





    def clean_comment(self, comment):
        '''
        Utility function to clean comment text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

    def get_comment_sentiment(self, comment):
        '''
        Utility function to classify sentiment of passed comment
        using textblob's sentiment method
        '''
        # create TextBlob object of passed comment text
        analysis = TextBlob(self.clean_comment(comment))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'




def main():
    # creating object of AnalysisClient Class
    api = AnalysisClient()
    # calling function to get parse comments from txt files
    comments = api.get_comments(count=200)



    pcomments = []
    ncomments = []
    for comment in comments:
        if comment['sentiment'] == 'positive':
            pcomments.append(comment)
        elif comment['sentiment'] == 'negative':
            ncomments.append(comment)


    # percentage of positive comments
    print("Positive comments percentage: {} %".format(100*len(pcomments)/len(comments)))
    # percentage of negative comments
    print("Negative comments percentage: {} %".format(100*len(ncomments)/len(comments)))
    # percentage of neutral comments
    print("Neutral comments percentage: {} % \
        ".format(100*(len(comments) - len(ncomments) - len(pcomments))/len(comments)))

    # # printing first 5 positive comments
    # print("\n\nPositive comments:")
    # for comment in comments[:5]:
    #     print("Comment :" + str(comment['text']))
    #
    # # printing first 5 negative comments
    # print("\n\nNegative comments:")
    # for comment in ncomments[:5]:
    #     print("Comment :" + str(comment['text']))

    print("Total positive coments: " + str(len(pcomments)))
    print("Total negative comments: " + str(len(ncomments)))
    print("Total neutral comments: " + str(len(comments) - len(ncomments) - len(pcomments)))
    print("Total comments analized: " + str(len(comments)))


main()

