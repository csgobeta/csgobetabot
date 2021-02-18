# based on: https://github.com/ericwoolard/CS-GO-Update-Notifier

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from steam.client import SteamClient
import json
from datetime import datetime
import time
import traceback
import logging
import telebot

import config
import strings
from apps import file_manager


def setup():
    client = SteamClient()
    try:
        client.login(username=config.STEAM_USERNAME, password=config.STEAM_PASS)
    except:
        error_message = traceback.format_exc()
        now = str(datetime.now())
        print(f'{now} - Error:\n{error_message}\n\n\n')
        time.sleep(60)
        setup()
        
    check_for_updates(client)


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
                file_manager.updateJson(config.CACHE_FILE_PATH, currentPublicBuild, cache_key_list[0])
                send_alert(currentPublicBuild)

            if currentDPRBuild != cacheFile['dpr_build_ID']:
                file_manager.updateJson(config.CACHE_FILE_PATH, currentDPRBuild, cache_key_list[1])
                send_alert_dpr(currentDPRBuild)

            time.sleep(10)

        except AttributeError:
            error_message = traceback.format_exc()
            now = str(datetime.now())
            print(f'{now} - Error:\n{error_message}\n\n\n')
            client.logout()
            time.sleep(60)
            setup()


def send_alert(currentPublicBuild):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    text = strings.notiNewBuild_ru.format(currentBuild)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        bot.send_message(chatID, text, parse_mode='Markdown')

def send_alert_dpr(currentDPRBuild):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    text = strings.notiNewDPRBuild_ru.format(currentBuild)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        bot.send_message(chatID, text, parse_mode='Markdown')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(process)d %(message)s')
    setup()