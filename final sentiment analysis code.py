import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

import numpy as np
import pandas as pd
import re


# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler("dH3QEI7Zrv5xgyM1JgNvPs7Ba", "oeN8HZJp3PIn3n0XZzMS7BePe4tI9FYz6ZBeIISAqV1YtpBMZI")
        auth.set_access_token("1031787320834486272-4rp0l8PIubzl3orECrFSXhH8UGwKvl", "aecV9aw9mrQcZkVSs73gBCqPH7oH7JpWGHUTsPwtQyMa2")
        return auth

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
            return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
            return home_timeline_tweets


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        #df['id'] = np.array([tweet.id for tweet in tweets])
        #df['len'] = np.array([len(tweet.text) for tweet in tweets])
        #df['date'] = np.array([tweet.created_at for tweet in tweets])
        #df['source'] = np.array([tweet.source for tweet in tweets])
        #df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="IRENA", count=200)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    print(df.head(20))

"""
    # Get average length off all tweets
    print(np.mean(df['len']))

    #Get the number of likes for the most liked tweet
    print(np.max(df['likes']))

    # Get the number of retweets for the most retweeted tweet
    print(np.max(df['retweets']))

    # Time series for retweets
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(color='r')
    #plt.show()

    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(label='retweets', legend=True)
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(label='likes', legend=True)

    plt.show()


    Time series for likes
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), color='r')
    plt.show()





    #print(df.head(10))
    #print(dir(tweets[0]))
    #print(tweets[0].id)
    #print(tweets[0].retweet_count)

    """
# Authenticate using config.py and connect to Twitter Streaming API.
# hash_tag_list = ["corona", "sanitizer"]
# fetched_tweets_filename = "tweets.txt"

# twitter_client = TwitterClient('pycon')
# print(twitter_client.get_user_timeline_tweets(5))
# print(twitter_client.get_friend_list(5))
# print(twitter_client.get_home_timeline_tweets(5))


# twitter_streamer = TwitterStreamer()
# twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)