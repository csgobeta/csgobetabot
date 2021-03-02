# -*- coding: utf-8 -*-

import time
from datetime import date, datetime, timedelta

import pytz
from babel.dates import format_datetime

import pandas as pd

import logging
import config

import telebot
from telebot import types
import random

from apps import file_manager
from apps.timer import Reset

from plugins import buttons
from plugins import strings

bot = telebot.TeleBot(config.BOT_TOKEN)
telebot.logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

tz = pytz.timezone('UTC')
tz_valve = pytz.timezone('America/Los_Angeles')
timer_drop = Reset()
CIS_lang_codes = ['ru', 'uk', 'be', 'uz', 'kk']


### Log setup ###


def log(message):   
    '''The bot sends log to log channel'''
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, message)

def log_inline(inline_query):
    '''The bot sends inline query to log channel'''
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, inline_query)


### Pull information ###


def get_server_status():
    '''Get the status of CS:GO servers'''
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    gcCache, slCache, sCache, piCache = cacheFile['game_coordinator'], cacheFile['sessionsLogon'], cacheFile['scheduler'], cacheFile['steam_community']

    array = [gcCache, slCache, sCache, piCache]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    gcRCache, slRCache, sRCache, piRCache = array_ru[0], array_ru[1], array_ru[2], array_ru[3]

    if gcCache != 'normal' or slCache != 'normal':
        tick = '❌'
    else:
        tick = '✅'

    status_text_en = strings.status_en.format(tick, gcCache, slCache, sCache, piCache, tsCache)
    status_text_ru = strings.status_ru.format(tick, gcRCache, slRCache, sRCache, piRCache, tsRCache)

    return status_text_en, status_text_ru

def get_mm_stats():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url']
    pcCache, scCache = cacheFile['online_player_count'], cacheFile['online_server_count']
    apCache, ssCache, spCache = cacheFile['active_player_count'], cacheFile['search_seconds_avg'], cacheFile['searching_players']
    p24Cache, paCache, uqCache = cacheFile['peak_24_hours'], cacheFile['peak_all_time'], cacheFile['unique_monthly']

    mm_text_en = strings.mm_en.format(url, scCache, pcCache, apCache, spCache, ssCache)
    mm_text_ru = strings.mm_ru.format(url, scCache, pcCache, apCache, spCache, ssCache)

    addInf_text_en = strings.additionalInfo_en.format(p24Cache, paCache, uqCache, tsCache)
    addInf_text_ru = strings.additionalInfo_ru.format(p24Cache, paCache, uqCache, tsRCache)

    mm_stats_text_en = mm_text_en + addInf_text_en
    mm_stats_text_ru = mm_text_ru + addInf_text_ru

    return mm_stats_text_en, mm_stats_text_ru

def get_devcount():
    '''Get the count of online devs'''
    tsCache, tsRCache, tsVCache = time_converter()[0], time_converter()[1], time_converter()[4]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url2']
    dcCache, dpCache = cacheFile['dev_player_count'], cacheFile['dev_all_time_peak']
    devcount_text_en = strings.devCount_en.format(url, dcCache, dpCache, tsCache, tsVCache)
    devcount_text_ru = strings.devCount_ru.format(url, dcCache, dpCache, tsRCache, tsVCache)
    return devcount_text_en, devcount_text_ru

def get_timer():
    '''Get drop cap reset time'''
    delta_days, delta_hours, delta_mins, delta_secs = timer_drop.get_time()
    timer_text_en = strings.timer_en.format(delta_days, delta_hours, delta_mins, delta_secs)
    timer_text_ru = strings.timer_ru.format(delta_days, delta_hours, delta_mins, delta_secs)
    return timer_text_en, timer_text_ru

def get_gameversion():
    '''Get the version of the game'''
    vdCache, vdRCache = time_converter()[2], time_converter()[3]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    cvCache, svCache, pvCache = cacheFile['client_version'], cacheFile['server_version'], cacheFile['patch_version']
    gameversion_text_en = strings.gameversion_en.format(pvCache, cvCache, svCache, vdCache)
    gameversion_text_ru = strings.gameversion_ru.format(pvCache, cvCache, svCache, vdRCache)
    return gameversion_text_en, gameversion_text_ru


### Send information ###   


def send_server_status(message):
    '''Send the status of CS:GO servers'''
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            status_text_en, status_text_ru = get_server_status()
            if message.from_user.language_code in CIS_lang_codes:
                text = status_text_ru
                markup = buttons.markup_ru
            else:
                text = status_text_en
                markup = buttons.markup_en
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)   

def send_mm_stats(message):
    '''Send the CS:GO matchmaking stats'''
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            mm_stats_text_en, mm_stats_text_ru = get_mm_stats()
            if message.from_user.language_code in CIS_lang_codes:
                text = mm_stats_text_ru
                markup = buttons.markup_ru
            else:
                text = mm_stats_text_en
                markup = buttons.markup_en
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)     

def send_devcount(message):
    '''Send the count of online devs'''
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            devcount_text_en, devcount_text_ru = get_devcount()
            if message.from_user.language_code in CIS_lang_codes:
                    text = devcount_text_ru
                    markup = buttons.markup_ru
            else:    
                    text = devcount_text_en
                    markup = buttons.markup_en
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def send_timer(message):
    '''Send drop cap reset time'''
    try:
        timer_text_en, timer_text_ru = get_timer()
        if message.from_user.language_code in CIS_lang_codes:
                text = timer_text_ru
                markup = buttons.markup_other_ru
        else:
                text = timer_text_en
                markup = buttons.markup_other_en
        bot.send_message(message.chat.id, text, reply_markup=markup) 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_gameversion(message):
    '''Send the version of the game'''
    try:
        gameversion_text_en, gameversion_text_ru = get_gameversion()
        if message.from_user.language_code in CIS_lang_codes:
                text = gameversion_text_ru
                markup = buttons.markup_other_ru
        else:
                text = gameversion_text_en
                markup = buttons.markup_other_en
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_about_problem_valve_api(message):
    '''In case the bot can't get Valve's API'''
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongAPI_ru
        markup = buttons.markup_ru       
    else:
        text = strings.wrongAPI_en
        markup = buttons.markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_maintenance(message):
    '''In case weekly server update (on Tuesdays)'''
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.maintenance_ru
        markup = buttons.markup_ru       
    else:
        text = strings.maintenance_en
        markup = buttons.markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_problem_valve_api_inline(inline_query):
    try:
        if inline_query.from_user.language_code in CIS_lang_codes:
            wrong_r = strings.wrongAPI_ru
            title_un = 'Нет данных'
            description_un = 'Не получилось связаться с API Valve'
        else:
            wrong_r = strings.wrongAPI_en
            title_un = 'No data'
            description_un = 'Unable to call Valve API'
        r = types.InlineQueryResultArticle('1', title_un, input_message_content = types.InputTextMessageContent(wrong_r), thumb_url='https://telegra.ph/file/b9d408e334795b014ee5c.jpg', description=description_un)
        bot.answer_inline_query(inline_query.id, [r], cache_time=5)
        log_inline(inline_query)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')

def send_about_maintenance_inline(inline_query):
    try:
        if inline_query.from_user.language_code in CIS_lang_codes:
            maintenance_r = strings.maintenance_ru
            title_maintenance = 'Нет данных'
            maintenance = 'Еженедельное тех. обслуживание.'
        else:
            maintenance_r = strings.maintenance_en
            title_maintenance = 'No data'
            maintenance = 'Weekly maintenance'
        r = types.InlineQueryResultArticle('1', title_maintenance, input_message_content = types.InputTextMessageContent(maintenance_r), thumb_url='https://telegra.ph/file/6120ece0aab30d8c59d07.jpg', description=maintenance)
        bot.answer_inline_query(inline_query.id, [r], cache_time=5)
        log_inline(inline_query)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')

def send_about_problem_bot(message):
    '''If anything goes wrong'''
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongBOT_ru
        markup = buttons.markup_ru
    else:
        text = strings.wrongBOT_en
        markup = buttons.markup_en  
    bot.send_message(message.chat.id, text, reply_markup=markup)

def other(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📂 Выберите одну из дополнительных функций:'
        markup = buttons.markup_other_ru
    else:
        text = '📂 Select one of the additional features:'
        markup = buttons.markup_other_en
    bot.send_message(message.chat.id, text, reply_markup=markup)


### Apps ###


def time_converter():
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    time_server = cacheFile['server_timestamp']
    tsCache = datetime.fromtimestamp(time_server, tz=tz).strftime('%a, %d %B %Y, %H:%M:%S')
    tsRCache = str(format_datetime(datetime.strptime(tsCache, '%a, %d %B %Y, %H:%M:%S'), 'EEE, dd MMMM yyyy, HH:mm:ss', locale='ru')).title()

    version_date = cacheFile['version_timestamp']
    vdCache = (datetime.fromtimestamp(version_date, tz=tz) + timedelta(hours=8)).strftime('%a, %d %B %Y, %H:%M:%S') 
    vdRCache = str(format_datetime(datetime.strptime(vdCache, '%a, %d %B %Y, %H:%M:%S'), 'EEE, dd MMMM yyyy, HH:mm:ss', locale='ru')).title()

    tsVCache = datetime.now(tz = tz_valve).strftime('%H:%M:%S, %d/%m/%y %Z')

    return tsCache, tsRCache, vdCache, vdRCache, tsVCache

def translate(data):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    en_list = ['low', 'medium', 'high', 'full', 'normal', 'surge', 'delayed', 'idle', 'offline', 'N/A', 'critical', 'internal server error']
    ru_list = ['низкая', 'средняя', 'высокая', 'полная', 'в норме', 'помехи', 'задержка', 'бездействие', 'офлайн', 'N/A', 'критическое', 'внутренняя ошибка сервера']
    for en, ru in zip(en_list, ru_list):
        if data in en:
            data_ru = ru
            return data_ru


### Guns archive ###


def get_gun_info(gun_id): 
    '''Get archived data about guns'''
    cacheFile = file_manager.readJson(config.GUNS_CACHE_FILE_PATH)
    raw_data = list(filter(lambda x:x['id'] == gun_id, cacheFile['data']))
    data = raw_data[0]
    key_list = []
    value_list = []
    for key, value in data.items():
        key_list.append(key)
        value_list.append(value)
    name, price = value_list[1], value_list[2]
    origin, origin_ru = value_list[3], ''
    clip_size, reserve_ammo = value_list[4], value_list[5]
    fire_rate, kill_reward, movement_speed = value_list[6], value_list[10], value_list[8]
    armor_penetration, accurate_range_stand, accurate_range_crouch = value_list[9], value_list[11], value_list[12]
    draw_time, reload_clip_ready, reload_fire_ready = value_list[13], value_list[14], value_list[15]
    origin_list_ru = ['Германия', 'Австрия', 'Италия', 'Швейцария', 'Чехия', 'Бельгия', 'Швеция', 'Израль',
                'Соединённые Штаты', 'Россия', 'Франция', 'Соединённое Королевство', 'Южная Африка']
    origin_list_en = ['Germany', 'Austria', 'Italy', 'Switzerland', 'Czech Republic', 'Belgium', 'Sweden', 'Israel',
                'United States', 'Russia', 'France', 'United Kingdom', 'South Africa']
    unarmored_damage_head, unarmored_damage_chest_and_arm, unarmored_damage_stomach, unarmored_damage_leg = value_list[16], value_list[17], value_list[18], value_list[19]
    armored_damage_head, armored_damage_chest_and_arm, armored_damage_stomach, armored_damage_leg = value_list[20], value_list[21], value_list[22], value_list[23]
    for en, ru in zip(origin_list_en, origin_list_ru):
        if origin in en:
            origin_ru = ru
    gun_data_text_en = strings.gun_data_en.format(name, origin, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                    armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                    armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                    armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    gun_data_text_ru = strings.gun_data_ru.format(name, origin_ru, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                    armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                    armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                    armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    return gun_data_text_en, gun_data_text_ru

def send_gun_info(message, gun_id):
    '''Send archived data about guns'''
    try:
        gun_data_text_en, gun_data_text_ru = get_gun_info(gun_id)
        if message.from_user.language_code in CIS_lang_codes:
                text = gun_data_text_ru
                markup = buttons.markup_guns_ru
        else:
                text = gun_data_text_en
                markup = buttons.markup_guns_en
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def guns(message):
    try:
        if message.from_user.language_code in CIS_lang_codes:
            text = '#️⃣ Выберите категорию, которая Вас интересует:'
            markup = buttons.markup_guns_ru
        else:
            text = '#️⃣ Select the category, that you are interested in:'
            markup = buttons.markup_guns_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def pistols(message):
    try:
        if message.from_user.language_code in CIS_lang_codes:
            text = '🔫 Выберите пистолет..'
            markup = buttons.markup_pistols_ru
        else:
            text = '🔫 Select the pistol..'
            markup = buttons.markup_pistols_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def smgs(message):
    try:
        if message.from_user.language_code in CIS_lang_codes:
            text = '🔫 Выберите пистолет-пулемёт..'
            markup = buttons.markup_smgs_ru
        else:
            text = '🔫 Select the SMG..'
            markup = buttons.markup_smgs_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def rifles(message):
    try:
        if message.from_user.language_code in CIS_lang_codes:
            text = '🔫 Выберите винтовку..'
            markup = buttons.markup_rifles_ru
        else:
            text = '🔫 Select the rifle..'
            markup = buttons.markup_rifles_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def heavy(message):
    try:
        if message.from_user.language_code in CIS_lang_codes:
            text = '🔫 Выберите тяжёлое оружие..'
            markup = buttons.markup_heavy_ru
        else:
            text = '🔫 Select the heavy gun..'
            markup = buttons.markup_heavy_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


### Data-centers ###


def dc(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            if message.from_user.language_code in CIS_lang_codes:
                text = '📶 Выберите регион, который Вам интересен, чтобы получить информацию о дата-центрах:'
                markup = buttons.markup_DC_ru
            else:
                text = '📶 Select the region, that you are interested in, to get information about the data centers:'
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def back(message):
    if message.from_user.language_code in CIS_lang_codes:
        markup = buttons.markup_ru
    else:
        markup = buttons.markup_en
    bot.send_message(message.chat.id, '👌', reply_markup=markup)

def dc_europe(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in CIS_lang_codes:
            text = '📍 Укажите регион...'
            markup = buttons.markup_DC_EU_ru            
        else:
            text = '📍 Specify the region...'
            markup = buttons.markup_DC_EU_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def dc_usa(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in CIS_lang_codes:
            text = '📍 Укажите регион...'
            markup = buttons.markup_DC_USA_ru
        else:
            text = '📍 Specify the region...'
            markup = buttons.markup_DC_USA_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def dc_asia(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in CIS_lang_codes:
            text = '📍 Укажите страну...'
            markup = buttons.markup_DC_Asia_ru
        else:
            text = '📍 Specify the country...'
            markup = buttons.markup_DC_Asia_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# Africa

def get_dc_africa():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    africa_dc = cacheFile['datacenters']['South Africa']
    capacity, load = africa_dc['capacity'], africa_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    africa_text_ru = strings.dc_africa_ru.format(load_ru, capacity_ru, tsRCache)
    africa_text_en = strings.dc_africa_en.format(load, capacity, tsCache)           
    return africa_text_en, africa_text_ru

def send_dc_africa(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            africa_text_en, africa_text_ru = get_dc_africa()
            if message.from_user.language_code in CIS_lang_codes:
                text = africa_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = africa_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# Australia 

def get_dc_australia():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    australia_dc = cacheFile['datacenters']['Australia']
    capacity, load = australia_dc['capacity'], australia_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    australia_text_ru = strings.dc_australia_ru.format(load_ru, capacity_ru, tsRCache)
    australia_text_en = strings.dc_australia_en.format(load, capacity, tsCache)           
    return australia_text_en, australia_text_ru

def send_dc_australia(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            australia_text_en, australia_text_ru = get_dc_australia()
            if message.from_user.language_code in CIS_lang_codes:
                text = australia_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = australia_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# Europe

def get_dc_eu_north():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    sweden_dc = cacheFile['datacenters']['EU North']
    capacity, load = sweden_dc['capacity'], sweden_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    eu_north_text_ru = strings.dc_north_eu_ru.format(load_ru, capacity_ru, tsRCache)
    eu_north_text_en = strings.dc_north_eu_en.format(load, capacity, tsCache)
    return eu_north_text_en, eu_north_text_ru

def send_dc_eu_north(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_north_text_en, eu_north_text_ru = get_dc_eu_north()
            if message.from_user.language_code in CIS_lang_codes:
                text = eu_north_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = eu_north_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_eu_west():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    germany_dc = cacheFile['datacenters']['EU West']
    spain_dc = cacheFile['datacenters']['Spain']
    capacity, load = germany_dc['capacity'], germany_dc['load']
    capacity_secondary, load_secondary = spain_dc['capacity'], spain_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3]
    eu_west_text_ru = strings.dc_west_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_west_text_en = strings.dc_west_eu_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_west_text_en, eu_west_text_ru

def send_dc_eu_west(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_west_text_en, eu_west_text_ru = get_dc_eu_west()
            if message.from_user.language_code in CIS_lang_codes:
                text = eu_west_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = eu_west_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_eu_east():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    austria_dc = cacheFile['datacenters']['EU East']
    poland_dc = cacheFile['datacenters']['Poland']
    capacity, load = austria_dc['capacity'], austria_dc['load']
    capacity_secondary, load_secondary = poland_dc['capacity'], poland_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3]
    eu_east_text_ru = strings.dc_east_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_east_text_en = strings.dc_east_eu_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_east_text_en, eu_east_text_ru

def send_dc_eu_east(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_east_text_en, eu_east_text_ru = get_dc_eu_east()
            if message.from_user.language_code in CIS_lang_codes:
                text = eu_east_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = eu_east_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)   

# USA

def get_dc_usa_north():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    chicago_dc = cacheFile['datacenters']['US Northcentral']
    sterling_dc = cacheFile['datacenters']['US Northeast']
    moseslake_dc = cacheFile['datacenters']['US Northwest']
    capacity, load = chicago_dc['capacity'], chicago_dc['load']
    capacity_secondary, load_secondary = sterling_dc['capacity'], sterling_dc['load']
    capacity_tertiary, load_tertiary = moseslake_dc['capacity'], moseslake_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5] 
    usa_north_text_ru = strings.dc_north_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    usa_north_text_en = strings.dc_north_us_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return usa_north_text_en, usa_north_text_ru

def send_dc_usa_north(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_north_text_en, usa_north_text_ru = get_dc_usa_north()
            if message.from_user.language_code in CIS_lang_codes:        
                text = usa_north_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = usa_north_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)        
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_usa_south():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    losangeles_dc = cacheFile['datacenters']['US Southwest']
    atlanta_dc = cacheFile['datacenters']['US Southeast']
    capacity, load = losangeles_dc['capacity'], losangeles_dc['load']
    capacity_secondary, load_secondary = atlanta_dc['capacity'], atlanta_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3]    
    usa_south_text_ru = strings.dc_south_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    usa_south_text_en = strings.dc_south_us_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return usa_south_text_en, usa_south_text_ru

def send_dc_usa_south(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_south_text_en, usa_south_text_ru = get_dc_usa_south()
            if message.from_user.language_code in CIS_lang_codes:        
                text = usa_south_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = usa_south_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# South America

def get_dc_south_america():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    brazil_dc = cacheFile['datacenters']['Brazil']
    chile_dc = cacheFile['datacenters']['Chile']
    peru_dc = cacheFile['datacenters']['Peru']
    argentina_dc = cacheFile['datacenters']['Argentina']
    capacity, load = brazil_dc['capacity'], brazil_dc['load']
    capacity_secondary, load_secondary = chile_dc['capacity'], chile_dc['load']
    capacity_tertiary, load_tertiary = peru_dc['capacity'], peru_dc['load']
    capacity_quaternary, load_quaternary = argentina_dc['capacity'], argentina_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary, capacity_quaternary, load_quaternary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary_ru, load_quaternary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5], array_ru[6], array_ru[7] 
    south_america_text_ru = strings.dc_south_america_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, load_quaternary_ru, capacity_quaternary_ru, tsRCache)
    south_america_text_en = strings.dc_south_america_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, load_quaternary, capacity_quaternary, tsCache)
    return south_america_text_en, south_america_text_ru

def send_dc_south_america(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            south_america_text_en, south_america_text_ru = get_dc_south_america()
            if message.from_user.language_code in CIS_lang_codes:
                text = south_america_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = south_america_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# Asia

def get_dc_india():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    mumbai_dc = cacheFile['datacenters']['India']
    chennai_dc = cacheFile['datacenters']['India East']
    capacity, load = mumbai_dc['capacity'], mumbai_dc['load']
    capacity_secondary, load_secondary = chennai_dc['capacity'], chennai_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3]
    india_text_ru = strings.dc_india_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    india_text_en = strings.dc_india_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return india_text_en, india_text_ru

def send_dc_india(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            india_text_en, india_text_ru = get_dc_india()
            if message.from_user.language_code in CIS_lang_codes:  
                text = india_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = india_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_japan():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    japan_dc = cacheFile['datacenters']['Japan']
    capacity, load = japan_dc['capacity'], japan_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    japan_text_ru = strings.dc_japan_ru.format(load_ru, capacity_ru, tsRCache)
    japan_text_en = strings.dc_japan_en.format(load, capacity, tsCache)
    return japan_text_en, japan_text_ru

def send_dc_japan(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            japan_text_en, japan_text_ru = get_dc_japan()
            if message.from_user.language_code in CIS_lang_codes:
                text = japan_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = japan_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)        
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_china():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    shanghai_dc = cacheFile['datacenters']['China Shanghai']
    tianjin_dc = cacheFile['datacenters']['China Tianjin']
    guangzhou_dc = cacheFile['datacenters']['China Guangzhou']
    capacity, load = shanghai_dc['capacity'], shanghai_dc['load']
    capacity_secondary, load_secondary = tianjin_dc['capacity'], tianjin_dc['load']
    capacity_tertiary, load_tertiary = guangzhou_dc['capacity'], guangzhou_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5] 
    china_text_ru = strings.dc_china_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    china_text_en = strings.dc_china_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return china_text_en, china_text_ru

def send_dc_china(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            china_text_en, china_text_ru = get_dc_china()
            if message.from_user.language_code in CIS_lang_codes:
                text = china_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = china_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message) 
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_emirates():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    emirates_dc = cacheFile['datacenters']['Emirates']
    capacity, load = emirates_dc['capacity'], emirates_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1] 
    emirates_text_ru = strings.dc_emirates_ru.format(load_ru, capacity_ru, tsRCache)
    emirates_text_en = strings.dc_emirates_en.format(load, capacity, tsCache)           
    return emirates_text_en, emirates_text_ru

def send_dc_emirates(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            emirates_text_en, emirates_text_ru = get_dc_emirates()
            if message.from_user.language_code in CIS_lang_codes:
                text = emirates_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = emirates_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_singapore():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    singapore_dc = cacheFile['datacenters']['Singapore']
    capacity, load = singapore_dc['capacity'], singapore_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1] 
    singapore_text_ru = strings.dc_singapore_ru.format(load_ru, capacity_ru, tsRCache)
    singapore_text_en = strings.dc_singapore_en.format(load, capacity, tsCache)           
    return singapore_text_en, singapore_text_ru

def send_dc_singapore(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            singapore_text_en, singapore_text_ru = get_dc_singapore()
            if message.from_user.language_code in CIS_lang_codes:
                text = singapore_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = singapore_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def get_dc_hong_kong():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    hongkong_dc = cacheFile['datacenters']['Hong Kong']
    capacity, load = hongkong_dc['capacity'], hongkong_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1] 
    hong_kong_text_ru = strings.dc_hong_kong_ru.format(load_ru, capacity_ru, tsRCache)
    hong_kong_text_en = strings.dc_hong_kong_en.format(load, capacity, tsCache)           
    return hong_kong_text_en, hong_kong_text_ru

def send_dc_hong_kong(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            hong_kong_text_en, hong_kong_text_ru = get_dc_hong_kong()
            if message.from_user.language_code in CIS_lang_codes:
                text = hong_kong_text_ru
                markup = buttons.markup_DC_ru
            else:
                text = hong_kong_text_en
                markup = buttons.markup_DC_en
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)



### Inline-mode ###


# Default
@bot.inline_handler(lambda query: len(query.query) == 0)
def default_inline(inline_query):
    '''Inline mode'''
    log_inline(inline_query)
    try:
        status_text_en, status_text_ru = get_server_status()
        mm_stats_text_en, mm_stats_text_ru = get_mm_stats()
        devcount_text_en, devcount_text_ru = get_devcount()
        timer_text_en, timer_text_ru = get_timer()
        gameversion_text_en, gameversion_text_ru = get_gameversion()
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        wsCache = cacheFile['valve_webapi']
        if wsCache == 'normal':
            thumbs = ['https://telegra.ph/file/8b640b85f6d62f8ed2900.jpg', 'https://telegra.ph/file/57ba2b279c53d69d72481.jpg',
                        'https://telegra.ph/file/24b05cea99de936fd12bf.jpg', 'https://telegra.ph/file/6948255408689d2f6a472.jpg',
                        'https://telegra.ph/file/82d8df1e9f5140da70232.jpg']
            if inline_query.from_user.language_code in CIS_lang_codes:
                data = [status_text_ru, mm_stats_text_ru, devcount_text_ru, timer_text_ru, gameversion_text_ru]
                titles = ['Состояние серверов', 'Статистика ММ', 'Бета-версия', 'Сброс ограничений', 'Версия игры']
                descriptions = ['Проверить доступность серверов', 'Посмотреть количество онлайн игроков', 'Узнать количество онлайн разработчиков',
                                'Время до сброса ограничений опыта и дропа', 'Проверить последнюю версию игры']
            else:
                data = [status_text_en, mm_stats_text_ru, devcount_text_en, timer_text_en, gameversion_text_en]
                titles = ['Server status', 'MM stats', 'Beta version', 'Drop cap reset', 'Game version']
                descriptions = ['Check the availability of the servers', 'Check the count of online players', 'Show the count of in-game developers',
                                'Time left until experience and drop cap reset', 'Check the latest game version']
            results = []
            for data, tt, desc, thumb in zip(data, titles, descriptions, thumbs):
                results.append(types.InlineQueryResultArticle(random.randint(0,9999), tt, input_message_content=types.InputTextMessageContent(data, parse_mode='html'), thumb_url=thumb, description=desc))
            bot.answer_inline_query(inline_query.id, results, cache_time=5)
        elif wsCache == 'maintenance':
            send_about_maintenance_inline(inline_query)
        else:
            send_about_problem_valve_api_inline(inline_query)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')

# DC
@bot.inline_handler(lambda query: len(query.query) >= 0)
def inline_dc(inline_query):
    log_inline(inline_query)
    try:
        status_text_en, status_text_ru = get_server_status()
        mm_stats_text_en, mm_stats_text_ru = get_mm_stats()
        devcount_text_en, devcount_text_ru = get_devcount()
        timer_text_en, timer_text_ru = get_timer()
        gameversion_text_en, gameversion_text_ru = get_gameversion()
        eu_north_text_en, eu_north_text_ru = get_dc_eu_north()
        eu_east_text_en, eu_east_text_ru = get_dc_eu_east()
        eu_west_text_en, eu_west_text_ru = get_dc_eu_west()
        usa_north_text_en, usa_north_text_ru = get_dc_usa_north()
        usa_south_text_en, usa_south_text_ru = get_dc_usa_south()
        china_text_en, china_text_ru = get_dc_china()
        emirates_text_en, emirates_text_ru = get_dc_emirates()
        hong_kong_text_en, hong_kong_text_ru = get_dc_hong_kong()
        india_text_en, india_text_ru = get_dc_india()
        japan_text_en, japan_text_ru = get_dc_japan()
        singapore_text_en, singapore_text_ru = get_dc_singapore()
        australia_text_en, australia_text_ru = get_dc_australia()
        africa_text_en, africa_text_ru = get_dc_africa()            
        south_america_text_en, south_america_text_ru = get_dc_south_america()
        cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
        wsCache = cacheFile['valve_webapi']
        if wsCache == 'normal':
            thumbs = ['https://telegra.ph/file/8b640b85f6d62f8ed2900.jpg', 'https://telegra.ph/file/57ba2b279c53d69d72481.jpg',
                        'https://telegra.ph/file/24b05cea99de936fd12bf.jpg', 'https://telegra.ph/file/6948255408689d2f6a472.jpg',
                        'https://telegra.ph/file/82d8df1e9f5140da70232.jpg', 'https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg',
                        'https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', 'https://telegra.ph/file/0b209e65c421910419f34.jpg',
                        'https://telegra.ph/file/b2213992b750940113b69.jpg', 'https://telegra.ph/file/11b6601a3e60940d59c88.jpg',
                        'https://telegra.ph/file/1c2121ceec5d1482173d5.jpg', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg',
                        'https://telegra.ph/file/4d269cb98aadaae391024.jpg', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg',
                        'https://telegra.ph/file/06119c30872031d1047d0.jpg', 'https://telegra.ph/file/06119c30872031d1047d0.jpg',
                        'https://telegra.ph/file/5dc6beef1556ea852284c.jpg', 'https://telegra.ph/file/12628c8193b48302722e8.jpg',
                        'https://telegra.ph/file/60f8226ea5d72815bef57.jpg']
            tags = [strings.status_tags, strings.mm_tags, strings.dev_count_tags, strings.cap_reset_tags, strings.gameversion_tags,
                    strings.chinese_tags, strings.emirati_tags, strings.hong_kongese_tags, strings.indian_tags, strings.japanese_tags,
                    strings.singaporean_tags, strings.north_european_tags, strings.east_european_tags, strings.west_european_tags,
                    strings.northern_usa_tags, strings.southern_usa_tags, strings.australian_tags, strings.african_tags, strings.african_tags]
            if inline_query.from_user.language_code in CIS_lang_codes:
                data = [status_text_ru, mm_stats_text_ru, devcount_text_ru, timer_text_ru, gameversion_text_ru, china_text_ru, emirates_text_ru,
                        hong_kong_text_ru, india_text_ru, japan_text_ru, singapore_text_ru, eu_north_text_ru, eu_east_text_ru, eu_west_text_ru,
                        usa_north_text_ru, usa_south_text_ru, australia_text_ru, africa_text_ru, south_america_text_ru]
                titles = ['Состояние серверов', 'Статистика ММ', 'Бета-версия', 'Сброс ограничений', 'Версия игры', 'Китайские ДЦ', 'Эмиратский ДЦ',
                        'Гонконгский ДЦ', 'Индийские ДЦ', 'Японский ДЦ', 'Сингапурский ДЦ', 'Североевропейский ДЦ', 'Восточноевропейские ДЦ',
                        'Западноевропейские ДЦ', 'ДЦ северной части США', 'ДЦ южной части США', 'Австралийский ДЦ', 'Африканский ДЦ', 'Южноамериканские ДЦ']
                descriptions = ['Проверить доступность серверов', 'Посмотреть количество онлайн игроков', 'Узнать количество онлайн разработчиков',
                                'Время до сброса ограничений опыта и дропа', 'Проверить последнюю версию игры']
                for _ in range(len(data)-len(descriptions)): descriptions.append('Проверить состояние')
            else:
                data = [status_text_en, mm_stats_text_ru, devcount_text_en, timer_text_en, gameversion_text_en, china_text_en, emirates_text_en,
                        hong_kong_text_en, india_text_en, japan_text_en, singapore_text_en, eu_north_text_en, eu_east_text_en, eu_west_text_en,
                        usa_north_text_en, usa_south_text_en, australia_text_en, africa_text_en, south_america_text_en]
                titles = ['Server status', 'MM stats', 'Beta version', 'Drop cap reset', 'Game version', 'Chinese DC', 'Emirati DC', 'Hong Kongese DC',
                        'Indian DC', 'Japanese DC', 'Singaporean DC', 'North European DC', 'East European DC', 'West European DC', 'Northern USA DC',
                        'Southern USA DC', 'Australian DC', 'African DC', 'South American DC']
                descriptions = ['Check the availability of the servers', 'Check the count of online players', 'Show the count of in-game developers',
                                'Time left until experience and drop cap reset', 'Check the latest game version']
                for _ in range(len(data)-len(descriptions)): descriptions.append('Check the status')
            results = []
            for data, tt, desc, thumb, tagList in zip(data, titles, descriptions, thumbs, tags):
                for tag in tagList:
                    if inline_query.query == tag:
                        results.append(types.InlineQueryResultArticle(random.randint(0,9999), tt, input_message_content=types.InputTextMessageContent(data, parse_mode='html'), thumb_url=thumb, description=desc))
            bot.answer_inline_query(inline_query.id, results, cache_time=5)
        elif wsCache == 'maintenance':
            send_about_maintenance_inline(inline_query)
        else:
            send_about_problem_valve_api_inline(inline_query)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')


### Commands setup ###


@bot.message_handler(commands=['start'])
def welcome(message):
    '''First bot's message'''
    data = pd.read_csv(config.USER_DB_FILE_PATH)
    if not data['UserID'].isin([message.from_user.id]).any():
        new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id, message.from_user.language_code]], columns=['Name', 'UserID', 'Language'])
        pd.concat([data, new_data]).to_csv(config.USER_DB_FILE_PATH, index=False)
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdStart_ru.format(message.from_user.first_name)
            markup = buttons.markup_ru
        else:
            text = strings.cmdStart_en.format(message.from_user.first_name)
            markup = buttons.markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

@bot.message_handler(commands=['feedback'])
def leave_feedback(message):
    '''Send feedback'''
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdFeedback_ru 
        else:
            text = strings.cmdFeedback_en
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=buttons.markup_del)
        bot.register_next_step_handler(message, get_feedback)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

def get_feedback(message):
    '''Get feedback from users'''
    if message.text == '/cancel':
        log(message)
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        bot.send_message(message.chat.id, '👍', reply_markup=markup)

    else:
        bot.send_message(config.OWNER, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', parse_mode='html', disable_notification=True)
        bot.forward_message(config.OWNER, message.chat.id, message.message_id)
        
        if not config.TEST_MODE:
            bot.send_message(config.AQ, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', parse_mode='html', disable_notification=True)
            bot.forward_message(config.AQ, message.chat.id, message.message_id)

        if message.from_user.language_code in CIS_lang_codes:
            text = 'Отлично! Ваше сообщение отправлено.'
            markup = buttons.markup_ru
        else:
            text = 'Awesome! Your message has been sent.'
            markup = buttons.markup_en

        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id,reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    '''/help message'''
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdHelp_ru
            markup = buttons.markup_ru
        else:
            text = strings.cmdHelp_en
            markup = buttons.markup_en
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

@bot.message_handler(commands=['delkey'])
def delete_keyboard(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, '👍', reply_markup=buttons.markup_del)
    time.sleep(10)
    bot.delete_message(message.chat.id, message.message_id+1)
        
@bot.message_handler(content_types=['text'])
def answer(message):
    '''Answer of the bot'''
    log(message)
    try:
        if message.chat.type == 'private':
            bot.send_chat_action(message.chat.id, 'typing')

            data = pd.read_csv(config.USER_DB_FILE_PATH)
            if not data['UserID'].isin([message.from_user.id]).any():
                new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id, message.from_user.language_code]], columns=['Name', 'UserID', 'Language'])
                pd.concat([data, new_data]).to_csv(config.USER_DB_FILE_PATH, index=False)

            if message.text.lower() in strings.status_tags:
                send_server_status(message)

            elif message.text.lower() in strings.mm_tags:
                send_mm_stats(message)

            elif message.text.lower() in strings.dev_count_tags:
                send_devcount(message)
    
            elif message.text.lower() == 'other' or message.text.lower() == 'другое':
                other(message)

            elif message.text.lower() in strings.cap_reset_tags:
                send_timer(message)

            elif message.text.lower() in strings.gameversion_tags:
                send_gameversion(message)

            elif message.text.lower() in strings.gun_tags:
                guns(message)

            elif message.text.lower() in strings.gun_name_list:
                for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
                    if message.text.lower() == gName:
                        send_gun_info(message, gId)

            elif message.text.lower() == 'pistols' or message.text.lower() == 'пистолеты':
                pistols(message)

            elif message.text.lower() == 'smgs' or message.text.lower() == 'пистолеты-пулемёты':
                smgs(message)

            elif message.text.lower() == 'rifles' or message.text.lower() == 'винтовки':
                rifles(message)

            elif message.text.lower() == 'heavy' or message.text.lower() == 'тяжёлое оружие':
                heavy(message)

            elif message.text.lower() in strings.dc_tags:
                dc(message)

            elif message.text.lower() in strings.african_tags:
                send_dc_africa(message)

            elif message.text.lower() in strings.australian_tags:
                send_dc_australia(message)

            elif message.text.lower() in strings.european_tags:
                dc_europe(message)

            elif message.text.lower() in strings.asian_tags:
                dc_asia(message)

            elif message.text.lower() in strings.american_tags:
                dc_usa(message)

            elif message.text.lower() in strings.south_american_tags:
                send_dc_south_america(message)

            elif message.text.lower() in strings.northern_usa_tags:
                send_dc_usa_north(message)

            elif message.text.lower() in strings.southern_usa_tags:
                send_dc_usa_south(message)

            elif message.text.lower() in strings.north_european_tags:
                send_dc_eu_north(message)

            elif message.text.lower() in strings.west_european_tags:
                send_dc_eu_west(message)

            elif message.text.lower() in strings.east_european_tags:
                send_dc_eu_east(message)

            elif message.text.lower() in strings.indian_tags:
                send_dc_india(message)

            elif message.text.lower() in strings.japanese_tags:
                send_dc_japan(message)

            elif message.text.lower() in strings.chinese_tags:
                send_dc_china(message)

            elif message.text.lower() in strings.emirati_tags:
                send_dc_emirates(message)

            elif message.text.lower() in strings.singaporean_tags:
                send_dc_singapore(message)

            elif message.text.lower() in strings.hong_kongese_tags:
                send_dc_hong_kong(message)

            elif message.text == '⏪ Back' or message.text == '⏪ Назад':
                back(message)

            elif message.text == '⏪ Bаck' or message.text == '⏪ Нaзад':
                dc(message)
                
            elif message.text == '⏪ Bасk' or message.text == '⏪ Haзад':
                guns(message)
                
            elif message.text == '⏪ Вack' or message.text == '⏪ Haзaд':
                other(message)

            else:
                if message.from_user.language_code in CIS_lang_codes:
                    text = strings.unknownRequest_ru
                    markup = buttons.markup_ru
                else: 
                    text = strings.unknownRequest_en
                    markup = buttons.markup_en

                bot.send_message(message.chat.id, text, reply_markup=markup)
                
        else:
            if message.from_user.id == 777000:
                if message.forward_from_chat.id == config.CSGOBETACHANNEL and 'Обновлены файлы локализации' in message.text:
                    bot.send_sticker(config.CSGOBETACHAT, 'CAACAgIAAxkBAAID-l_9tlLJhZQSgqsMUAvLv0r8qhxSAAIKAwAC-p_xGJ-m4XRqvoOzHgQ', reply_to_message_id=message.message_id)
    
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')


### Polling ###


bot.polling(True)