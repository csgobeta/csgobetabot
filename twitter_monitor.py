from tweepy import StreamListener
from tweepy import Stream
import tweepy

import telebot
import json
import re

import config
import strings

auth = tweepy.OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_KEY_S)
auth.set_access_token(config.TWITTER_TOKEN, config.TWITTER_TOKEN_S)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

class CSGOTwitterListener(StreamListener):
    def on_data(self, data):
        delta = json.loads(data)
        if 'text' in delta:
            clean_tweet = re.sub(r' http\S+', '', delta['text'])
            bot = telebot.TeleBot(config.BOT_TOKEN)
            text = strings.notiNewTweet_ru.format(clean_tweet, delta['id'])
            bot.send_message(config.CSGOBETACHAT, text)
        else:
            pass

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = CSGOTwitterListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=['353780675'])