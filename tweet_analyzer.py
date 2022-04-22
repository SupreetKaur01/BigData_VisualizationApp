###Importing Libraries and Utilities

from pdb import main
from nltk.probability import ConditionalFreqDist, FreqDist
from nltk.tokenize import word_tokenize
import string, os, re
#import cStringIO
from io import StringIO
import json
import datetime
from collections import defaultdict
import pickle
import pandas as pd
import numpy as np
import pycountry
import sys
import tweepy
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

# Setting up the SentiStrength jar file for -5 to +5 sentiment classification
# Access of this jar can be made by emailing Dr. Mike Thelwall  http://sentistrength.wlv.ac.uk/#Java
# Note :  This can be used for educational purposes only

from sentistrength import PySentiStr
senti = PySentiStr()
senti.setSentiStrengthPath('C:/SentiStrength_Java/SentiStrength.jar') # Note: Provide absolute path instead of relative path
senti.setSentiStrengthLanguageFolderPath('C:/SentiStrength_Data/') # Note: Provide absolute path instead of relative path

from myconnection import getLocalHandler
from mystopwords import getStopWords
import credentials

#get database handler
#dbh = getLocalHandler()
#print (dbh.collection_names())

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
    analysis = senti.getSentiment(clean_tweet(tweet), score='scale')
    return analysis

def percentage(part,whole):
 return 100 * float(part)/float(whole)

# Twitter authentication for livestreaming tweets
# Keep an eye on rate limit exceeding exception: 412

auth = tweepy.OAuthHandler(credentials.consumerKey, credentials.consumerSecret)
auth.set_access_token(credentials.accessToken, credentials.accessTokenSecret)
twitter_client = tweepy.API(auth)

#Sentiment Analysis

def bitcoinAnalysis() :

    keyword = 'bitcoin'
    num_tweet = int('50')
    tweet_list=[]
    tweets=[]
    tweets = tweepy.Cursor(twitter_client.search_tweets, q=keyword).items(num_tweet)

    for tweet in tweets:
       tweet_list.append(tweet)

    #print(tweet_list)


    df = pd.DataFrame(data=[tweet.text for tweet in tweet_list], columns=['tweets'])
    df['sentiment'] = np.array([analyze_sentiment(tweet.text) for tweet in tweet_list])

    #render dataframe as html
    html = df.to_html(classes='table table-stripped')

    #write html to file
    text_file = open("tweets-df-bitcoin.html", "w", encoding="utf-8")
    text_file.write(html)
    text_file.close()

    
    df['id'] = np.array([tweet.id for tweet in tweet_list])
    df['len'] = np.array([len(tweet.text) for tweet in tweet_list])
    df['date'] = np.array([tweet.created_at for tweet in tweet_list])
    df['source'] = np.array([tweet.source for tweet in tweet_list])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweet_list])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweet_list])
    print(df)


    # Time Series
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(5, 4), label="bitcoin-sentiments")
    plt.title('Time series for bitcoin sentiment')
    plt.savefig('sentiment_bitcoin.png')
    plt.show()

    # Layered Time Series:
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    plt.title('Layered Time series for bitcoin sentiment')
    plt.savefig('Layered_sentiment_bitcoin1.png')
    plt.show()

    # Layered Time Series:
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    time_likes = pd.Series(data=df['retweets'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="retweets", legend=True)
    plt.title('Layered Time series for bitcoin sentiment')
    plt.savefig('Layered_sentiment_bitcoin2.png')
    plt.show()


    #Density plot
    df.sentiment.plot.density(color='green')
    plt.title('Density plot for bitcoin sentiment')
    plt.savefig('sentiment_Density_bitcoin.png')
    plt.show()

    #Layered density plot
    df.sentiment.plot.density(legend=True, label="sentiment")
    df.likes.plot.density(legend=True, label="likes")
    plt.title('Density plot for bitcoin-layered')
    plt.savefig('layered_sentiment_Density_bitcoin.png')
    plt.show()

    #Function to Create Wordcloud
    def create_wordcloud(text):
     mask = np.array(Image.open("cloud.png"))
     stopwords = set(STOPWORDS)
     stopwords.add("RT")
     stopwords.add("n")
     stopwords.add("t")
     stopwords.add("co")
     stopwords.add("https")
     stopwords.add("retweet")
     wc = WordCloud(background_color="white",
     mask = mask,
     max_words=3000,
     stopwords=stopwords,
     repeat=True)
     wc.generate(str(text))
     wc.to_file("wc_bitcoin.png")
     print("Word Cloud Saved Successfully")
     path="wc_bitcoin.png"
     sys.displayhook(Image.open(path))

    #Creating wordcloud for all tweets
    create_wordcloud(df["tweets"].values)

def ethereumAnalysis() :

    keyword = 'ethereum'
    num_tweet = int('50')
    tweet_list=[]
    tweets=[]
    tweets = tweepy.Cursor(twitter_client.search_tweets, q=keyword).items(num_tweet)

    for tweet in tweets:
       tweet_list.append(tweet)

    #print(tweet_list)

    df = pd.DataFrame(data=[tweet.text for tweet in tweet_list], columns=['tweets'])
    df['sentiment'] = np.array([analyze_sentiment(tweet.text) for tweet in tweet_list])

    #render dataframe as html
    html = df.to_html(classes='table table-stripped')

    #write html to file
    text_file = open("tweets-df-ethereum.html", "w", encoding="utf-8")
    text_file.write(html)
    text_file.close()

    df['id'] = np.array([tweet.id for tweet in tweet_list])
    df['len'] = np.array([len(tweet.text) for tweet in tweet_list])
    df['date'] = np.array([tweet.created_at for tweet in tweet_list])
    df['source'] = np.array([tweet.source for tweet in tweet_list])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweet_list])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweet_list])
    print(df)


    # Time Series
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(10, 4), color='r', label="ethereum sentiments", legend=True)
    plt.title('Time series for ethereum sentiment')
    plt.savefig('sentiment_ethereum.png')
    plt.show()

    # Layered Time Series:
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    plt.title('Layered time series for ethereum sentiment')
    plt.savefig('Layered_sentiment_ethereum.png')
    plt.show()


    #Density plot
    df.sentiment.plot.density(color='green')
    plt.title('Density plot for ethereum sentiment')
    plt.savefig('sentiment_Density_ethereum.png')
    plt.show()

    #Layered density plot
    df.sentiment.plot.density(legend=True, label="sentiment")
    df.likes.plot.density(legend=True, label="likes")
    plt.title('Density plot for ethereum-layered')
    plt.savefig('sentiment_Density_ethereum1.png')
    plt.show()

    #Layered density plot
    df.sentiment.plot.density(legend=True, label="sentiment")
    df.likes.plot.density(legend=True, label="retweets")
    plt.title('Density plot for ethereum-layered')
    plt.savefig('sentiment_Density_ethereum2.png')
    plt.show()

    #Function to Create Wordcloud
    def create_wordcloud(text):
     mask = np.array(Image.open("cloud.png"))
     stopwords = set(STOPWORDS)
     stopwords.add("RT")
     stopwords.add("n")
     stopwords.add("t")
     stopwords.add("co")
     stopwords.add("https")
     stopwords.add("retweet")
     wc = WordCloud(background_color="white",
     mask = mask,
     max_words=3000,
     stopwords=stopwords,
     repeat=True)
     wc.generate(str(text))
     wc.to_file("wc_ethereum.png")
     print("Word Cloud Saved Successfully")
     path="wc_ethereum.png"
     sys.displayhook(Image.open(path))

    #Creating wordcloud for all tweets
    create_wordcloud(df["tweets"].values)

def algorandAnalysis() :

    keyword = 'algorand'
    num_tweet = int('50')
    tweet_list=[]
    tweets=[]
    tweets = tweepy.Cursor(twitter_client.search_tweets, q=keyword).items(num_tweet)

    for tweet in tweets:
       tweet_list.append(tweet)

    #print(tweet_list)


    df = pd.DataFrame(data=[tweet.text for tweet in tweet_list], columns=['tweets'])
    df['sentiment'] = np.array([analyze_sentiment(tweet.text) for tweet in tweet_list])
    df['id'] = np.array([tweet.id for tweet in tweet_list])
    df['len'] = np.array([len(tweet.text) for tweet in tweet_list])
    df['date'] = np.array([tweet.created_at for tweet in tweet_list])
    df['source'] = np.array([tweet.source for tweet in tweet_list])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweet_list])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweet_list])
    print(df)


    # Time Series
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(5, 4), label="algorand-sentiments")
    plt.title('Time series for algorand sentiment')
    plt.savefig('sentiment_algorand.png')
    plt.show()

    # Layered Time Series:
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    plt.title('Layered Time series for algorand sentiment')
    plt.savefig('Layered_sentiment_algorand1.png')
    plt.show()

    # Layered Time Series:
    time_sentiment = pd.Series(data=df['sentiment'].values, index=df['date'])
    time_sentiment.plot(figsize=(16, 4), label="sentiment", legend=True)
    time_likes = pd.Series(data=df['retweets'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="retweets", legend=True)
    plt.title('Layered Time series for algorand sentiment')
    plt.savefig('Layered_sentiment_algorand2.png')
    plt.show()


    #Density plot
    df.sentiment.plot.density(color='green')
    plt.title('Density plot for algorand sentiment')
    plt.savefig('sentiment_Density_algorand.png')
    plt.show()

    #Layered density plot
    df.sentiment.plot.density(legend=True, label="sentiment")
    df.likes.plot.density(legend=True, label="likes")
    plt.title('Density plot for algorand-layered')
    plt.savefig('layered_sentiment_Density_algorand.png')
    plt.show()

    #Function to Create Wordcloud
    def create_wordcloud(text):
     mask = np.array(Image.open("cloud.png"))
     stopwords = set(STOPWORDS)
     stopwords.add("RT")
     stopwords.add("n")
     stopwords.add("t")
     stopwords.add("co")
     stopwords.add("https")
     stopwords.add("retweet")
     wc = WordCloud(background_color="white",
     mask = mask,
     max_words=3000,
     stopwords=stopwords,
     repeat=True)
     wc.generate(str(text))
     wc.to_file("wc_algorand.png")
     print("Word Cloud Saved Successfully")
     path="wc_algorand.png"
     sys.displayhook(Image.open(path))

    #Creating wordcloud for all tweets
    create_wordcloud(df["tweets"].values)

#Calling functions for real time analysis
bitcoinAnalysis()
ethereumAnalysis()
#algorandAnalysis()

