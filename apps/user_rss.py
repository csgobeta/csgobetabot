import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import telebot

import time
import logging

import config
from plugins import strings
CIS_lang_codes = ['ru', 'uk', 'be', 'uz', 'kk']

def send_messages():
    data = pd.read_csv(config.USER_DB_FILE_PATH)
    for name, userID, lang in zip(data['Name'], data['UserID'], data['Language']):
        if lang in CIS_lang_code:
            with open(config.USER_RU_MESSAGE_FILE_PATH, 'r') as f:
                text = f.read().format(username = name)
            bot = telebot.TeleBot(config.BOT_TOKEN)
            bot.send_message(userID, text, parse_mode='Markdown')
            time.sleep(3)
        else:
            with open(config.USER_EN_MESSAGE_FILE_PATH, 'r') as f:
                text = f.read().format(username = name)
            bot = telebot.TeleBot(config.BOT_TOKEN)
            bot.send_message(userID, text, parse_mode='Markdown')
            time.sleep(3)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    send_messages()