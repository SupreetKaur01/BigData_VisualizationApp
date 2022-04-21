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
import nltk
import pycountry
from textblob import TextBlob
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

# # # # TWITTER AUTHENTICATER # # # #



def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
    analysis = senti.getSentiment(clean_tweet(tweet), score='scale')
    return analysis

auth = tweepy.OAuthHandler(credentials.consumerKey, credentials.consumerSecret)
auth.set_access_token(credentials.accessToken, credentials.accessTokenSecret)
twitter_client = tweepy.API(auth)

#Sentiment Analysis
def percentage(part,whole):
 return 100 * float(part)/float(whole)

keyword = input("Please enter keyword or hashtag to search: ")
num_tweet = int(input ("Please enter how many tweets to analyze: "))
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
time_sentiment.plot(figsize=(10, 4), color='r', label="sentiments", legend=True)
plt.savefig('sentiment.png')
plt.show()

df.sentiment.plot.density(color='green')
plt.title('Density plot for sentiment')
plt.savefig('sentiment_Density.png')
plt.show()


#Function to Create Wordcloud
def create_wordcloud(text):
 mask = np.array(Image.open("cloud.png"))
 stopwords = set(STOPWORDS)
 wc = WordCloud(background_color="white",
 mask = mask,
 max_words=3000,
 stopwords=stopwords,
 repeat=True)
 wc.generate(str(text))
 wc.to_file("wc.png")
 print("Word Cloud Saved Successfully")
 path="wc.png"
 sys.displayhook(Image.open(path))

#Creating wordcloud for all tweets
create_wordcloud(df["tweets"].values)

