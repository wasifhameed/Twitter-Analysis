import pymongo
from pymongo import MongoClient
import twitter
from pprint import pprint
from abc import ABCMeta,abstractmethod
from twiterKeys import TwitterConfig
import pandas as pd
from textblob import TextBlob
import re
import os

class TwitterBase(metaclass=ABCMeta):

    @abstractmethod
    def callApi(self):
        return 0
    @abstractmethod
    def startProcess(self):
        return 0
    @abstractmethod
    def searchTweets(self):
        return 0
    @abstractmethod
    def saveTweets(self):
        return 0

class MongoInitilize(TwitterBase,TwitterConfig):

    ## api call to fetch tweets from twitter
    def callApi(self):
        self.auth = twitter.oauth.OAuth(self._TwitterConfig__OAUTH_TOKEN, self._TwitterConfig__OAUTH_TOKEN_SECRET, self._TwitterConfig__CONSUMER_KEY, self._TwitterConfig__CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)
        return self.twitter_api

    ## table creation
    def mongoTableCreate(self):
        ## create our database
        self.tweet_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        print("Database Created")

    ## table variable initiation
    def mongoDbname(self):
        self.dbNameTwitter = "tweets_db"
        self.db = self.client.tweets_db
        self.tweet_collection = self.db.tweet_collection

    ## create data base using pymongo
    def startProcess(self):
        self.client = MongoClient()
        self.mongoDbname()
        #print(self.client.list_database_names())
        ## check if data base already exists or not
        self.dbNames = self.client.list_database_names()
        if self.dbNameTwitter in self.dbNames:
            ## method call to perform the action
            try:
                os.remove("out.csv")
            except:
                print("file not found exception")
                pass
            self.searchTweets()
        else:
            self.mongoTableCreate()
            self.searchTweets()

    def searchTweets(self):
        print("Searching tweets")
        self.count = int(input("Enter the no of tweets to stream : "))
        self.query = input("Enter the keyword to search : ")
        ## twitter api call
        self.tweetz = self.callApi()
        self.searchResult = self.tweetz.search.tweets(count=self.count,q=self.query)
        pprint(self.searchResult['search_metadata'])
        ## method call save the result into mongoDB
        self.saveTweets()

    def saveTweets(self):
        print("Saving the tweets into mongoDB")
        self.tweet_collection.drop()
        self.statuses = self.searchResult["statuses"]
        for status in self.statuses:
            try:
                self.tweet_collection.insert(status)
                ##pprint(status)
            except:
                pass


class PerfromAnalysis(MongoInitilize):

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def checkTweetSentimen(self,tweet):
        self.tweet = tweet
        self.analysis = TextBlob(self.cleanTweet(self.tweet))
        if self.analysis.sentiment.polarity > 0:
            return 'positive'
        elif self.analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def startCheck(self):
        self.client = MongoClient()
        self.dbNames = self.client.list_database_names()
        self.comment = []
        self.result = []
        if "tweets_db" in self.dbNames:
            self.db = self.client.tweets_db
            try:
                self.tweet_collection = self.db.tweet_collection
                self.tweet_cursor = self.tweet_collection.find()

                for document in self.tweet_cursor:
                    try:
                        #print('name:-', document["user"]["name"])
                       # print('text:-', document["text"])
                        self.tmpstr = self.checkTweetSentimen(document["text"])
                        self.comment.append(self.cleanTweet(document["text"]))
                        self.result.append(self.tmpstr)
                        #print(self.tmpstr)
                        #print('Created Date:-', document["created_at"])
                    except:
                        print("Error in Encoding")
                        pass
            except:
                print("Documents not found")
                pass
        else:
            print("Database not found")

        self.outDf = pd.DataFrame({'Comment': self.comment, 'Result': self.result},index=None)
        self.outDf.to_csv("out.csv")


if __name__ == '__main__':
    mongo = MongoInitilize()
    mongo.startProcess()
    analysis = PerfromAnalysis()
    analysis.startCheck()
