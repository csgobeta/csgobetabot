import time
from datetime import date, datetime, timedelta
from apps import file_manager

import config

import pytz
from babel.dates import format_datetime

tz = pytz.timezone('UTC')
tz_valve = pytz.timezone('America/Los_Angeles')

def time_converter():
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    time_server = cacheFile['server_timestamp']
    tsCache = datetime.fromtimestamp(time_server, tz=tz).strftime('%a, %d %B %Y, %H:%M:%S')
    tsRCache = str(format_datetime(datetime.strptime(tsCache, '%a, %d %B %Y, %H:%M:%S'), 'EEE, dd MMMM yyyy, HH:mm:ss', locale='ru')).title()

    version_date = cacheFile['version_timestamp']
    vdCache = (datetime.fromtimestamp(version_date, tz=tz) + timedelta(hours=8)).strftime('%a, %d %B %Y, %H:%M:%S') 
    vdRCache = str(format_datetime(datetime.strptime(vdCache, '%a, %d %B %Y, %H:%M:%S'), 'EEE, dd MMMM yyyy, HH:mm:ss', locale='ru')).title()

    tsVCache = datetime.now(tz = tz_valve).strftime('%a, %d %B %Y, %H:%M:%S %Z')

    return tsCache, tsRCache, vdCache, vdRCache, tsVCache

def translate(data):
    en_list = ['low', 'medium', 'high', 'full', 'normal', 'surge', 'delayed', 'idle', 'offline', 'N/A', 'critical', 'internal server error']
    ru_list = ['низкая', 'средняя', 'высокая', 'полная', 'в норме', 'помехи', 'задержка', 'бездействие', 'офлайн', 'N/A', 'критическое', 'внутренняя ошибка сервера']
    for en, ru in zip(en_list, ru_list):
        if data in en:
            data_ru = ru
            return data_ru