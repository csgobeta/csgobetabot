import json
import logging
import telebot
import time
import config
from plugins import strings
from apps import file_manager
from apps.valve_api import ValveServersAPI
from apps.scrapper import PeakOnline, Monthly, GameVersion


api = ValveServersAPI()
peak_count = PeakOnline()
month_unique = Monthly()
gv = GameVersion()


def info_updater():
    while True:
        try:
            print('\nNew session started..\n')
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

            cache_key_list = []
            cache_value_list = []
            value_list = []
            playerCount = api.get_players()
            devCount = api.get_devs()
            overallData = api.get_status()
            for keys, values in cacheFile.items():
                cache_key_list.append(keys)
                cache_value_list.append(values)

            for data in [cacheFile['public_build_ID'], cacheFile['dpr_build_ID'], cacheFile['game_coordinator']]:
                value_list.append(data)
            for data in overallData[0:9]:
                value_list.append(data)
            for data in [playerCount, devCount, cacheFile['dev_all_time_peak'], peak_count.get_peak(), cacheFile['peak_all_time'], month_unique.get_unique()]:
                value_list.append(data)
            for data in gv.get_gameVer():
                value_list.append(data)
            for data in [cacheFile['graph_url'], cacheFile['graph_url2']]:
                value_list.append(data)
            for data in overallData[9:10]:
                value_list.append(data)

            for values, cache_values, cache_keys in zip(value_list, cache_value_list, cache_key_list):
                if values != cache_values:
                    file_manager.updateJson(
                        config.CACHE_FILE_PATH, values, cache_keys)

            if playerCount > cacheFile['peak_all_time']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, playerCount, cache_key_list[168])
                send_alert(playerCount, cache_key_list[16])

            if devCount > cacheFile['dev_all_time_peak']:
                file_manager.updateJson(
                    config.CACHE_FILE_PATH, devCount, cache_key_list[14])
                send_alert(devCount, cache_key_list[14])

            time.sleep(40)

        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(newVal, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == 'dev_all_time_peak':
        text_ru = strings.notiNewDevPeak_ru.format(newVal)
        text_en = strings.notiNewDevPeak_en.format(newVal)
    else:
        text_ru = strings.notiNewPlayerPeak_ru.format(newVal)
        text_en = strings.notiNewPlayerPeak_en.format(newVal)
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
    info_updater()
