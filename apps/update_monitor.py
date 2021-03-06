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
import logging
import telebot
import subprocess
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
            for keys, values in client.get_product_info(apps=[730], timeout=15).items():
                for k, v in values.items():
                    currentPublicBuild = v['depots']['branches']['public']['buildid']
                    currentDPRBuild = v['depots']['branches']['dpr']['buildid']

            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            cache_key_list = []
            for keys, values in cacheFile.items():
                cache_key_list.append(keys)

            if currentPublicBuild != cacheFile['public_build_ID']:
                subprocess.call(['steamcmd', '+login', config.STEAM_USERNAME, config.STEAM_PASS, '+app_update 730', '+quit'])
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
        text_ru = strings.notiNewBuild_ru.format(newVal)
        text_en = strings.notiNewBuild_en.format(newVal)
    else:
        text_ru = strings.notiNewDPRBuild_ru.format(newVal)
        text_en = strings.notiNewDPRBuild_en.format(newVal)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.CSGOBETACHAT_EN, config.CSGOBETA_DEV]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        if chatID == config.CSGOBETACHAT:
            msg = bot.send_message(chatID, text_ru, parse_mode='html')
        else:
            msg = bot.send_message(chatID, text_en, parse_mode='html')
        if chatID != config.CSGOBETA_DEV:
            bot.pin_chat_message(msg.chat.id, msg.id,
                                 disable_notification=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    setup()
