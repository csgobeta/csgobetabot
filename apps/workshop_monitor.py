import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import requests
import traceback
import logging
import telebot

from datetime import datetime
import time

import config
import strings

workshop_url = f'https://api.steampowered.com/IPublishedFileService/GetUserFiles/v1/?key={config.STEAM_API_KEY}&steamid={config.CSGO_STEAM_PROFILE_ID}&appid=730&page=1&numperpage=18'

def workshop_monitor():
    data = requests.get(workshop_url).json()
    currentWorkshop = data['response']
    currentTags = []
    for tag in currentWorkshop['publishedfiledetails']:
        currentTags.append(tag['publishedfileid'])
    while True:
        try:
            data = requests.get(workshop_url).json()
            newWorkshop = data['response']
            newTags = []
            for tag in newWorkshop['publishedfiledetails']:
                newTags.append(tag['publishedfileid'])
            if len(newTags) == 0:
                time.sleep(60)
                continue
            else:
                if currentTags != newTags:
                    tempTags = currentTags[:]
                    modifiedTags = [i for i in newTags if not i in tempTags or tempTags.remove(i)]

                    mapNames = []
                    for tag in modifiedTags:
                        name = list(filter(lambda x:x['publishedfileid'] == tag, newWorkshop['publishedfiledetails']))[0]['title'].split()[0]
                        mapNames.append(name)

                    delta = list(zip(mapNames, modifiedTags))
                    if len(delta) < 2:   
                        for x, y in delta:
                            text = strings.notiNewMap_ru.format(x, y)
                        send_alert(text)
                    else:
                        names = ' и '.join([', '.join(mapNames[:-1]),mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        text = strings.notiNewMaps_ru.format(names)
                        send_alert(text)
                currentTags = newTags
                time.sleep(60)
        except:
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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    workshop_monitor()