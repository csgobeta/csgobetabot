import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import telebot
import time
import config

with open(config.USER_MESSAGE_FILE_PATH, 'r') as f:
    text = f.read()
data = pd.read_csv(config.USER_DB_FILE_PATH)
for userID in data['UserID']:
    bot = telebot.TeleBot(config.BOT_TOKEN)
    bot.send_message(userID, text, parse_mode='Markdown')
    time.sleep(3)