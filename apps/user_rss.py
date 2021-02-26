import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import telebot

import time
import logging
import config

def send_messages():
    data = pd.read_csv(config.USER_DB_FILE_PATH)
    for Name, UserID in zip(data['Name'], data['UserID']):
        with open(config.USER_MESSAGE_FILE_PATH, 'r') as f:
            text = f.read().format(username = Name)
        bot = telebot.TeleBot(config.BOT_TOKEN)
        bot.send_message(UserID, text, parse_mode='Markdown')
        time.sleep(3)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    send_messages()