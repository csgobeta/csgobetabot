import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import requests
from bs4 import BeautifulSoup

import traceback
import logging

from datetime import datetime
import time

import telebot

import config
import strings

url = 'https://steamcommunity.com/profiles/76561198082857351/myworkshopfiles/?appid=730&p=1&numperpage=18'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

def workshop_monitor():
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    currentTags = []
    for tag in soup.find_all(class_='ugc'):
        currentTags.append(tag.get('data-publishedfileid'))
    while True:
        try:
            soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
            newTags = []
            for tag in soup.find_all(class_='ugc'):
                newTags.append(tag.get('data-publishedfileid'))
            if len(newTags) == 0:
                time.sleep(60)
                continue
            else:
                urlList, nameList = [], []
                if currentTags != newTags:
                    tempTags = currentTags[:]
                    modifiedTags = [i for i in newTags if not i in tempTags or tempTags.remove(i)]
                    workshop = soup.find('div', {'class': 'workshopBrowseItems'})
                    for tag in modifiedTags:
                        urlPath = workshop.find_all('a', attrs={'class': 'ugc', 'data-publishedfileid': tag})
                        for i in urlPath:
                            newUrl = i['href']
                            urlList.append(newUrl)
                            newName = i.find_parent('div').find('div', attrs={'class': 'workshopItemTitle'}).string.split()[0]
                            nameList.append(newName)
                    data = list(zip(urlList, nameList))
                    if len(data) < 2:
                        for x, y in data:
                            text = strings.notiNewMap_ru.format(y, x)
                        send_alert(text)
                    else:
                        names = ' и '.join([', '.join(nameList[:-1]),nameList[-1]] if len(nameList) > 2 else nameList)
                        text = strings.notiNewMaps_ru.format(names)
                        send_alert(text)
                currentTags = newTags
                time.sleep(60)

        except AttributeError:
            error_message = traceback.format_exc()
            now = str(datetime.now())
            print(f'{now} - Error:\n{error_message}\n\n\n')
            time.sleep(60)
            workshop_monitor()

def send_alert(text):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chatID = config.CSGOBETACHAT
    else:
        chatID = config.OWNER
    bot.send_message(chatID, text, parse_mode='Markdown')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(process)d %(message)s')
    workshop_monitor()