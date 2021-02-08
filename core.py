import json
from datetime import datetime
import time
import traceback
import logging
import config
import telebot
import strings

from apps import file_manager
from apps.valve_api import ValveServersAPI
from apps.scrapper import PeakOnline, Monthly, CSGOGameCoordinator, GameVersion

api = ValveServersAPI()
peak_count = PeakOnline()
month_unique = Monthly()
gc = CSGOGameCoordinator()
gv = GameVersion()

def info_updater():
    while True:
        try:
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

            cache_key_list = []
            cache_value_list = []
            for keys, values in cacheFile.items():
                cache_key_list.append(keys)
                cache_value_list.append(values)
                
            value_list = [ cacheFile['build_ID'], gc.get_status(), api.check_status(), api.get_status()[1], api.get_players(), api.get_status()[4],
            api.get_status()[0], api.get_status()[2], api.get_status()[3], api.get_status()[5], api.get_status()[6], api.get_devs(),
            cacheFile['dev_all_time_peak'], peak_count.get_peak(), cacheFile['peak_all_time'], month_unique.get_unique(),
            gv.get_gameVer()[0], gv.get_gameVer()[1], gv.get_gameVer()[2], gv.get_gameVer()[3] ]

            for values, cache_values, cache_keys in zip(value_list, cache_value_list, cache_key_list):
                if values != cache_values:
                    file_manager.updateJson(config.CACHE_FILE_PATH, values, cache_keys)

            if api.get_players() > cacheFile['peak_all_time']:
                file_manager.updateJson(config.CACHE_FILE_PATH, api.get_players(), cache_key_list[13])
                send_alert_players(api.get_players())

            if api.get_devs() > cacheFile['dev_all_time_peak']:
                file_manager.updateJson(config.CACHE_FILE_PATH, api.get_devs(), cache_key_list[11])
                send_alert(api.get_devs())

            time.sleep(40)

        except AttributeError:
            error_message = traceback.format_exc()
            now = str(datetime.now())
            print(f'{now} - Error:\n{error_message}\n\n\n')
            time.sleep(60)
            info_updater()
            
def send_alert_players(newVal):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    text = strings.notiNewPlayerPeak_ru.format(newVal)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        bot.send_message(chatID, text, parse_mode='Markdown')
            
def send_alert_devs(newVal):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    text = strings.notiNewDevPeak_ru.format(newVal)
    if not config.TEST_MODE:
        chat_list = [config.CSGOBETACHAT, config.AQ]
    else:
        chat_list = [config.OWNER]
    for chatID in chat_list:
        bot.send_message(chatID, text, parse_mode='Markdown')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(process)d %(message)s')
    info_updater()