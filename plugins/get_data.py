import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from apps.timer import get_time
from apps import file_manager
from plugins import strings
from plugins.addons import time_converter
from plugins.addons import translate

import config

def server_status():
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

def mm_stats():
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

def devcount():
    '''Get the count of online devs'''
    tsCache, tsRCache, tsVCache = time_converter()[0], time_converter()[1], time_converter()[4]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url2']
    dcCache, dpCache = cacheFile['dev_player_count'], cacheFile['dev_all_time_peak']
    devcount_text_en = strings.devCount_en.format(url, dcCache, dpCache, tsCache, tsVCache)
    devcount_text_ru = strings.devCount_ru.format(url, dcCache, dpCache, tsRCache, tsVCache)
    return devcount_text_en, devcount_text_ru

def timer():
    '''Get drop cap reset time'''
    delta_days, delta_hours, delta_mins, delta_secs = get_time()
    timer_text_en = strings.timer_en.format(delta_days, delta_hours, delta_mins, delta_secs)
    timer_text_ru = strings.timer_ru.format(delta_days, delta_hours, delta_mins, delta_secs)
    return timer_text_en, timer_text_ru

def gameversion():
    '''Get the version of the game'''
    vdCache, vdRCache = time_converter()[2], time_converter()[3]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    cvCache, svCache, pvCache = cacheFile['client_version'], cacheFile['server_version'], cacheFile['patch_version']
    gameversion_text_en = strings.gameversion_en.format(pvCache, cvCache, svCache, vdCache)
    gameversion_text_ru = strings.gameversion_ru.format(pvCache, cvCache, svCache, vdRCache)
    return gameversion_text_en, gameversion_text_ru

def gun_info(gun_id):
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

### DATA CENTERS ###

def dc_africa():
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

def dc_australia():
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

def dc_eu_north():
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

def dc_eu_west():
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

def dc_eu_east():
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

def dc_usa_north():
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

def dc_usa_south():
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

def dc_south_america():
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

def dc_india():
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

def dc_japan():
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

def dc_china():
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

def dc_emirates():
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

def dc_singapore():
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

def dc_hong_kong():
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