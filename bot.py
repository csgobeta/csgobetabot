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
from plugins import tag_list
from plugins.addons import translate
from apps import file_manager

bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode='html')
telebot.logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
CIS_lang_codes = ['ru', 'uk', 'be', 'uz', 'kk']


### Server statistics ###


def server_stats(message):
    bot.send_chat_action(message.chat.id, 'typing')
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
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'service status' or 'состояние служб':
        send_server_status(message)
    elif message.text.lower() == 'matchmaking status' or 'состояние матчмейкинга':
        send_mm_stats(message)
    elif message.text.lower() == 'dataсenters status' or 'состояние дата-центров':
        dc(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        back(message, markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        unknown_request(message, markup, server_stats_process)

def send_server_status(message):
    '''Send the status of CS:GO servers'''
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        mm_stats_text_en, mm_stats_text_ru = get_data.mm_stats()
        if message.from_user.language_code in CIS_lang_codes:
            text = mm_stats_text_ru
            markup = buttons.markup_ss_ru
        else:
            text = mm_stats_text_en
            markup = buttons.markup_ss_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, server_stats_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


### Extra features ###


def extra_features(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🗃 Воспользуйтесь одной из приведённых команд:'
        markup = buttons.markup_extra_ru
    else:
        text = '🗃 Use one of the following commands:'
        markup = buttons.markup_extra_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, extra_features_process)

def extra_features_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'developers in-game' or 'разработчиков в игре':
        send_devcount(message)
    elif message.text.lower() == 'game version' or 'версия игры':
        send_gameversion(message)
    elif message.text.lower() == 'cap reset' or 'сброс ограничений':
        send_timer(message)
    elif message.text.lower() == 'gun database' or 'база данных оружий':
        guns(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        back(message, markup)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        unknown_request(message, markup, extra_features_process)

def send_devcount(message):
    '''Send the count of online devs'''
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        devcount_text_en, devcount_text_ru = get_data.devcount()
        if message.from_user.language_code in CIS_lang_codes:
            text = devcount_text_ru
            markup = buttons.markup_extra_ru
        else:    
            text = devcount_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_timer(message):
    '''Send drop cap reset time'''
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        gameversion_text_en, gameversion_text_ru = get_data.gameversion()
        if message.from_user.language_code in CIS_lang_codes:
            text = gameversion_text_ru
            markup = buttons.markup_extra_ru
        else:
            text = gameversion_text_en
            markup = buttons.markup_extra_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup) 
        bot.register_next_step_handler(msg, extra_features_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def guns(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '#️⃣ Выберите категорию, которая Вас интересует:'
        markup = buttons.markup_guns_ru
    else:
        text = '#️⃣ Select the category, that you are interested in:'
        markup = buttons.markup_guns_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup) 
    bot.register_next_step_handler(msg, guns_process)

def guns_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'pistols' or 'пистолеты':
        pistols(message)
    elif message.text.lower() == 'smgs' or 'пистолеты-пулемёты':
        smgs(message)
    elif message.text.lower() == 'rifles' or 'винтовки':
        rifles(message)
    elif message.text.lower() == 'heavy' or 'тяжёлое оружие':
        heavy(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_extra_ru
        else:
            markup = buttons.markup_extra_en
        back(message, markup, extra_features_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        unknown_request(message, markup, guns_process)

def pistols(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет..'
        markup = buttons.markup_pistols_ru
    else:
        text = '🔫 Select the pistol..'
        markup = buttons.markup_pistols_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, pistols_process)

def pistols_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() in tag_list.gun_name_list:
        for gName, gId in zip(tag_list.gun_name_list, tag_list.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_pistols_ru
        else:
            markup = buttons.markup_pistols_en
        unknown_request(message, markup, pistols_process)

def smgs(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите пистолет-пулемёт..'
        markup = buttons.markup_smgs_ru
    else:
        text = '🔫 Select the SMG..'
        markup = buttons.markup_smgs_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, smgs_process)

def smgs_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() in tag_list.gun_name_list:
        for gName, gId in zip(tag_list.gun_name_list, tag_list.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_smgs_ru
        else:
            markup = buttons.markup_smgs_en
        unknown_request(message, markup, smgs_process)

def rifles(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите винтовку..'
        markup = buttons.markup_rifles_ru
    else:
        text = '🔫 Select the rifle..'
        markup = buttons.markup_rifles_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, rifles_process)

def rifles_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() in tag_list.gun_name_list:
        for gName, gId in zip(tag_list.gun_name_list, tag_list.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_rifles_ru
        else:
            markup = buttons.markup_rifles_en
        unknown_request(message, markup, rifles_process)

def heavy(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '🔫 Выберите тяжёлое оружие..'
        markup = buttons.markup_heavy_ru
    else:
        text = '🔫 Select the heavy gun..'
        markup = buttons.markup_heavy_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, heavy_process)

def heavy_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() in tag_list.gun_name_list:
        for gName, gId in zip(tag_list.gun_name_list, tag_list.gun_id_list):
            if message.text.lower() == gName:
                send_gun_info(message, gId)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_guns_ru
        else:
            markup = buttons.markup_guns_en
        back(message, markup, guns_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_heavy_ru
        else:
            markup = buttons.markup_heavy_en
        unknown_request(message, markup, heavy_process)

def send_gun_info(message, gun_id):
    '''Send archived data about guns'''
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    try:
        gun_data_text_en, gun_data_text_ru = get_data.gun_info(gun_id)
        if message.from_user.language_code in CIS_lang_codes:
            text = gun_data_text_ru
            markup = buttons.markup_guns_ru
        else:
            text = gun_data_text_en
            markup = buttons.markup_guns_en
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, guns_process)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)


### Profile information ###


def profile_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '💤 В разработке..'
        markup = buttons.markup_ru
    else:
        text = '💤 Coming soon..'
        markup = buttons.markup_en
    bot.send_message(message.chat.id, text, reply_markup=markup)


### Datacenters ###


def dc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '📶 Выберите регион, который Вам интересен, чтобы получить информацию о дата-центрах:'
        markup = buttons.markup_DC_ru
    else:
        text = '📶 Select the region, that you are interested in, to get information about the datacenters:'
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

def dc_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'asia' or 'азия':
        dc_asia(message)
    elif message.text.lower() == 'south africa' or 'южная африка':
        send_dc_africa(message)
    elif message.text.lower() == 'australia' or 'австралия':
        send_dc_australia(message)
    elif message.text.lower() == 'europe' or 'европа':
        dc_europe(message)
    elif message.text.lower() == 'usa' or 'сша':
        dc_usa(message)
    elif message.text.lower() == 'south america' or 'южная америка':
        send_dc_south_america(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ss_ru
        else:
            markup = buttons.markup_ss_en
        back(message, markup, server_stats_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        unknown_request(message, markup, dc_process)

def dc_europe(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион..'
        markup = buttons.markup_DC_EU_ru            
    else:
        text = '📍 Specify the region..'
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process)

def dc_europe_process(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'north' or 'север':
        send_dc_eu_north(message)
    elif message.text.lower() == 'east' or 'восток':
        send_dc_eu_east(message)
    elif message.text.lower() == 'west' or 'запад':
        send_dc_eu_west(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_EU_ru
        else:
            markup = buttons.markup_DC_EU_en
        unknown_request(message, markup, dc_europe_process)

def dc_usa(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите регион..'
        markup = buttons.markup_DC_USA_ru
    else:
        text = '📍 Specify the region..'
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_usa_process)

def dc_usa_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'north' or 'север':
        send_dc_usa_north(message)
    elif message.text.lower() == 'south' or 'юг':
        send_dc_usa_south(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_USA_ru
        else:
            markup = buttons.markup_DC_USA_en
        unknown_request(message, markup, dc_usa_process)

def dc_asia(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = '📍 Укажите страну..'
        markup = buttons.markup_DC_Asia_ru
    else:
        text = '📍 Specify the country..'
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)

def dc_asia_process(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.lower() == 'india' or 'индия':
        send_dc_india(message)
    elif message.text.lower() == 'japan' or 'япония':
        send_dc_japan(message)
    elif message.text.lower() == 'china' or 'китай':
        send_dc_china(message)
    elif message.text.lower() == 'emirates' or 'эмираты':
        send_dc_emirates(message)
    elif message.text.lower() == 'singapore' or 'сингапур':
        send_dc_singapore(message)
    elif message.text.lower() == 'hong kong' or 'гонконг':
        send_dc_hong_kong(message)
    elif message.text == '⏪ Back' or message.text == '⏪ Назад':
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_ru
        else:
            markup = buttons.markup_DC_en
        back(message, markup, dc_process)
    else:
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_DC_Asia_ru
        else:
            markup = buttons.markup_DC_Asia_en
        unknown_request(message, markup, dc_asia_process)

def send_dc_africa(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    africa_text_en, africa_text_ru = get_data.dc_africa()
    if message.from_user.language_code in CIS_lang_codes:
        text = africa_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = africa_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

def send_dc_australia(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    australia_text_en, australia_text_ru = get_data.dc_australia()
    if message.from_user.language_code in CIS_lang_codes:
        text = australia_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = australia_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

def send_dc_eu_north(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    eu_east_text_en, eu_east_text_ru = get_data.dc_eu_east()
    if message.from_user.language_code in CIS_lang_codes:
        text = eu_east_text_ru
        markup = buttons.markup_DC_EU_ru
    else:
        text = eu_east_text_en
        markup = buttons.markup_DC_EU_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_europe_process) 

def send_dc_usa_north(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    usa_south_text_en, usa_south_text_ru = get_data.dc_usa_south()
    if message.from_user.language_code in CIS_lang_codes:
        text = usa_south_text_ru
        markup = buttons.markup_DC_USA_ru
    else:
        text = usa_south_text_en
        markup = buttons.markup_DC_USA_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_usa_process)

def send_dc_south_america(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    south_america_text_en, south_america_text_ru = get_data.dc_south_america()
    if message.from_user.language_code in CIS_lang_codes:
        text = south_america_text_ru
        markup = buttons.markup_DC_ru
    else:
        text = south_america_text_en
        markup = buttons.markup_DC_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_process)

def send_dc_india(message):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
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
    log(message)
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
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    hong_kong_text_en, hong_kong_text_ru = get_data.dc_hong_kong()
    if message.from_user.language_code in CIS_lang_codes:
        text = hong_kong_text_ru
        markup = buttons.markup_DC_Asia_ru
    else:
        text = hong_kong_text_en
        markup = buttons.markup_DC_Asia_en
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, dc_asia_process)


### Addons ###


def send_about_problem_valve_api(message):
    '''In case the bot can't get Valve's API'''
    log(message)
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongAPI_ru
        markup = buttons.markup_ru       
    else:
        text = strings.wrongAPI_en
        markup = buttons.markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_maintenance(message):
    '''In case weekly server update (on Tuesdays)'''
    log(message)
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.maintenance_ru
        markup = buttons.markup_ru       
    else:
        text = strings.maintenance_en
        markup = buttons.markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_problem_valve_api_inline(inline_query):
    log(message)
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
    log(message)
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
    log(message)
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.wrongBOT_ru
        markup = buttons.markup_ru
    else:
        text = strings.wrongBOT_en
        markup = buttons.markup_en
    bot.send_message(message.chat.id, text, reply_markup=markup)

def unknown_request(message, *args):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.language_code in CIS_lang_codes:
        text = strings.unknownRequest_ru
        markup = buttons.markup_ru
    else: 
        text = strings.unknownRequest_en
        markup = buttons.markup_en
    if len(args) < 1:
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, text, reply_markup=args[0])
        bot.register_next_step_handler(msg, args[1])

def back(message, *args):
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if len(args) < 2:
        bot.send_message(message.chat.id, '👌', reply_markup=args[0])
    else:
        msg = bot.send_message(message.chat.id, '👌', reply_markup=args[0])
        bot.register_next_step_handler(msg, args[1])


### Commands ###


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
    bot.send_chat_action(message.chat.id, 'typing')
    if message.chat.type == 'private':
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdFeedback_ru 
        else:
            text = strings.cmdFeedback_en
        msg = bot.send_message(message.chat.id, text, reply_markup=buttons.markup_del)
        bot.register_next_step_handler(msg, get_feedback)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

def get_feedback(message):
    '''Get feedback from users'''
    log(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text == '/cancel':
        log(message)
        if message.from_user.language_code in CIS_lang_codes:
            markup = buttons.markup_ru
        else:
            markup = buttons.markup_en
        bot.send_message(message.chat.id, '👍', reply_markup=markup)

    else:
        bot.send_message(config.OWNER, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', disable_notification=True)
        bot.forward_message(config.OWNER, message.chat.id, message.message_id)
        
        if not config.TEST_MODE:
            bot.send_message(config.AQ, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', disable_notification=True)
            bot.forward_message(config.AQ, message.chat.id, message.message_id)

        if message.from_user.language_code in CIS_lang_codes:
            text = 'Отлично! Ваше сообщение отправлено.'
            markup = buttons.markup_ru
        else:
            text = 'Awesome! Your message has been sent.'
            markup = buttons.markup_en

        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    '''/help message'''
    bot.send_chat_action(message.chat.id, 'typing')
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in CIS_lang_codes:
            text = strings.cmdHelp_ru
            markup = buttons.markup_ru
        else:
            text = strings.cmdHelp_en
            markup = buttons.markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)
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
        

### Inline-mode ###


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

@bot.inline_handler(lambda query: len(query.query) >= 0)
def inline_dc(inline_query):
    log_inline(inline_query)
    try:
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
            thumbs = ['https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg', 'https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', 'https://telegra.ph/file/0b209e65c421910419f34.jpg',
                        'https://telegra.ph/file/b2213992b750940113b69.jpg', 'https://telegra.ph/file/11b6601a3e60940d59c88.jpg', 'https://telegra.ph/file/1c2121ceec5d1482173d5.jpg',
                        'https://telegra.ph/file/4d269cb98aadaae391024.jpg', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg', 'https://telegra.ph/file/4d269cb98aadaae391024.jpg',
                        'https://telegra.ph/file/06119c30872031d1047d0.jpg', 'https://telegra.ph/file/06119c30872031d1047d0.jpg', 'https://telegra.ph/file/5dc6beef1556ea852284c.jpg',
                        'https://telegra.ph/file/12628c8193b48302722e8.jpg',
                        'https://telegra.ph/file/60f8226ea5d72815bef57.jpg']
            tagList = [tag_list.chinese, tag_list.emirati, tag_list.hong_kongese, tag_list.indian, tag_list.japanese,
                    tag_list.singaporean, tag_list.north_european, tag_list.east_european, tag_list.west_european,
                    tag_list.northern_usa, tag_list.southern_usa, tag_list.australian, tag_list.african, tag_list.south_american]
            if inline_query.from_user.language_code in CIS_lang_codes:
                data = [china_text_ru, emirates_text_ru, hong_kong_text_ru, india_text_ru, japan_text_ru, singapore_text_ru, eu_north_text_ru,
                eu_east_text_ru, eu_west_text_ru, usa_north_text_ru, usa_south_text_ru, australia_text_ru, africa_text_ru, south_america_text_ru]
                titles = ['Китайские ДЦ', 'Эмиратский ДЦ', 'Гонконгский ДЦ', 'Индийские ДЦ', 'Японский ДЦ', 'Сингапурский ДЦ', 'Североевропейский ДЦ',
                            'Восточноевропейские ДЦ', 'Западноевропейские ДЦ', 'ДЦ северной части США', 'ДЦ южной части США', 'Австралийский ДЦ',
                            'Африканский ДЦ', 'Южноамериканские ДЦ']
                descriptions = ['Проверить состояние']
            else:
                data = [china_text_en, emirates_text_en, hong_kong_text_en, india_text_en, japan_text_en, singapore_text_en, eu_north_text_en,
                        eu_east_text_en, eu_west_text_en, usa_north_text_en, usa_south_text_en, australia_text_en, africa_text_en, south_america_text_en]
                titles = ['Chinese DC', 'Emirati DC', 'Hong Kongese DC', 'Indian DC', 'Japanese DC', 'Singaporean DC', 'North European DC',
                            'East European DC', 'West European DC', 'Northern USA DC', 'Southern USA DC', 'Australian DC', 'African DC', 'South American DC']
                descriptions = ['Check the status']
            results = []
            for data, tt, desc, thumb, tags in zip(data, titles, descriptions*100, thumbs, tagList):
                for tag in tags:
                    if inline_query.query == tag:
                        results.append(types.InlineQueryResultArticle(random.randint(0,9999), tt, input_message_content=types.InputTextMessageContent(data, parse_mode='html'), thumb_url=thumb, description=desc))
            bot.answer_inline_query(inline_query.id, results, cache_time=5)
        elif wsCache == 'maintenance':
            send_about_maintenance_inline(inline_query)
        else:
            send_about_problem_valve_api_inline(inline_query)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')


### 


@bot.message_handler(content_types=['text'])
def answer(message):
    log(message)
    try:
        if message.chat.type == 'private':
            bot.send_chat_action(message.chat.id, 'typing')

            data = pd.read_csv(config.USER_DB_FILE_PATH)
            if not data['UserID'].isin([message.from_user.id]).any():
                new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id, message.from_user.language_code]], columns=['Name', 'UserID', 'Language'])
                pd.concat([data, new_data]).to_csv(config.USER_DB_FILE_PATH, index=False)

            if message.text.lower() == 'server statistics' or 'статистика серверов':
                server_stats(message)

            elif message.text.lower() == 'extra features' or 'дополнительные функции':
                extra_features(message)

            elif message.text.lower() == 'profile information' or 'информация о профиле':
                profile_info(message)

            else:
                unknown_request(message)

        else:
            if message.from_user.id == 777000:
                if message.forward_from_chat.id == config.CSGOBETACHANNEL and 'Обновлены файлы локализации' in message.text:
                    bot.send_sticker(config.CSGOBETACHAT, 'CAACAgIAAxkBAAID-l_9tlLJhZQSgqsMUAvLv0r8qhxSAAIKAwAC-p_xGJ-m4XRqvoOzHgQ', reply_to_message_id=message.message_id)

    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')


### Logging ###


def log(message):   
    '''The bot sends log to log channel'''
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, message, parse_mode='')

def log_inline(inline_query):
    '''The bot sends inline query to log channel'''
    if not config.TEST_MODE:
        bot.send_message(config.LOGCHANNEL, inline_query, parse_mode='')


### Polling ###


bot.polling(True)