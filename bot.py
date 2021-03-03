# -*- coding: utf-8 -*-

import time
import pandas as pd

import telebot
from telebot import types

import logging
import random

import config
from plugins import strings
from plugins import buttons
from plugins import get_data
from plugins.addons import translate
from apps import file_manager

bot = telebot.TeleBot(config.BOT_TOKEN)
telebot.logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
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


### Send information ###   


def send_server_status(message):
    '''Send the status of CS:GO servers'''
    try:
        status_text_en, status_text_ru = get_data.server_status()
        if message.from_user.language_code in CIS_lang_codes:
            text = status_text_ru
            markup = buttons.markup_ss_ru
        else:
            text = status_text_en
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, server_stats_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_mm_stats(message):
    '''Send CS:GO matchamaking statistics'''
    try:
        mm_stats_text_en, mm_stats_text_ru = get_data.mm_stats()
        if message.from_user.language_code in CIS_lang_codes:
            text = mm_stats_text_ru
            markup = buttons.markup_ss_ru
        else:
            text = mm_stats_text_en
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, server_stats_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_devcount(message):
    '''Send the count of online devs'''
    try:
        devcount_text_en, devcount_text_ru = get_data.devcount()
        if message.from_user.language_code in CIS_lang_codes:
            text = devcount_text_ru
            markup = buttons.markup_extra_ru
        else:    
            text = devcount_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_timer(message):
    '''Send drop cap reset time'''
    try:
        timer_text_en, timer_text_ru = get_data.timer()
        if message.from_user.language_code in CIS_lang_codes:
            text = timer_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = timer_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, extra_features_process) 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_gameversion(message):
    '''Send the version of the game'''
    try:
        gameversion_text_en, gameversion_text_ru = get_data.gameversion()
        if message.from_user.language_code in CIS_lang_codes:
            text = gameversion_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = gameversion_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
        bot.register_next_step_handler(msg, extra_features_process)
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

def send_about_maintenance_inline(inline_query):
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

def send_about_problem_bot(message):
    '''If anything goes wrong'''
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongBOT_ru
        markup = buttons.markup_ru
    else:
        text = strings.wrongBOT_en
        markup = buttons.markup_en  
    bot.send_message(message.chat.id, text, reply_markup=markup)


### Guns archive ###


def send_gun_info(message, gun_id):
    '''Send archived data about guns'''
    try:
        gun_data_text_en, gun_data_text_ru = get_data.gun_info(gun_id)
        if message.from_user.language_code in CIS_lang_codes:
            text = gun_data_text_ru
            markup = buttons.markup_guns_ru
        else:
            text = gun_data_text_en
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, guns_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def guns(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '#️⃣ Выберите категорию, которая Вас интересует:'
        markup = buttons.markup_guns_ru
    else:
        text = '#️⃣ Select the category, that you are interested in:'
        markup = buttons.markup_guns_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
    bot.register_next_step_handler(msg, guns_process)

def guns_process(message):
    if message.text.lower() == 'pistols' or message.text.lower() == 'пистолеты':
        pistols(message)
    elif message.text.lower() == 'smgs' or message.text.lower() == 'пистолеты-пулемёты':
        smgs(message)
    elif message.text.lower() == 'rifles' or message.text.lower() == 'винтовки':
        rifles(message)
    elif message.text.lower() == 'heavy' or message.text.lower() == 'тяжёлое оружие':
        heavy(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, extra_features_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Категория не найдена, пожалуйста, выберите одну из данных категорий:'
            markup = buttons.markup_guns_ru
        else:
            text = '⚠️ No category found, please select one of the given categories:'
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)

def pistols(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет..'
        markup = buttons.markup_pistols_ru
    else:
        text = '🔫 Select the pistol..'
        markup = buttons.markup_pistols_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, pistols_process)

def pistols_process(message):
    if message.text.lower() in strings.gun_name_list:
        for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Пистолет не найден, пожалуйста, выберите один из данных пистолетов:'
            markup = buttons.markup_pistols_ru
        else:
            text = '⚠️ No pistol found, please select one of the given pistols:'
            markup = buttons.markup_pistols_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, pistols_process)


def smgs(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет-пулемёт..'
        markup = buttons.markup_smgs_ru
    else:
        text = '🔫 Select the SMG..'
        markup = buttons.markup_smgs_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, smgs_process)

def smgs_process(message):
    if message.text.lower() in strings.gun_name_list:
        for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Пистолет-пулемёт не найден, пожалуйста, выберите один из данных пистолетов-пулемётов:'
            markup = buttons.markup_smgs_ru
        else:
            text = '⚠️ No SMG found, please select one of the given SMGs:'
            markup = buttons.markup_smgs_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, smgs_process)

def rifles(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите винтовку..'
        markup = buttons.markup_rifles_ru
    else:
        text = '🔫 Select the rifle..'
        markup = buttons.markup_rifles_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, rifles_process)

def rifles_process(message):
    if message.text.lower() in strings.gun_name_list:
        for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Винтовка не найдена, пожалуйста, выберите одну из данных винтовок:'
            markup = buttons.markup_rifles_ru
        else:
            text = '⚠️ No rilfe found, please select one of the given rifles:'
            markup = buttons.markup_rifles_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, rifles_process)

def heavy(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите тяжёлое оружие..'
        markup = buttons.markup_heavy_ru
    else:
        text = '🔫 Select the heavy gun..'
        markup = buttons.markup_heavy_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, heavy_process)

def heavy_process(message):
    if message.text.lower() in strings.gun_name_list:
        for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Тяжёлое оружие не найдено, пожалуйста, выберите одно из данных тяжёлых оружий:'
            markup = buttons.markup_heavy_ru
        else:
            text = '⚠️ No heavy gun found, please select one of the given heavy guns:'
            markup = buttons.markup_heavy_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, heavy_process)


### Data-centers ###


def dc_europe(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион..'
        markup = buttons.markup_DC_EU_ru            
    else:
        text = '📍 Specify the region..'
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process)

def dc_europe_process(message):
    if message.text.lower() in strings.north_european_tags:
        send_dc_eu_north(message)
    elif message.text.lower() in strings.east_european_tags:
        send_dc_eu_east(message)
    elif message.text.lower() in strings.west_european_tags:
        send_dc_eu_west(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        dc_back(message)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Регион не найден, пожалуйста, выберите один из данных регионов:'
            markup = buttons.markup_DC_EU_ru
        else:
            text = '⚠️ No region found, please select one of the given regions:'
            markup = buttons.markup_DC_EU_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, dc_europe_process)

def dc_usa(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион..'
        markup = buttons.markup_DC_USA_ru
    else:
        text = '📍 Specify the region..'
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_usa_process)

def dc_back(message):
    if message.from_user.language_code in CIS_lang_codes:
        markup = buttons.markup_DC_ru
    else:
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

def dc_usa_process(message):
    if message.text.lower() in strings.northern_usa_tags:
        send_dc_usa_north(message)
    elif message.text.lower() in strings.southern_usa_tags:
        send_dc_usa_south(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        dc_back(message)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Регион не найден, пожалуйста, выберите один из данных регионов:'
            markup = buttons.markup_DC_USA_ru
        else:
            text = '⚠️ No region found, please select one of the given regions:'
            markup = buttons.markup_DC_USA_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, dc_usa_process)

def dc_asia(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите страну..'
        markup = buttons.markup_DC_Asia_ru
    else:
        text = '📍 Specify the country..'
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def dc_asia_process(message):
    if message.text.lower() in strings.indian_tags:
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
        dc_back(message)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Страна не найдена, пожалуйста, выберите одну из данных стран:'
            markup = buttons.markup_DC_Asia_ru
        else:
            text = '⚠️ No country found, please select one of the given countries:'
            markup = buttons.markup_DC_Asia_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, dc_asia_process)

# Africa

def send_dc_africa(message):
    africa_text_en, africa_text_ru = get_data.dc_africa()
    if message.from_user.language_code in CIS_lang_codes:
        text = africa_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = africa_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

# Australia 

def send_dc_australia(message):
    australia_text_en, australia_text_ru = get_data.dc_australia()
    if message.from_user.language_code in CIS_lang_codes:
        text = australia_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = australia_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

# Europe

def send_dc_eu_north(message):
    eu_north_text_en, eu_north_text_ru = get_data.dc_eu_north()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_north_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_north_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process)

def send_dc_eu_west(message):
    eu_west_text_en, eu_west_text_ru = get_data.dc_eu_west()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_west_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_west_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process)

def send_dc_eu_east(message):
    eu_east_text_en, eu_east_text_ru = get_data.dc_eu_east()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_east_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_east_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process) 

# USA

def send_dc_usa_north(message):
    usa_north_text_en, usa_north_text_ru = get_data.dc_usa_north()
    if message.from_user.language_code in CIS_lang_codes:
        text = usa_north_text_ru
        markup = buttons.markup_DC_USA_ru
    else:
        text = usa_north_text_en
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_usa_process)

def send_dc_usa_south(message):
    usa_south_text_en, usa_south_text_ru = get_data.dc_usa_south()
    if message.from_user.language_code in CIS_lang_codes:
        text = usa_south_text_ru
        markup = buttons.markup_DC_USA_ru
    else:
        text = usa_south_text_en
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_usa_process)

# South America

def send_dc_south_america(message):
    south_america_text_en, south_america_text_ru = get_data.dc_south_america()
    if message.from_user.language_code in CIS_lang_codes:
        text = south_america_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = south_america_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

# Asia

def send_dc_india(message):
    india_text_en, india_text_ru = get_data.dc_india()
    if message.from_user.language_code in CIS_lang_codes:
        text = india_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = india_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def send_dc_japan(message):
    japan_text_en, japan_text_ru = get_data.dc_japan()
    if message.from_user.language_code in CIS_lang_codes:
        text = japan_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = japan_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def send_dc_china(message):
    china_text_en, china_text_ru = get_data.dc_china()
    if message.from_user.language_code in CIS_lang_codes:
        text = china_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = china_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def send_dc_emirates(message):
    emirates_text_en, emirates_text_ru = get_data.dc_emirates()
    if message.from_user.language_code in CIS_lang_codes:
        text = emirates_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = emirates_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def send_dc_singapore(message):
    singapore_text_en, singapore_text_ru = get_data.dc_singapore()
    if message.from_user.language_code in CIS_lang_codes:
        text = singapore_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = singapore_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def send_dc_hong_kong(message):
    hong_kong_text_en, hong_kong_text_ru = get_data.dc_hong_kong()
    if message.from_user.language_code in CIS_lang_codes:
        text = hong_kong_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = hong_kong_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)



### Inline-mode ###


# Default
@bot.inline_handler(lambda query: len(query.query) == 0)
def default_inline(inline_query):
    '''Inline mode'''
    log_inline(inline_query)
    try:
        status_text_en, status_text_ru = get_data.server_status()
        mm_stats_text_en, mm_stats_text_ru = get_data.mm_stats()
        devcount_text_en, devcount_text_ru = get_data.devcount()
        timer_text_en, timer_text_ru = get_data.timer()
        gameversion_text_en, gameversion_text_ru = get_data.gameversion()
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
        status_text_en, status_text_ru = get_data.server_status()
        mm_stats_text_en, mm_stats_text_ru = get_data.mm_stats()
        devcount_text_en, devcount_text_ru = get_data.devcount()
        timer_text_en, timer_text_ru = get_data.timer()
        gameversion_text_en, gameversion_text_ru = get_data.gameversion()
        eu_north_text_en, eu_north_text_ru = get_data.dc_eu_north()
        eu_east_text_en, eu_east_text_ru = get_data.dc_eu_east()
        eu_west_text_en, eu_west_text_ru = get_data.dc_eu_west()
        usa_north_text_en, usa_north_text_ru = get_data.dc_usa_north()
        usa_south_text_en, usa_south_text_ru = get_data.dc_usa_south()
        china_text_en, china_text_ru = get_data.dc_china()
        emirates_text_en, emirates_text_ru = get_data.dc_emirates()
        hong_kong_text_en, hong_kong_text_ru = get_data.dc_hong_kong()
        india_text_en, india_text_ru = get_data.dc_india()
        japan_text_en, japan_text_ru = get_data.dc_japan()
        singapore_text_en, singapore_text_ru = get_data.dc_singapore()
        australia_text_en, australia_text_ru = get_data.dc_australia()
        africa_text_en, africa_text_ru = get_data.dc_africa()            
        south_america_text_en, south_america_text_ru = get_data.dc_south_america()
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
                data = [status_text_en, mm_stats_text_en, devcount_text_en, timer_text_en, gameversion_text_en, china_text_en, emirates_text_en,
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
        

@bot.message_handler(func=lambda message: message.chat.type == 'private' and (message.text.lower() == 'dataсenters status' or message.text.lower() == 'состояние дата-центров'), content_types=['text'])
def dc(message):
            if message.from_user.language_code in CIS_lang_codes:
                text = '📶 Выберите регион, который Вам интересен, чтобы получить информацию о дата-центрах:'
                markup = buttons.markup_DC_ru
            else:
                text = '📶 Select the region, that you are interested in, to get information about the datacenters:'
                markup = buttons.markup_DC_en
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
            bot.register_next_step_handler(msg, dc_process)

def dc_process(message):
    if message.text.lower() in strings.asian_tags:
        dc_asia(message)
    elif message.text.lower() in strings.african_tags:
        send_dc_africa(message)
    elif message.text.lower() in strings.australian_tags:
        send_dc_australia(message)
    elif message.text.lower() in strings.european_tags:
        dc_europe(message)
    elif message.text.lower() in strings.american_tags:
        dc_usa(message)
    elif message.text.lower() in strings.south_american_tags:
        send_dc_south_america(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, '👌', reply_markup=markup)
        bot.register_next_step_handler(msg, server_stats_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Регион не найден, пожалуйста, выберите один из данных регионов:'
            markup = buttons.markup_DC_ru
        else:
            text = '⚠️ No region found, please select one of the given regions:'
            markup = buttons.markup_DC_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, dc_process)

@bot.message_handler(func=lambda message: message.chat.type == 'private' and (message.text.lower() == 'server statistics' or message.text.lower() == 'статистика серверов'), content_types=['text'])
def server_stats(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in CIS_lang_codes:
            text = '📊 Воспользуйтесь одной из приведённых команд:'
            markup = buttons.markup_ss_ru
        else:
            text = '📊 Use one of the following commands:'
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, server_stats_process)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def server_stats_process(message):
    if message.text.lower() == 'server status' or message.text.lower() == 'состояние серверов':
        send_server_status(message)
    elif message.text.lower() == 'matchmaking statistics' or message.text.lower() == 'статистика матчмейкинга':
        send_mm_stats(message)
    elif message.text.lower() == 'dataсenters status' or message.text.lower() == 'состояние дата-центров':
        dc(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        bot.send_message(message.chat.id, '👌', reply_markup=markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Ничего не найден, пожалуйста, воспользуйтесь одной из приведённых команд:'
            markup = buttons.markup_ss_ru
        else:
            text = '⚠️ Nothing found, please use one of the following commands:'
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, server_stats_process)

@bot.message_handler(func=lambda message: message.chat.type == 'private' and (message.text.lower() == 'profile information' or message.text.lower() == 'информация о профиле'), content_types=['text'])
def profile_info(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '💤 Скоро..'
        markup = buttons.markup_ru
    else:
        text = '💤 Coming soon..'
        markup = buttons.markup_en
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.type == 'private' and (message.text.lower() == 'extra features' or message.text.lower() == 'дополнительные функции'), content_types=['text'])
def extra_features(message):
    if message.from_user.language_code in CIS_lang_codes:
        text = '🗃 Воспользуйтесь одной из приведённых команд:'
        markup = buttons.markup_extra_ru
    else:
        text = '🗃 Use one of the following commands:'
        markup = buttons.markup_extra_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, extra_features_process)

def extra_features_process(message):
    if message.text.lower() == 'developers in-game' or message.text.lower() == 'разработчиков в игре':
        send_devcount(message)
    elif message.text.lower() == 'game version' or message.text.lower() == 'версия игры':
        send_gameversion(message)
    elif message.text.lower() == 'cap reset' or message.text.lower() == 'сброс ограничений':
        send_timer(message)
    elif message.text.lower() == 'gun database' or message.text.lower() == 'база данных оружий':
        guns(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        bot.send_message(message.chat.id, '👌', reply_markup=markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            text = '⚠️ Ничего не найден, пожалуйста, воспользуйтесь одной из приведённых команд:'
            markup = buttons.markup_extra_ru
        else:
            text = '⚠️ Nothing found, please use one of the following commands:'
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, extra_features_process)

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

            elif message.text.lower() in strings.gun_name_list:
                for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
                    if message.text.lower() == gName:
                        send_gun_info(message, gId)

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