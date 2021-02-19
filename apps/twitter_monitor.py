import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from tweepy import StreamListener, Stream, OAuthHandler

import telebot
import json
import re

import logging
import config
import strings

auth = OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_KEY_S)
auth.set_access_token(config.TWITTER_TOKEN, config.TWITTER_TOKEN_S)

class CSGOTwitterListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if 'user' in tweet and tweet['user']['id_str'] == config.CSGO_TWITTER_ID:
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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    l = CSGOTwitterListener()
    twitterStream = Stream(auth, l)
    twitterStream.filter(follow=[config.CSGO_TWITTER_ID])