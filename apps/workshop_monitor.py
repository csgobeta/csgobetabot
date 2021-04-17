import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from plugins import strings
import config
import time
import telebot
import logging
import requests


workshop_url = f'https://api.steampowered.com/IPublishedFileService/GetUserFiles/v1/?key={config.STEAM_API_KEY}&steamid={config.CSGO_STEAM_PROFILE_ID}&appid={config.CSGO_APP_ID}&page=1&numperpage=18'


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
                    modifiedTags = [
                        i for i in newTags if not i in tempTags or tempTags.remove(i)]

                    mapNames = []
                    for tag in modifiedTags:
                        name = list(filter(lambda x: x['publishedfileid'] == tag, newWorkshop['publishedfiledetails']))[
                            0]['title'].split()[0]
                        mapNames.append(name)

                    delta = list(zip(mapNames, modifiedTags))
                    if len(delta) < 2:
                        for x, y in delta:
                            text_ru = strings.notiNewMap_ru.format(x, y)
                            text_en = strings.notiNewMap_en.format(x, y)
                        send_alert(text_ru, text_en)
                    else:
                        names = ' и '.join(
                            [', '.join(mapNames[:-1]), mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        names_en = ' and '.join(
                            [', '.join(mapNames[:-1]), mapNames[-1]] if len(mapNames) > 2 else mapNames)
                        text_ru = strings.notiNewMaps_ru.format(names)
                        text_en = strings.notiNewMaps_en.format(names_en)
                        send_alert(text_ru, text_en)
                currentTags = newTags
                time.sleep(60)
        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(text_ru, text_en):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.CSGOBETACHAT_EN]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        if chatID == config.CSGOBETACHAT:
            msg = bot.send_message(chatID, text_ru, parse_mode='html')
        else:
            msg = bot.send_message(chatID, text_en, parse_mode='html')
        bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    workshop_monitor()
