import pandas as pd
import tweepy
import json
import re

def word_in_text(word,text):
    word = word.lower()
    text = text.lower()
    match = re.search(word,text)
    if match:
        return True
    return False

CONSUMER_KEY = "Vd2xvDktj9bNXr6LQ3Qp66WBJ"
CONSUMER_SECRET = "Ar28LYiiEJxuFZtnfb49EKrzaLmluvaYGxEwevEOSbZiFbyx4A"
ACCESS_TOKEN = "3377451101-OsiLN4ZbyHUAB4tH4LgI08e2xTUjCm5oET8gcOF"
ACCESS_TOKEN_SECRET = "gw0rti3Jf2LZNZtIiVNolHkOU90odH0hCcdBq8T0NIiWW"

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
        
    def on_error(self,status_code):
        if status_code == 420:
            return False


    def on_status(self,status):
        if status.retweeted_status:
            return
        if status.favorite_count is None or status.favorite_count < 10:
            return
        if status.withheld_in_countries:
            return
        print(status.text)  
       
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color


        
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth = api.auth , listener = stream_listener)
        stream.filter(track=["modi","AbkiBarModiSarkar","ModiForPM"])

        import dataset
        db = dataset.connect("sqlite:///tweets.db")

        table = db["tweets"]
        table.insert(dict(
        user_description = description,
        user_location = loc,
        coordinates = coords,
        text = text,
        user_name = name,
        user_created = user_created,
        user_followers = followers,
        id_str = id_str,
        created = created,
        retweet_count = retweets,
        user_bg_color = bg_color)
        )     

        import sqlite3
        with open('C:\file.csv', 'w+') as write_file:
            conn =sqlite3.connect('sqlite://tweets.db')
            cursor = conn.cursor()
            for row in cursor.execute('SELECT * FROM table'):
                write_file.write(row)
                
        
