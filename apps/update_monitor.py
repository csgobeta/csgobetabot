# based on: https://github.com/ericwoolard/CS-GO-Update-Notifier

import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from apps import file_manager
from plugins import strings
import config
import time
from datetime import datetime
import logging
import telebot
from steam.client import SteamClient


def setup():
    client = SteamClient()
    try:
        client.login(username=config.STEAM_USERNAME,
                     password=config.STEAM_PASS)
        check_for_updates(client)
    except Exception as e:
        print(f' - Error:\n{e}\n\n\n')


def check_for_updates(client):
    while True:
        try:
            currentPublicBuild = 0
            currentDPRBuild = 0

            for keys, values in client.get_product_info(apps=[730], timeout=15).items():
                for k, v in values.items():
                    currentPublicBuild = v['depots']['branches']['public']['buildid']
                    currentDPRBuild = v['depots']['branches']['dpr']['buildid']

            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            cache_key_list = []
            for keys, values in cacheFile.items():
                cache_key_list.append(keys)

            if currentPublicBuild != cacheFile['public_build_ID']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentPublicBuild, cache_key_list[0])
                send_alert(currentPublicBuild, cache_key_list[0])

            if currentDPRBuild != cacheFile['dpr_build_ID']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, currentDPRBuild, cache_key_list[1])
                send_alert(currentDPRBuild, cache_key_list[1])

            time.sleep(10)

        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == 'public_build_ID':
        text = strings.notiNewBuild_ru.format(newVal)
    else:
        text = strings.notiNewDPRBuild_ru.format(newVal)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        msg = bot.send_message(chatID, text, parse_mode='html')
        if chatID != config.AQ:
            bot.pin_chat_message(msg.chat.id, msg.id, disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    setup()
