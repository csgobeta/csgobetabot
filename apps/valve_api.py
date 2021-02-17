import requests
import config

from datetime import datetime

API_server_status = f'https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1?key={config.KEY}'
API_csgo_players = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=730' 
API_dev_players = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=710'


def get_response():
    response = requests.get(API_server_status)
    response = response.json()
    result = response['result']
    return result

def translate(data):
    en_list = ['offline', 'idle', 'low', 'medium', 'high', 'full']
    ru_list = ['офлайн', 'никакая', 'низкая', 'средняя', 'высокая', 'полная']
    for en, ru in zip(en_list, ru_list):
        if data in en:
            data_ru = ru
            return data_ru


class ValveServersAPI:

    def get_status(self): 
        try:
            result = get_response()

            matchmaking = result['matchmaking']
            
            scheduler = matchmaking['scheduler']
            sessionsLogon = result['services']['SessionsLogon']
            steam_community = result['services']['SteamCommunity']
            
            online_servers = matchmaking['online_servers']
            online_players = matchmaking['online_players']
            searching_players = matchmaking['searching_players']        
            search_seconds_avg = matchmaking['search_seconds_avg']
            
            timestamp = result['app']['timestamp']

            return scheduler, sessionsLogon, online_servers, online_players, timestamp, search_seconds_avg, searching_players, steam_community
        except:
            scheduler = sessionsLogon = steam_community = 'N/A'
            timestamp = online_servers = online_players = search_seconds_avg = searching_players = 0
            return scheduler, sessionsLogon, online_servers, online_players, timestamp, search_seconds_avg, searching_players, steam_community
            
    def get_players(self):
        try:
            response = requests.get(API_csgo_players)
            data = response.json()
            player_count = data['response']['player_count']
            return player_count
        except:
            player_count = 0
            return player_count
            
    def get_devs(self):
        try:
            response = requests.get(API_dev_players)
            data = response.json()
            dev_player_count = data['response']['player_count']
            return dev_player_count
        except:
            dev_player_count = 0
            return dev_player_count
            
    def check_status(self):
        try:
            response = requests.get(API_server_status)
            if response.status_code == 200:
                webapi_status = 'normal'
            elif response.status_code != 200 and datetime.today().weekday() == 1:
                webapi_status = 'maintenance'
            else:
                webapi_status = 'N/A'
            return webapi_status
        except:
            webapi_status = 'N/A'
            return webapi_status
    
class ValveServersDataCentersAPI:

    #
    #   Australia
    #
    """Australia (Sydney)"""
    def australia(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Australia']['capacity']
            load = result['datacenters']['Australia']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru

 
    #
    #   South Africa
    #
    """South Africa (Johannesburg)"""
    def africa_South(self):
        try:
            result = get_response()
            capacity = result['datacenters']['South Africa']['capacity']
            load = result['datacenters']['South Africa']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru
    
    #
    #   South America
    #
    """Brazil (Sao Paulo) && Chile (Santiago) && Peru (Lima) && Argentina (Buenos Aires)"""
    def america_South(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Brazil']['capacity']
            load = result['datacenters']['Brazil']['load']
            capacity_secondary = result['datacenters']['Chile']['capacity']
            load_secondary = result['datacenters']['Chile']['load']
            capacity_tertiary = result['datacenters']['Peru']['capacity']
            load_tertiary = result['datacenters']['Peru']['load']
            capacity_quaternary = result['datacenters']['Argentina']['capacity']
            load_quaternary = result['datacenters']['Argentina']['load']
            array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary, capacity_quaternary, load_quaternary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            capacity_tertiary_ru, load_tertiary_ru = array_ru[4], array_ru[5]
            capacity_quaternary_ru, load_quaternary_ru = array_ru[6], array_ru[7]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

    #
    #   USA
    #
    """US Northcentral (Chicago) && US Northeast (Sterling) && US Northwest (Moses Lake)"""
    def usa_North(self):
        try:
            result = get_response()
            capacity = result['datacenters']['US Northcentral']['capacity']
            load = result['datacenters']['US Northcentral']['load']
            capacity_secondary = result['datacenters']['US Northeast']['capacity']
            load_secondary = result['datacenters']['US Northeast']['load']
            capacity_tertiary = result['datacenters']['US Northwest']['capacity']
            load_tertiary = result['datacenters']['US Northwest']['load']
            array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            capacity_tertiary_ru, load_tertiary_ru = array_ru[4], array_ru[5]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru

    """US Southwest (Los Angeles) && US Southeast (Atlanta)"""
    def usa_South(self):
        try:
            result = get_response()
            capacity = result['datacenters']['US Southwest']['capacity']
            load = result['datacenters']['US Southwest']['load']
            capacity_secondary = result['datacenters']['US Southeast']['capacity']
            load_secondary = result['datacenters']['US Southeast']['load']
            array = [capacity, load, capacity_secondary, load_secondary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru

    #
    #   Europe
    #

    """EU West (Luxembourg) && Spain (Mardid)"""   
    def eu_West(self):
        try:
            result = get_response()
            capacity = result['datacenters']['EU West']['capacity']
            load = result['datacenters']['EU West']['load']
            capacity_secondary = result['datacenters']['Spain']['capacity']
            load_secondary = result['datacenters']['Spain']['load']
            array = [capacity, load, capacity_secondary, load_secondary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru

    """EU East (Vienna) && Poland (Warsaw)"""
    def eu_East(self):
        try:
            result = get_response()
            capacity = result['datacenters']['EU East']['capacity']
            load = result['datacenters']['EU East']['load']
            capacity_secondary = result['datacenters']['Poland']['capacity']
            load_secondary = result['datacenters']['Poland']['load']
            array = [capacity, load, capacity_secondary, load_secondary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru

    """EU North (Stockholm)"""
    def eu_North(self):
        try:
            result = get_response()
            capacity = result['datacenters']['EU North']['capacity']
            load = result['datacenters']['EU North']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru
    
    #
    #    Asia   
    #

    """India (Mumbai) && India East (Chennai)"""
    def india(self):
        try:
            result = get_response()
            capacity = result['datacenters']['India']['capacity']
            load = result['datacenters']['India']['load']
            capacity_secondary = result['datacenters']['India East']['capacity']
            load_secondary = result['datacenters']['India East']['load']
            array = [capacity, load, capacity_secondary, load_secondary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru

    """Japan (Tokyo)"""
    def japan(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Japan']['capacity']
            load = result['datacenters']['Japan']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru

    """Emirates (Dubai)"""
    def emirates(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Emirates']['capacity']
            load = result['datacenters']['Emirates']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru

    """China Shanghai && China Tianjin && China Guangzhou"""
    def china(self):
        try:
            result = get_response()
            capacity = result['datacenters']['China Shanghai']['capacity']
            load = result['datacenters']['China Shanghai']['load']
            capacity_secondary = result['datacenters']['China Tianjin']['capacity']
            load_secondary = result['datacenters']['China Tianjin']['load']
            capacity_tertiary = result['datacenters']['China Guangzhou']['capacity']
            load_tertiary = result['datacenters']['China Guangzhou']['load']
            array = [capacity, load, capacity_secondary, load_secondary, capacity_tertiary, load_tertiary]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            capacity_secondary_ru, load_secondary_ru = array_ru[2], array_ru[3]
            capacity_tertiary_ru, load_tertiary_ru = array_ru[4], array_ru[5]
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru
    """Singapore"""
    def singapore(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Singapore']['capacity']
            load = result['datacenters']['Singapore']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru

    """Hong Kong"""
    def hong_kong(self):
        try:
            result = get_response()
            capacity = result['datacenters']['Hong Kong']['capacity']
            load = result['datacenters']['Hong Kong']['load']
            array = [capacity, load]
            array_ru = []
            for data in array:
                data_ru = translate(data)
                array_ru.append(data_ru)
            capacity_ru, load_ru = array_ru[0], array_ru[1]
            return capacity, load, capacity_ru, load_ru
        except:
            capacity = load = capacity_ru = load_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru