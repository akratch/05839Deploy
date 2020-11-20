#Program adapted from GeeksforGeeks: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
#consumer_key = "yJsuGs8DcLZjVe4w46RlmE7EU"
#consumer_secret = "7LTHqVUngpY2TnrO2TUKIGDOU3pokGh1s48AhqGDArqrv6ajtv"
#access_token = "1090450437222948864-upQR0M9V0ChS6QKRsRMgsZnBtkZ5oT"
#access_token_secret = "5ntu65BcOUlU1Qwm8Nu369ijMqTkaNhl4CLb60whqXxYQ"

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "yJsuGs8DcLZjVe4w46RlmE7EU"
        consumer_secret = "7LTHqVUngpY2TnrO2TUKIGDOU3pokGh1s48AhqGDArqrv6ajtv"
        access_token = "1090450437222948864-upQR0M9V0ChS6QKRsRMgsZnBtkZ5oT"
        access_token_secret = "5ntu65BcOUlU1Qwm8Nu369ijMqTkaNhl4CLb60whqXxYQ"

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])\
                                    |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['date'] = tweet.created_at
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            print(tweets[0])
            print(tweets[-1])
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def main():
    # creating object of TwitterClient Class
    q_word = "Carnegie Mellon University"
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = q_word, count = 20000000)
    #print("Example of a tweet")
    print(len(tweets))

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    ntext = []
    for tweet in ntweets:
        ntext.append(tweet['text'])
    print("Negative text compilation")
    print(ntext[1])
    ntext = " ".join(ntext)
    re.sub(r'\b\w{1,3}\b', '', ntext)
    #Wordcloud part..
    stop_words = ["https", "co", "RT","realDonaldTrump","t","Re","S",q_word]+list(STOPWORDS)
    wordcloud = WordCloud(stopwords=stop_words,max_words = 20, width = 1000, height = 500).generate(ntext)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("test"+".png", bbox_inches='tight')
    plt.show()
    plt.close()


if __name__ == "__main__":
    # calling main function
    main()
