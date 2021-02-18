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
        tweet = json.loads(data)
        if tweet['user']['id'] == '353780675' and 'text' in tweet:
            clean_tweet = re.sub(r' http\S+', '', tweet['text'])
            bot = telebot.TeleBot(config.BOT_TOKEN)
            text = strings.notiNewTweet_ru.format(clean_tweet, tweet['id'])
            bot.send_message(config.CSGOBETACHAT, text)
        else:
            pass

    def on_error(self, status):
        print(status)
        
    def on_limit(self,status):
        print ("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

if __name__ == '__main__':
    listener = CSGOTwitterListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=[config.CSGOTWITTERID])