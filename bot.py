# -*- coding: utf-8 -*-

import time
from datetime import date, datetime, timedelta
import pytz
from babel.dates import format_datetime

import pandas as pd
import logging
import telebot
from telebot import types

import config
import strings

from apps.timer import Reset
from apps.valve_api import ValveServersDataCentersAPI
from apps import file_manager

bot = telebot.TeleBot(config.BOT_TOKEN)
telebot.logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

tz = pytz.timezone('UTC')
tz_valve = pytz.timezone('America/Los_Angeles')
api_dc = ValveServersDataCentersAPI()
timer_drop = Reset()


### Keyboard setup ###


# English
markup_en = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
server_status = types.KeyboardButton('Server status')
devcount = types.KeyboardButton('Online devs')
timer = types.KeyboardButton('Cap reset')
dc = types.KeyboardButton('Data centers')
gv = types.KeyboardButton('Game version')
guns = types.KeyboardButton('Gun database')
markup_en.add(server_status, dc, devcount, timer, gv, guns)

# DC
markup_DC = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
europe = types.KeyboardButton('Europe')
asia = types.KeyboardButton('Asia')
south_africa = types.KeyboardButton('South Africa')
south_america = types.KeyboardButton('South America')
australia = types.KeyboardButton('Australia')
usa =  types.KeyboardButton('USA')
back_button = types.KeyboardButton('⏪ Back')
back_button_alt = types.KeyboardButton('⏪ Bаck')
markup_DC.add(asia, australia, europe, south_africa, south_america, usa, back_button)

# DC Asia
markup_DC_Asia = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
india = types.KeyboardButton('India')
emirates = types.KeyboardButton('Emirates')
china = types.KeyboardButton('China')
singapore = types.KeyboardButton('Singapore')
hong_kong = types.KeyboardButton('Hong Kong')
japan = types.KeyboardButton('Japan')
markup_DC_Asia.add(china, emirates, hong_kong, india, japan, singapore, back_button_alt)

# DC Europe
markup_DC_EU = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West = types.KeyboardButton('West')
eu_East = types.KeyboardButton('East')
eu_North = types.KeyboardButton('North')
markup_DC_EU.add(eu_East, eu_North, eu_West, back_button_alt)

# DC USA
markup_DC_USA = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest = types.KeyboardButton('Nоrth')
usa_Southwest = types.KeyboardButton('South')
markup_DC_USA.add(usa_Northwest, usa_Southwest, back_button_alt)

# Guns
markup_guns = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols = types.KeyboardButton('Pistols')
smgs = types.KeyboardButton('SMGs')
rifles = types.KeyboardButton('Rifles')
heavy = types.KeyboardButton('Heavy')
back_button = types.KeyboardButton('⏪ Back')
back_button_alt_2 = types.KeyboardButton('⏪ Bасk')
markup_guns.add(pistols, smgs, rifles, heavy, back_button)

# Guns Russian
markup_guns_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols = types.KeyboardButton('Пистолеты')
smgs = types.KeyboardButton('Пистолеты-пулемёты')
rifles = types.KeyboardButton('Винтовки')
heavy = types.KeyboardButton('Тяжёлое оружие')
Back_button_ru = types.KeyboardButton('⏪ Назад')
back_button_alt_2_ru = types.KeyboardButton('⏪ Haзад')
markup_guns_ru.add(pistols, smgs, rifles, heavy, Back_button_ru)

# Pistols
markup_pistols = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
usps = types.KeyboardButton('USP-S')
p2000 = types.KeyboardButton('P2000')
glock = types.KeyboardButton('Glock-18')
dualies = types.KeyboardButton('Dual Berettas')
p250 = types.KeyboardButton('P250')
cz75 = types.KeyboardButton('CZ75-Auto')
five_seven = types.KeyboardButton('Five-SeveN')
tec = types.KeyboardButton('Tec-9')
deagle = types.KeyboardButton('Desert Eagle')
r8 = types.KeyboardButton('R8 Revolver')
markup_pistols.add(usps, p2000, glock, dualies, p250, cz75, five_seven, tec, deagle, r8)
markup_pistols.add(back_button_alt_2)

# Pistols Russian
markup_pistols_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
usps = types.KeyboardButton('USP-S')
p2000 = types.KeyboardButton('P2000')
glock = types.KeyboardButton('Glock-18')
dualies = types.KeyboardButton('Dual Berettas')
p250 = types.KeyboardButton('P250')
cz75 = types.KeyboardButton('CZ75-Auto')
five_seven = types.KeyboardButton('Five-SeveN')
tec = types.KeyboardButton('Tec-9')
deagle = types.KeyboardButton('Desert Eagle')
r8 = types.KeyboardButton('R8 Revolver')
markup_pistols_ru.add(usps, p2000, glock, dualies, p250, cz75, five_seven, tec, deagle, r8)
markup_pistols_ru.add(back_button_alt_2_ru)

# SMGs
markup_smgs = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
mp9 = types.KeyboardButton('MP9')
mac10 = types.KeyboardButton('MAC-10')
mp7 = types.KeyboardButton('MP7')
mp5 = types.KeyboardButton('MP5-SD')
ump = types.KeyboardButton('UMP-45')
p90 = types.KeyboardButton('P90')
pp = types.KeyboardButton('PP-Bizon')
markup_smgs.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs.add(back_button_alt_2)

# SMGs Russian
markup_smgs_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
mp9 = types.KeyboardButton('MP9')
mac10 = types.KeyboardButton('MAC-10')
mp7 = types.KeyboardButton('MP7')
mp5 = types.KeyboardButton('MP5-SD')
ump = types.KeyboardButton('UMP-45')
p90 = types.KeyboardButton('P90')
pp = types.KeyboardButton('PP-Bizon')
markup_smgs_ru.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs_ru.add(back_button_alt_2_ru)

# Rifles
markup_rifles = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
famas = types.KeyboardButton('Famas')
galil = types.KeyboardButton('Galil AR')
m4a4 = types.KeyboardButton('M4A4')
m4a1 = types.KeyboardButton('M4A1-S')
ak = types.KeyboardButton('AK-47')
aug = types.KeyboardButton('AUG')
sg = types.KeyboardButton('SG 553')
ssg = types.KeyboardButton('SSG 08')
awp = types.KeyboardButton('AWP')
scar = types.KeyboardButton('SCAR-20')
g3sg1 = types.KeyboardButton('G3SG1')
markup_rifles.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles.add(back_button_alt_2)

# Rifles Russian
markup_rifles_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
famas = types.KeyboardButton('Famas')
galil = types.KeyboardButton('Galil AR')
m4a4 = types.KeyboardButton('M4A4')
m4a1 = types.KeyboardButton('M4A1-S')
ak = types.KeyboardButton('AK-47')
aug = types.KeyboardButton('AUG')
sg = types.KeyboardButton('SG 553')
ssg = types.KeyboardButton('SSG 08')
awp = types.KeyboardButton('AWP')
scar = types.KeyboardButton('SCAR-20')
g3sg1 = types.KeyboardButton('G3SG1')
markup_rifles_ru.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles_ru.add(back_button_alt_2_ru)

# Heavy
markup_heavy = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
nova = types.KeyboardButton('Nova')
xm1014 = types.KeyboardButton('XM1014')
mag7 = types.KeyboardButton('MAG-7')
sawedoff = types.KeyboardButton('Sawed-Off')
m249 = types.KeyboardButton('M249')
negev = types.KeyboardButton('Negev')
markup_heavy.add(nova, xm1014, mag7, sawedoff, m249, negev)
markup_heavy.add(back_button_alt_2)

# Heavy Russian
markup_heavy_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
nova = types.KeyboardButton('Nova')
xm1014 = types.KeyboardButton('XM1014')
mag7 = types.KeyboardButton('MAG-7')
sawedoff = types.KeyboardButton('Sawed-Off')
m249 = types.KeyboardButton('M249')
negev = types.KeyboardButton('Negev')
markup_heavy_ru.add(nova, xm1014, mag7, sawedoff, m249, negev)
markup_heavy_ru.add(back_button_alt_2_ru)

# Russian
markup_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
server_status_ru = types.KeyboardButton('Статус серверов')
devcount_ru = types.KeyboardButton('Разработчиков в игре')
timer_ru = types.KeyboardButton('Сброс ограничений')
dc_ru = types.KeyboardButton('Дата-центры')
gv_ru = types.KeyboardButton('Версия игры')
guns_ru = types.KeyboardButton('База данных оружий')
markup_ru.add(server_status_ru, dc_ru, devcount_ru, timer_ru, gv_ru, guns_ru)

# DC RU
markup_DC_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
Europe_ru = types.KeyboardButton('Европа')
Asia_ru = types.KeyboardButton('Азия')
Africa_ru = types.KeyboardButton('Южная Африка')
South_America_ru = types.KeyboardButton('Южная Америка')
Australia_ru = types.KeyboardButton('Австралия') 
USA_ru =  types.KeyboardButton('США')
Back_button_ru = types.KeyboardButton('⏪ Назад')
Back_button_ru_alt = types.KeyboardButton('⏪ Нaзад')
markup_DC_ru.add(Australia_ru, Asia_ru, Europe_ru, USA_ru, South_America_ru, Africa_ru, Back_button_ru)

# DC Europe Russian
markup_DC_EU_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West_ru = types.KeyboardButton('Запад')
eu_East_ru = types.KeyboardButton('Восток')
eu_North_ru = types.KeyboardButton('Север')
markup_DC_EU_ru.add(eu_East_ru, eu_West_ru, eu_North_ru, Back_button_ru_alt)

# DC Asia Russian
markup_DC_Asia_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
india_ru = types.KeyboardButton('Индия')
emirates_ru = types.KeyboardButton('Эмираты')
china_ru = types.KeyboardButton('Китай')
singapore_ru = types.KeyboardButton('Сингапур')
hong_kong_ru = types.KeyboardButton('Гонконг')
japan_ru = types.KeyboardButton('Япония')
markup_DC_Asia_ru.add(hong_kong_ru, india_ru, china_ru, singapore_ru, emirates_ru, japan_ru, Back_button_ru_alt)

# DC USA Russian
markup_DC_USA_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest_ru = types.KeyboardButton('Сeвер')
usa_Southwest_ru = types.KeyboardButton('Юг')
markup_DC_USA_ru.add(usa_Northwest_ru, usa_Southwest_ru, Back_button_ru_alt)

# Delete keyboard
markup_del = types.ReplyKeyboardRemove(False)


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
    url = cacheFile['graph_url']
    gcCache, slCache, sCache, piCache = cacheFile['game_coordinator'], cacheFile['sessionsLogon'], cacheFile['scheduler'], cacheFile['steam_community']
    pcCache, scCache = cacheFile['online_player_count'], cacheFile['online_server_count']
    apCache, ssCache, spCache = cacheFile['active_player_count'], cacheFile['search_seconds_avg'], cacheFile['searching_players']
    p24Cache, paCache, uqCache = cacheFile['peak_24_hours'], cacheFile['peak_all_time'], cacheFile['unique_monthly']

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

    status_text_en = strings.statusNormal_en.format(url, tick, gcCache, slCache, sCache, piCache)
    status_text_ru = strings.statusNormal_ru.format(url, tick, gcRCache, slRCache, sRCache, piRCache)

    mm_text_en = strings.mmNormal_en.format(scCache, pcCache, apCache, spCache, ssCache)
    mm_text_ru = strings.mmNormal_ru.format(scCache, pcCache, apCache, spCache, ssCache)

    addInf_text_en = strings.additionalInfo_en.format(p24Cache, paCache, uqCache, tsCache)
    addInf_text_ru = strings.additionalInfo_ru.format(p24Cache, paCache, uqCache, tsRCache)

    server_status_text_en = status_text_en +  mm_text_en + addInf_text_en
    server_status_text_ru = status_text_ru +  mm_text_ru + addInf_text_ru
    return server_status_text_en, server_status_text_ru

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
    data = pd.read_csv(config.USER_DB_FILE_PATH)
    if not data['UserID'].isin([message.from_user.id]).any():
        new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id]], columns=['Name', 'UserID'])
        pd.concat([data, new_data]).to_csv(config.USER_DB_FILE_PATH, index=False)
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            server_status_text_en, server_status_text_ru = get_server_status()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = server_status_text_ru
                markup = markup_ru
            else:
                text = server_status_text_en
                markup = markup_en
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
            if message.from_user.language_code in strings.CIS_lang_code:
                    text = devcount_text_ru
                    markup = markup_ru
            else:    
                    text = devcount_text_en
                    markup = markup_en
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
        if message.from_user.language_code in strings.CIS_lang_code:
                text = timer_text_ru
                markup = markup_ru
        else:
                text = timer_text_en
                markup = markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup) 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_gameversion(message):
    '''Send the version of the game'''
    try:
        gameversion_text_en, gameversion_text_ru = get_gameversion()
        if message.from_user.language_code in strings.CIS_lang_code:
                text = gameversion_text_ru
                markup = markup_ru
        else:
                text = gameversion_text_en
                markup = markup_en
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def send_about_problem_valve_api(message):
    '''In case the bot can't get Valve's API'''
    if message.from_user.language_code in strings.CIS_lang_code:
        text = strings.wrongAPI_ru
        markup = markup_ru       
    else:
        text = strings.wrongAPI_en
        markup = markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_maintenance(message):
    '''In case weekly server update (on Tuesdays)'''
    if message.from_user.language_code in strings.CIS_lang_code:
        text = strings.maintenance_ru
        markup = markup_ru       
    else:
        text = strings.maintenance_en
        markup = markup_en   
    bot.send_message(message.chat.id, text, reply_markup=markup)

def send_about_problem_valve_api_inline(inline_query):
    try:
        if inline_query.from_user.language_code in strings.CIS_lang_code:
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
        if inline_query.from_user.language_code in strings.CIS_lang_code:
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
    if message.from_user.language_code in strings.CIS_lang_code:
        text = strings.wrongBOT_ru
        markup = markup_ru
    else:
        text = strings.wrongBOT_en
        markup = markup_en  
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
    en_list = ['normal', 'surge', 'delayed', 'idle', 'offline', 'N/A', 'critical', 'internal server error']
    ru_list = ['в норме', 'помехи', 'задержка', 'бездействие', 'офлайн', 'N/A', 'критическое', 'внутренняя ошибка сервера']
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
    unarmored_damage_head, unarmored_damage_chest_and_arm, unarmored_damage_stomach, unarmored_damage_leg = value_list[16], value_list[17], value_list[18], value_list[19]
    armored_damage_head, armored_damage_chest_and_arm, armored_damage_stomach, armored_damage_leg = value_list[20], value_list[21], value_list[22], value_list[23]
    for en, ru in zip(strings.origin_list_en, strings.origin_list_ru):
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
        if message.from_user.language_code in strings.CIS_lang_code:
                text = gun_data_text_ru
                markup = markup_guns_ru
        else:
                text = gun_data_text_en
                markup = markup_guns
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html') 
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def guns(message):
    try:
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '#️⃣ Выберите категорию, которая Вас интересует:'
            markup = markup_guns_ru
        else:
            text = '#️⃣ Select the category, that you are interested in:'
            markup = markup_guns
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def pistols(message):
    try:
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '🔫 Выберите пистолет..'
            markup = markup_pistols_ru
        else:
            text = '🔫 Choose the pistol..'
            markup = markup_pistols
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def smgs(message):
    try:
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '🔫 Выберите пистолет-пулемёт..'
            markup = markup_smgs_ru
        else:
            text = '🔫 Choose the SMG..'
            markup = markup_smgs
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def rifles(message):
    try:
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '🔫 Выберите винтовку..'
            markup = markup_rifles_ru
        else:
            text = '🔫 Choose the rifle..'
            markup = markup_rifles
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')
        send_about_problem_bot(message)

def heavy(message):
    try:
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '🔫 Выберите тяжёлое оружие..'
            markup = markup_heavy_ru
        else:
            text = '🔫 Choose the heavy gun..'
            markup = markup_heavy
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
            if message.from_user.language_code in strings.CIS_lang_code:
                text = '📶 Выберите регион, который Вам интересен, чтобы получить информацию о дата-центрах:'
                markup = markup_DC_ru
            else:
                text = '📶 Select the region, that you are interested in, to get information about the data centers:'
                markup = markup_DC
            bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}')
            send_about_problem_bot(message)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def back(message):
    if message.from_user.language_code in strings.CIS_lang_code:
        markup = markup_ru
    else:
        markup = markup_en
    bot.send_message(message.chat.id, '👌', reply_markup=markup)

def dc_europe(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '📍 Укажите регион...'
            markup = markup_DC_EU_ru            
        else:
            text = '📍 Specify the region...'
            markup = markup_DC_EU
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def dc_usa(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '📍 Укажите регион...'
            markup = markup_DC_USA_ru
        else:
            text = '📍 Specify the region...'
            markup = markup_DC_USA
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

def dc_asia(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        if message.from_user.language_code in strings.CIS_lang_code:
            text = '📍 Укажите страну...'
            markup = markup_DC_Asia_ru
        else:
            text = '📍 Specify the country...'
            markup = markup_DC_Asia
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif wsCache == 'maintenance':
        send_about_maintenance(message)
    else:
        send_about_problem_valve_api(message)

# Africa

def get_dc_africa():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    capacity, load, capacity_ru, load_ru = api_dc.africa_South()     
    africa_text_ru = strings.dc_africa_ru.format(load_ru, capacity_ru, tsRCache)
    africa_text_en = strings.dc_africa_en.format(load, capacity, tsCache)           
    return africa_text_en, africa_text_ru

def send_dc_africa(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            africa_text_en, africa_text_ru = get_dc_africa()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = africa_text_ru
                markup = markup_DC_ru
            else:
                text = africa_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.australia()     
    australia_text_ru = strings.dc_australia_ru.format(load_ru, capacity_ru, tsRCache)
    australia_text_en = strings.dc_australia_en.format(load, capacity, tsCache)           
    return australia_text_en, australia_text_ru

def send_dc_australia(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            australia_text_en, australia_text_ru = get_dc_australia()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = australia_text_ru
                markup = markup_DC_ru
            else:
                text = australia_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.eu_North()        
    eu_north_text_ru = strings.dc_north_eu_ru.format(load_ru, capacity_ru, tsRCache)
    eu_north_text_en = strings.dc_north_eu_en.format(load, capacity, tsCache)
    return eu_north_text_en, eu_north_text_ru

def send_dc_eu_north(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_north_text_en, eu_north_text_ru = get_dc_eu_north()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = eu_north_text_ru
                markup = markup_DC_ru
            else:
                text = eu_north_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru = api_dc.eu_West()
    eu_west_text_ru = strings.dc_west_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_west_text_en = strings.dc_west_eu_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_west_text_en, eu_west_text_ru

def send_dc_eu_west(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_west_text_en, eu_west_text_ru = get_dc_eu_west()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = eu_west_text_ru
                markup = markup_DC_ru
            else:
                text = eu_west_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru = api_dc.eu_East()
    eu_east_text_ru = strings.dc_east_eu_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_east_text_en = strings.dc_east_eu_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_east_text_en, eu_east_text_ru

def send_dc_eu_east(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_east_text_en, eu_east_text_ru = get_dc_eu_east()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = eu_east_text_ru
                markup = markup_DC_ru
            else:
                text = eu_east_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru = api_dc.usa_North()   
    usa_north_text_ru = strings.dc_north_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    usa_north_text_en = strings.dc_north_us_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return usa_north_text_en, usa_north_text_ru

def send_dc_usa_north(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_north_text_en, usa_north_text_ru = get_dc_usa_north()
            if message.from_user.language_code in strings.CIS_lang_code:        
                text = usa_north_text_ru
                markup = markup_DC_ru
            else:
                text = usa_north_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru = api_dc.usa_South()      
    usa_south_text_ru = strings.dc_south_us_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    usa_south_text_en = strings.dc_south_us_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return usa_south_text_en, usa_south_text_ru

def send_dc_usa_south(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_south_text_en, usa_south_text_ru = get_dc_usa_south()
            if message.from_user.language_code in strings.CIS_lang_code:        
                text = usa_south_text_ru
                markup = markup_DC_ru
            else:
                text = usa_south_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = api_dc.america_South()
    south_america_text_ru = strings.dc_south_america_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, load_quaternary_ru, capacity_quaternary_ru, tsRCache)
    south_america_text_en = strings.dc_south_america_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, load_quaternary, capacity_quaternary, tsCache)
    return south_america_text_en, south_america_text_ru

def send_dc_south_america(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            south_america_text_en, south_america_text_ru = get_dc_south_america()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = south_america_text_ru
                markup = markup_DC_ru
            else:
                text = south_america_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru = api_dc.india()
    india_text_ru = strings.dc_india_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    india_text_en = strings.dc_india_en.format(load, capacity, load_secondary, capacity_secondary, tsCache)
    return india_text_en, india_text_ru

def send_dc_india(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            india_text_en, india_text_ru = get_dc_india()
            if message.from_user.language_code in strings.CIS_lang_code:  
                text = india_text_ru
                markup = markup_DC_ru
            else:
                text = india_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.japan()
    japan_text_ru = strings.dc_japan_ru.format(load_ru, capacity_ru, tsRCache)
    japan_text_en = strings.dc_japan_en.format(load, capacity, tsCache)
    return japan_text_en, japan_text_ru

def send_dc_japan(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            japan_text_en, japan_text_ru = get_dc_japan()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = japan_text_ru
                markup = markup_DC_ru
            else:
                text = japan_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru = api_dc.china()
    china_text_ru = strings.dc_china_ru.format(load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    china_text_en = strings.dc_china_en.format(load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return china_text_en, china_text_ru

def send_dc_china(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            china_text_en, china_text_ru = get_dc_china()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = china_text_ru
                markup = markup_DC_ru
            else:
                text = china_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.emirates()     
    emirates_text_ru = strings.dc_emirates_ru.format(load_ru, capacity_ru, tsRCache)
    emirates_text_en = strings.dc_emirates_en.format(load, capacity, tsCache)           
    return emirates_text_en, emirates_text_ru

def send_dc_emirates(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            emirates_text_en, emirates_text_ru = get_dc_emirates()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = emirates_text_ru
                markup = markup_DC_ru
            else:
                text = emirates_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.singapore()     
    singapore_text_ru = strings.dc_singapore_ru.format(load_ru, capacity_ru, tsRCache)
    singapore_text_en = strings.dc_singapore_en.format(load, capacity, tsCache)           
    return singapore_text_en, singapore_text_ru

def send_dc_singapore(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            singapore_text_en, singapore_text_ru = get_dc_singapore()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = singapore_text_ru
                markup = markup_DC_ru
            else:
                text = singapore_text_en
                markup = markup_DC
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
    capacity, load, capacity_ru, load_ru = api_dc.hong_kong()     
    hong_kong_text_ru = strings.dc_hong_kong_ru.format(load_ru, capacity_ru, tsRCache)
    hong_kong_text_en = strings.dc_hong_kong_en.format(load, capacity, tsCache)           
    return hong_kong_text_en, hong_kong_text_ru

def send_dc_hong_kong(message):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            hong_kong_text_en, hong_kong_text_ru = get_dc_hong_kong()
            if message.from_user.language_code in strings.CIS_lang_code:
                text = hong_kong_text_ru
                markup = markup_DC_ru
            else:
                text = hong_kong_text_en
                markup = markup_DC
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
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            server_status_text_en, server_status_text_ru = get_server_status()
            devcount_text_en, devcount_text_ru = get_devcount()
            timer_text_en, timer_text_ru = get_timer()
            gameversion_text_en, gameversion_text_ru = get_gameversion()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    status_r, dev_r, timer_r, gv_r = server_status_text_ru, devcount_text_ru, timer_text_ru, gameversion_text_ru
                    title_status, title_dev, title_timer, title_gv = 'Статус', 'Бета-версия', 'Сброс ограничений', 'Версия игры'
                    description_status = 'Проверить доступность серверов'
                    description_dev = 'Показать количество онлайн разработчиков'
                    description_timer = 'Время до сброса ограничений опыта и дропа'
                    description_gv = 'Проверить последнюю версию игры'
                else:
                    status_r, dev_r, timer_r, gv_r = server_status_text_en, devcount_text_en, timer_text_en, gameversion_text_en
                    title_status, title_dev, title_timer, title_gv = 'Status', 'Beta version', 'Drop cap reset', 'Game version'
                    description_status = 'Check the availability of the servers'
                    description_dev = 'Show the count of in-game developers'
                    description_timer = 'Time left until experience and drop cap reset'
                    description_gv = 'Check the latest game version'
                r = types.InlineQueryResultArticle('1', title_status, input_message_content = types.InputTextMessageContent(status_r, parse_mode='html'), thumb_url='https://telegra.ph/file/57ba2b279c53d69d72481.jpg', description=description_status)
                r2 = types.InlineQueryResultArticle('2', title_dev, input_message_content = types.InputTextMessageContent(dev_r, parse_mode='html'), thumb_url='https://telegra.ph/file/24b05cea99de936fd12bf.jpg', description=description_dev)
                r3 = types.InlineQueryResultArticle('3', title_timer, input_message_content = types.InputTextMessageContent(timer_r), thumb_url='https://telegra.ph/file/6948255408689d2f6a472.jpg', description=description_timer)
                r4 = types.InlineQueryResultArticle('4', title_gv, input_message_content = types.InputTextMessageContent(gv_r, parse_mode='html'), thumb_url='https://telegra.ph/file/82d8df1e9f5140da70232.jpg', description=description_gv)
                bot.answer_inline_query(inline_query.id, [r, r2, r3, r4], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        try:
            timer_text_en, timer_text_ru = get_timer()
            gameversion_text_en, gameversion_text_ru = get_gameversion()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    maintenance_r, timer_r, gv_r = strings.maintenance_ru, timer_text_ru, gameversion_text_ru
                    title_maintenance, title_timer, title_gv = 'Нет данных', 'Сброс ограничений', 'Версия игры'
                    description_mntn = 'Еженедельное тех. обслуживание серверов'
                    description_timer = 'Время до сброса ограничений опыта и дропа'
                    description_gv = 'Проверить последнюю версию игры'
                else:
                    maintenance_r, timer_r, gv_r = strings.maintenance_en, timer_text_en, gameversion_text_en
                    title_maintenance, title_timer, title_gv = 'No data', 'Drop cap reset', 'Game version'
                    description_mntn = 'Weekly server maintenance'
                    description_timer = 'Time left until experience and drop cap reset'
                    description_gv = 'Check the latest game version'
                r = types.InlineQueryResultArticle('1', title_maintenance, input_message_content = types.InputTextMessageContent(maintenance_r), thumb_url='https://telegra.ph/file/6120ece0aab30d8c59d07.jpg', description=description_mntn)
                r2 = types.InlineQueryResultArticle('2', title_timer, input_message_content = types.InputTextMessageContent(timer_r), thumb_url='https://telegra.ph/file/6948255408689d2f6a472.jpg', description=description_timer)
                r4 = types.InlineQueryResultArticle('3', title_gv, input_message_content = types.InputTextMessageContent(gv_r, parse_mode='html'), thumb_url='https://telegra.ph/file/82d8df1e9f5140da70232.jpg', description=description_gv)
                bot.answer_inline_query(inline_query.id, [r, r2, r3], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️Error: {e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️Error: {e}\n\n↩️ inline_query')
    else:
        try:
            timer_text_en, timer_text_ru = get_timer()
            gameversion_text_en, gameversion_text_ru = get_gameversion()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    wrong_r, timer_r, gv_r = strings.wrongAPI_ru, timer_text_ru, gameversion_text_ru
                    title_un, title_timer, title_gv = 'Нет данных', 'Сброс ограничений', 'Версия игры'
                    description_un = 'Не получилось связаться с API Valve'
                    description_timer = 'Время до сброса ограничений опыта и дропа'
                    description_gv = 'Проверить последнюю версию игры'
                else:
                    wrong_r, timer_r, gv_r = strings.wrongAPI_en, timer_text_en, gameversion_text_en
                    title_un, title_timer, title_gv = 'No data', 'Drop cap reset', 'Game version'
                    description_un = 'Unable to call Valve API'
                    description_timer = 'Time left until experience and drop cap reset'
                    description_gv = 'Check the latest game version'
                r = types.InlineQueryResultArticle('1', title_un, input_message_content = types.InputTextMessageContent(wrong_r), thumb_url='https://telegra.ph/file/b9d408e334795b014ee5c.jpg', description=description_un)
                r2 = types.InlineQueryResultArticle('2', title_timer, input_message_content = types.InputTextMessageContent(timer_r), thumb_url='https://telegra.ph/file/6948255408689d2f6a472.jpg', description=description_timer)
                r3 = types.InlineQueryResultArticle('3', title_gv, input_message_content = types.InputTextMessageContent(gv_r, parse_mode='html'), thumb_url='https://telegra.ph/file/82d8df1e9f5140da70232.jpg', description=description_gv)
                bot.answer_inline_query(inline_query.id, [r, r2, r3], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️Error: {e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')

# DC
@bot.inline_handler(lambda query: query.query.lower() in strings.dc_tags)
def inline_dc(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
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
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title_china = 'Китайские ДЦ'
                    title_emirates = 'Эмиратский ДЦ'
                    title_hong_kong = 'Гонконгский ДЦ'
                    title_india = 'Индийские ДЦ'
                    title_japan = 'Японский ДЦ'
                    title_singapore = 'Сингапурский ДЦ'
                    title_eu_north = 'Североевропейский ДЦ'
                    title_eu_east = 'Восточноевропейские ДЦ'
                    title_eu_west = 'Западноевропейские ДЦ'
                    title_usa_north = 'ДЦ северной части США'
                    title_usa_south = 'ДЦ южной части США'
                    title_australia = 'Австралийский ДЦ'
                    title_africa = 'Африканский ДЦ'
                    title_south_america = 'Южноамериканские ДЦ' 
                    r_africa = africa_text_ru
                    r_australia = australia_text_ru
                    r_usa_north = usa_north_text_ru
                    r_usa_south = usa_south_text_ru
                    r_eu_north = eu_north_text_ru
                    r_eu_east = eu_east_text_ru
                    r_eu_west = eu_west_text_ru
                    r_china = china_text_ru
                    r_emirates = emirates_text_ru
                    r_hong_kong = hong_kong_text_ru
                    r_india = india_text_ru
                    r_japan = japan_text_ru
                    r_singapore = singapore_text_ru
                    r_south_america = south_america_text_ru
                    description = 'Проверить состояние'
                else:
                    title_usa_north = 'Northern USA DC'
                    title_usa_south = 'Southern USA DC'
                    title_eu_north = 'North European DC'
                    title_eu_east = 'East European DC'
                    title_eu_west = 'West European DC'
                    title_china = 'Chinese DC'
                    title_emirates = 'Emirati DC'
                    title_hong_kong = 'Hong Kongese DC'
                    title_india = 'Indian DC'
                    title_japan= 'Japanese DC'
                    title_singapore = 'Singaporean DC'
                    title_australia = 'Australian DC'
                    title_africa = 'African DC'
                    title_south_america = 'South American DC'
                    r_africa = africa_text_en
                    r_australia = australia_text_en
                    r_usa_north = usa_north_text_en
                    r_usa_south = usa_south_text_en
                    r_eu_north = eu_north_text_en
                    r_eu_east = eu_east_text_en
                    r_eu_west = eu_west_text_en
                    r_china = china_text_en
                    r_emirates = emirates_text_en
                    r_hong_kong = hong_kong_text_en
                    r_india = india_text_en
                    r_japan = japan_text_en
                    r_singapore = singapore_text_en
                    r_south_america = south_america_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title_eu_north, input_message_content = types.InputTextMessageContent(r_eu_north), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                r2 = types.InlineQueryResultArticle('2', title_eu_east, input_message_content = types.InputTextMessageContent(r_eu_east), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                r3 = types.InlineQueryResultArticle('3', title_eu_west, input_message_content = types.InputTextMessageContent(r_eu_west), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                r4 = types.InlineQueryResultArticle('4', title_emirates, input_message_content = types.InputTextMessageContent(r_emirates), thumb_url='https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', description=description)
                r5 = types.InlineQueryResultArticle('5', title_china, input_message_content = types.InputTextMessageContent(r_china), thumb_url='https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg', description=description)
                r6 = types.InlineQueryResultArticle('6', title_hong_kong, input_message_content = types.InputTextMessageContent(r_hong_kong), thumb_url='https://telegra.ph/file/0b209e65c421910419f34.jpg', description=description)
                r7 = types.InlineQueryResultArticle('7', title_india, input_message_content = types.InputTextMessageContent(r_india), thumb_url='https://telegra.ph/file/b2213992b750940113b69.jpg', description=description)
                r8 = types.InlineQueryResultArticle('8', title_japan, input_message_content = types.InputTextMessageContent(r_japan), thumb_url='https://telegra.ph/file/11b6601a3e60940d59c88.jpg', description=description)
                r9 = types.InlineQueryResultArticle('9', title_singapore, input_message_content = types.InputTextMessageContent(r_singapore), thumb_url='https://telegra.ph/file/1c2121ceec5d1482173d5.jpg', description=description)
                r10 = types.InlineQueryResultArticle('10', title_africa, input_message_content = types.InputTextMessageContent(r_africa), thumb_url='https://telegra.ph/file/12628c8193b48302722e8.jpg', description=description)
                r11 = types.InlineQueryResultArticle('11', title_usa_north, input_message_content = types.InputTextMessageContent(r_usa_north), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)
                r12 = types.InlineQueryResultArticle('12', title_usa_south, input_message_content = types.InputTextMessageContent(r_usa_south), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)                
                r13 = types.InlineQueryResultArticle('13', title_australia, input_message_content = types.InputTextMessageContent(r_australia), thumb_url='https://telegra.ph/file/5dc6beef1556ea852284c.jpg', description=description)
                r14 = types.InlineQueryResultArticle('14', title_south_america, input_message_content = types.InputTextMessageContent(r_south_america), thumb_url='https://telegra.ph/file/60f8226ea5d72815bef57.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General Australia
@bot.inline_handler(lambda query: query.query.lower() in strings.australian_tags)
def inline_dc_australia(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            australia_text_en, australia_text_ru = get_dc_australia()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Австралийский ДЦ'
                    r = australia_text_ru
                    description = 'Проверить состояние' 
                else:
                    title = 'Australian DC'
                    r = australia_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/5dc6beef1556ea852284c.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General Africa
@bot.inline_handler(lambda query: query.query.lower() in strings.african_tags)
def inline_dc_africa(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            africa_text_en, africa_text_ru = get_dc_africa()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Африканский ДЦ'
                    r = africa_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'African DC'
                    r = africa_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/12628c8193b48302722e8.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General South America
@bot.inline_handler(lambda query: query.query.lower() in strings.south_american_tags)
def inline_dc_south_america(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            south_america_text_en, south_america_text_ru = get_dc_south_america()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Южноамериканские ДЦ'
                    r = south_america_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'South American DC'
                    r = south_america_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/60f8226ea5d72815bef57.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General Europe
@bot.inline_handler(lambda query: query.query.lower() in strings.european_tags)
def inline_dc_europe(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_north_text_en, eu_north_text_ru = get_dc_eu_north()
            eu_east_text_en, eu_east_text_ru = get_dc_eu_east()
            eu_west_text_en, eu_west_text_ru = get_dc_eu_west()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title_north = 'Североевропейский ДЦ'
                    title_east = 'Восточноевропейские ДЦ'
                    title_west = 'Западноевропейские ДЦ'
                    r_north = eu_north_text_ru
                    r_east = eu_east_text_ru
                    r_west = eu_west_text_ru
                    description = 'Проверить состояние'
                else:
                    title_north = 'North European DC'
                    title_east = 'East European DC'
                    title_west = 'West European DC'
                    r_north = eu_north_text_en
                    r_east = eu_east_text_en
                    r_west = eu_west_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title_north, input_message_content = types.InputTextMessageContent(r_north), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                r2 = types.InlineQueryResultArticle('2', title_east, input_message_content = types.InputTextMessageContent(r_east), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                r3 = types.InlineQueryResultArticle('3', title_west, input_message_content = types.InputTextMessageContent(r_west), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                
                bot.answer_inline_query(inline_query.id, [r, r2, r3], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed North Europe
@bot.inline_handler(lambda query: query.query.lower() in strings.north_european_tags)
def inline_dc_eu_north(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_north_text_en, eu_north_text_ru = get_dc_eu_north()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Североевропейский ДЦ'
                    r = eu_north_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'North European DC'
                    r = eu_north_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed East Europe
@bot.inline_handler(lambda query: query.query.lower() in strings.east_european_tags)
def inline_dc_eu_east(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_east_text_en, eu_east_text_ru = get_dc_eu_east()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Восточноевропейские ДЦ'
                    r = eu_east_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'East European DC'
                    r = eu_east_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed West Europe
@bot.inline_handler(lambda query: query.query.lower() in strings.west_european_tags)
def inline_dc_eu_west(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            eu_west_text_en, eu_west_text_ru = get_dc_eu_west()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Западноевропейские ДЦ'
                    r = eu_west_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'West European DC'
                    r = eu_west_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/4d269cb98aadaae391024.jpg', description=description)
                
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General USA
@bot.inline_handler(lambda query: query.query.lower() in strings.american_tags)
def inline_dc_usa(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_north_text_en, usa_north_text_ru = get_dc_usa_north()
            usa_south_text_en, usa_south_text_ru = get_dc_usa_south()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title_north = 'ДЦ северной части США'
                    title_south = 'ДЦ южной части США'
                    r_north = usa_north_text_ru
                    r_south = usa_south_text_ru
                    description = 'Проверить состояние'
                else:
                    title_north = 'Northern USA DC'
                    title_south = 'Southern USA DC'
                    r_north = usa_north_text_en
                    r_south = usa_south_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title_north, input_message_content = types.InputTextMessageContent(r_north), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)
                r2 = types.InlineQueryResultArticle('2', title_south, input_message_content = types.InputTextMessageContent(r_south), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)                
                bot.answer_inline_query(inline_query.id, [r, r2], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Northern USA
@bot.inline_handler(lambda query: query.query.lower() in strings.northern_usa_tags)
def inline_dc_northern_usa(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_north_text_en, usa_north_text_ru = get_dc_usa_north()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'ДЦ северной части США'
                    r = usa_north_text_ru
                    description = 'Проверить состояние'
                else:
                    title_north = 'Northern USA DC'
                    r_north = usa_north_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Southern USA
@bot.inline_handler(lambda query: query.query.lower() in strings.southern_usa_tags)
def inline_dc_southern_usa(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            usa_south_text_en, usa_south_text_ru = get_dc_usa_south()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'ДЦ южной части США'
                    r = usa_south_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'Southern USA DC'
                    r = usa_south_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/06119c30872031d1047d0.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# General Asia
@bot.inline_handler(lambda query: query.query.lower() in strings.asian_tags)
def inline_dc_asia(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            china_text_en, china_text_ru = get_dc_china()
            emirates_text_en, emirates_text_ru = get_dc_emirates()
            hong_kong_text_en, hong_kong_text_ru = get_dc_hong_kong()
            india_text_en, india_text_ru = get_dc_india()
            japan_text_en, japan_text_ru = get_dc_japan()
            singapore_text_en, singapore_text_ru = get_dc_singapore()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title_china = 'Китайские ДЦ'
                    title_emirates = 'Эмиратский ДЦ'
                    title_hong_kong = 'Гонконгский ДЦ'
                    title_india = 'Индийские ДЦ'
                    title_japan = 'Японский ДЦ'
                    title_singapore = 'Сингапурский ДЦ'
                    r_china = china_text_ru
                    r_emirates = emirates_text_ru
                    r_hong_kong = hong_kong_text_ru
                    r_india = india_text_ru
                    r_japan = japan_text_ru
                    r_singapore = singapore_text_ru
                    description = 'Проверить состояние'
                else:
                    title_china = 'Chinese DC'
                    title_emirates = 'Emirati DC'
                    title_hong_kong = 'Hong Kongese DC'
                    title_india = 'Indian DC'
                    title_japan= 'Japanese DC'
                    title_singapore = 'Singaporean DC'
                    r_china = china_text_en
                    r_emirates = emirates_text_en
                    r_hong_kong = hong_kong_text_en
                    r_india = india_text_en
                    r_japan = japan_text_en
                    r_singapore = singapore_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title_china, input_message_content = types.InputTextMessageContent(r_china), thumb_url='https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg', description=description)
                r2 = types.InlineQueryResultArticle('2', title_emirates, input_message_content = types.InputTextMessageContent(r_emirates), thumb_url='https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', description=description)
                r3 = types.InlineQueryResultArticle('3', title_hong_kong, input_message_content = types.InputTextMessageContent(r_hong_kong), thumb_url='https://telegra.ph/file/0b209e65c421910419f34.jpg', description=description)
                r4 = types.InlineQueryResultArticle('4', title_india, input_message_content = types.InputTextMessageContent(r_india), thumb_url='https://telegra.ph/file/b2213992b750940113b69.jpg', description=description)
                r5 = types.InlineQueryResultArticle('5', title_japan, input_message_content = types.InputTextMessageContent(r_japan), thumb_url='https://telegra.ph/file/11b6601a3e60940d59c88.jpg', description=description)
                r6 = types.InlineQueryResultArticle('6', title_singapore, input_message_content = types.InputTextMessageContent(r_singapore), thumb_url='https://telegra.ph/file/1c2121ceec5d1482173d5.jpg', description=description)
                
                bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed China
@bot.inline_handler(lambda query: query.query.lower() in strings.chinese_tags)
def inline_dc_china(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            china_text_en, china_text_ru = get_dc_china()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Китайские ДЦ'
                    r = china_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'Chinese DC'
                    r = china_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/ff0dad30ae32144d7cd0c.jpg', description=description)                
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Emirates
@bot.inline_handler(lambda query: query.query.lower() in strings.emirati_tags)
def inline_dc_emirates(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            emirates_text_en, emirates_text_ru = get_dc_emirates()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Эмиратский ДЦ'
                    r = emirates_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'Emirati DC'
                    r = emirates_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/1de1e51e62b79cae5181a.jpg', description=description)

                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Hong Kong
@bot.inline_handler(lambda query: query.query.lower() in strings.hong_kongese_tags)
def inline_dc_hong_kong(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            hong_kong_text_en, hong_kong_text_ru = get_dc_hong_kong()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Гонконгский ДЦ'
                    r = hong_kong_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'Hong Kongese DC'
                    r = hong_kong_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/0b209e65c421910419f34.jpg', description=description)               
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed India
@bot.inline_handler(lambda query: query.query.lower() in strings.indian_tags)
def inline_dc_india(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            india_text_en, india_text_ru = get_dc_india()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Индийские ДЦ'
                    r = india_text_ru
                    description = 'Проверить состояние'
                else:
                    title = 'Indian DC'
                    r = india_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/b2213992b750940113b69.jpg', description=description)                
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Japan
@bot.inline_handler(lambda query: query.query.lower() in strings.japanese_tags)
def inline_dc_japan(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            japan_text_en, japan_text_ru = get_dc_japan()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Японский ДЦ'
                    r = japan_text_ru
                    description = 'Проверить состояние'
                else:
                    title= 'Japanese DC'
                    r = japan_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/11b6601a3e60940d59c88.jpg', description=description)              
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)

# Detailed Singapore
@bot.inline_handler(lambda query: query.query.lower() in strings.singaporean_tags)
def inline_dc_singapore(inline_query):
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    wsCache = cacheFile['valve_webapi']
    if wsCache == 'normal':
        try:
            singapore_text_en, singapore_text_ru = get_dc_singapore()
            try:
                if inline_query.from_user.language_code in strings.CIS_lang_code:
                    title = 'Сингапурский ДЦ'
                    r = singapore_text_ru
                    description = 'Проверить состояние'
                else:

                    title = 'Singaporean DC'
                    r = singapore_text_en
                    description = 'Check the status'
                r = types.InlineQueryResultArticle('1', title, input_message_content = types.InputTextMessageContent(r), thumb_url='https://telegra.ph/file/1c2121ceec5d1482173d5.jpg', description=description)
                bot.answer_inline_query(inline_query.id, [r], cache_time=5)
                log_inline(inline_query)
            except Exception as e:
                bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
        except Exception as e:
            bot.send_message(config.LOGCHANNEL, f'❗️{e}\n\n↩️ inline_query')
    elif wsCache == 'maintenance':
        send_about_maintenance_inline(inline_query)
    else:
        send_about_problem_valve_api_inline(inline_query)


### Commands setup ###


@bot.message_handler(commands=['start'])
def welcome(message):
    '''First bot's message'''
    data = pd.read_csv(config.USER_DB_FILE_PATH)
    if not data['UserID'].isin([message.from_user.id]).any():
        new_data = pd.DataFrame([[message.from_user.first_name, message.from_user.id]], columns=['Name', 'UserID'])
        pd.concat([data, new_data]).to_csv(config.USER_DB_FILE_PATH, index=False)
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in strings.CIS_lang_code:
            text = strings.cmdStart_ru.format(message.from_user.first_name)
            markup = markup_ru
        else:
            text = strings.cmdStart_en.format(message.from_user.first_name)
            markup = markup_en
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
        if message.from_user.language_code in strings.CIS_lang_code:
            text = strings.cmdFeedback_ru 
        else:
            text = strings.cmdFeedback_en
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup_del)
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
        if message.from_user.language_code in strings.CIS_lang_code:
            markup = markup_ru
        else:
            markup = markup_en
        bot.send_message(message.chat.id, '👍', reply_markup=markup)

    else:
        bot.send_message(config.OWNER, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', parse_mode='html', disable_notification=True)
        bot.forward_message(config.OWNER, message.chat.id, message.message_id)
        
        if not config.TEST_MODE:
            bot.send_message(config.AQ, f'🆔 <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>:', parse_mode='html', disable_notification=True)
            bot.forward_message(config.AQ, message.chat.id, message.message_id)

        if message.from_user.language_code in strings.CIS_lang_code:
            text = 'Отлично! Ваше сообщение отправлено.'
            markup = markup_ru
        else:
            text = 'Awesome! Your message has been sent.'
            markup = markup_en

        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id,reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    '''/help message'''
    log(message)
    if message.chat.type == 'private':
        if message.from_user.language_code in strings.CIS_lang_code:
            text = strings.cmdHelp_ru
            markup = markup_ru
        else:
            text = strings.cmdHelp_en
            markup = markup_en
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

@bot.message_handler(commands=['delkey'])
def delete_keyboard(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, '👍', reply_markup=markup_del)
    time.sleep(10)
    bot.delete_message(message.chat.id, message.message_id+1)

def chuj(message):
    for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
        send_gun_info(gName, gId)
        
@bot.message_handler(content_types=['text'])
def answer(message):
    '''Answer of the bot'''
    log(message)
    try:
        if message.chat.type == 'private':
            bot.send_chat_action(message.chat.id, 'typing')

            if message.text.lower() in strings.status_tags:
                send_server_status(message)
            
            elif message.text.lower() in strings.dev_count_tags:
                send_devcount(message)
    
            elif message.text.lower() in strings.cap_reset_tags:
                send_timer(message)

            elif message.text.lower() in strings.gameversion_tags:
                send_gameversion(message)

            elif message.text.lower() in strings.gun_tags:
                guns(message)

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

            elif message.text.lower() in strings.gun_name_list:
                for gName, gId in zip(strings.gun_name_list, strings.gun_id_list):
                    if message.text.lower() == gName:
                        send_gun_info(message, gId)

            elif message.text == '⏪ Back' or message.text == '⏪ Назад':
                back(message)

            elif message.text == '⏪ Bаck' or message.text == '⏪ Нaзад':
                dc(message)
                
            elif message.text == '⏪ Bасk' or message.text == '⏪ Haзад':
                guns(message)


            else:
                if message.from_user.language_code in strings.CIS_lang_code:
                    text = strings.unknownRequest_ru
                    markup = markup_ru
                else: 
                    text = strings.unknownRequest_en
                    markup = markup_en

                bot.send_message(message.chat.id, text, reply_markup=markup)
                
        else:
            if message.from_user.id == 777000:
                if message.forward_from_chat.id == config.CSGOBETACHANNEL and 'Обновлены файлы локализации' in message.text:
                    bot.send_sticker(config.CSGOBETACHAT, 'CAACAgIAAxkBAAID-l_9tlLJhZQSgqsMUAvLv0r8qhxSAAIKAwAC-p_xGJ-m4XRqvoOzHgQ', reply_to_message_id=message.message_id)
    
    except Exception as e:
        bot.send_message(config.LOGCHANNEL, f'❗️{e}')


### Polling ###


bot.polling(True)