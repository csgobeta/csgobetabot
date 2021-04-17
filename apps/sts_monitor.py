import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


import feedparser
import logging
import telebot
import re
import time
import config
from plugins import strings


stsgroup_url = 'https://steamcommunity.com/groups/STSLounge/rss/'


def sts_monitor():
    currentSTS = feedparser.parse(stsgroup_url).entries
    while True:
        try:
            newSTS = feedparser.parse(stsgroup_url).entries
            if newSTS != currentSTS:
                if 'csgo' in newSTS[0].summary_detail.value:
                    newStrings = newSTS[0]
                    currentSTS = newSTS
                    send_alert(newStrings)
            time.sleep(40)
        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(data):
    strList = re.findall(r'csgo/[\w]+\.txt', data.summary_detail.value)
    cleanList = []
    for i in strList:
        cleanList.append(re.sub(r'csgo/', '', i))
    changes = '• ' + '\n• '.join(cleanList)
    text_en = strings.notiNewSTS_en.format(changes, data.link)
    text_ru = strings.notiNewSTS_ru.format(changes, data.link)
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.CSGOBETACHAT_EN]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        if chatID == config.CSGOBETACHAT:
            msg = bot.send_message(
                chatID, text_ru, parse_mode='html', disable_web_page_preview=True)
        else:
            msg = bot.send_message(
                chatID, text_en, parse_mode='html', disable_web_page_preview=True)
        bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sts_monitor()
