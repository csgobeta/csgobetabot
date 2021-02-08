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

def translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw):
    capacity_ru = load_ru = capacity_secondary_ru = load_secondary_ru = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary_ru = load_quaternary_ru = ''
    capacity = capacity_raw
    capacity_secondary = capacity_secondary_raw
    capacity_tertiary = capacity_tertiary_raw
    capacity_quaternary = capacity_quaternary_raw
    load = load_raw
    load_secondary = load_secondary_raw
    load_tertiary = load_tertiary_raw
    load_quaternary = load_quaternary_raw

    raw_list_en = ['offline', 'idle', 'low', 'medium', 'high', 'full']
    raw_list_ru = ['офлайн', 'никакая', 'низкая', 'средняя', 'высокая', 'полная']

    for en, ru in zip(raw_list_en, raw_list_ru):
        if capacity in en:
            capacity_ru = ru
        if capacity_secondary in en:
            capacity_secondary_ru = ru
        if capacity_tertiary in en:
            capacity_tertiary_ru = ru
        if capacity_quaternary in en:
            capacity_quaternary_ru = ru
            
        if load in en:
            load_ru = ru
        if load_secondary in en:
            load_secondary_ru = ru
        if load_tertiary in en:
            load_tertiary_ru = ru
        if load_quaternary in en:
            load_quaternary_ru = ru

    return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

class ValveServersAPI:

    def get_status(self): 
        try:
            result = get_response()

            matchmaking = result['matchmaking']
            
            scheduler = matchmaking['scheduler']
            sessionsLogon = result['services']['SessionsLogon']
            
            online_servers = matchmaking['online_servers']
            online_players = matchmaking['online_players']
            searching_players = matchmaking['searching_players']        
            search_seconds_avg = matchmaking['search_seconds_avg']
            
            timestamp = result['app']['timestamp']

            return scheduler, sessionsLogon, online_servers, online_players, timestamp, search_seconds_avg, searching_players
        except:
            scheduler = sessionsLogon = timestamp = 'N/A' 
            online_servers = online_players = search_seconds_avg = searching_players = 000
            return scheduler, sessionsLogon, online_servers, online_players, timestamp, search_seconds_avg, searching_players
            
    def get_players(self):
        try:
            response = requests.get(API_csgo_players)
            data = response.json()
            player_count = data['response']['player_count']

            return player_count
        except:
            player_count = 000
            return player_count
            
    def get_devs(self):
        try:
            response = requests.get(API_dev_players)
            data = response.json()
            dev_player_count = data['response']['player_count']

            return dev_player_count
        except:
            dev_player_count = 000
            return dev_player_count
            
    def check_status(self):
        try:
            response = requests.get(API_server_status)
            if response.status_code == 200:
                webapi_status = 'Normal'
            elif response.status_code != 200 and datetime.datetime.today().weekday() == 1:
                webapi_status = 'Maintenance'
            else:
                webapi_status = 'N/A'
            return webapi_status
        except requests.ConnectionError:
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
            capacity_raw = result['datacenters']['Australia']['capacity']
            load_raw = result['datacenters']['Australia']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

 
    #
    #   South Africa
    #
    """South Africa (Johannesburg)"""
    def africa_South(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['South Africa']['capacity']
            load_raw = result['datacenters']['South Africa']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
    
    #
    #   South America
    #
    """Brazil (Sao Paulo) && Chile (Santiago) && Peru (Lima) && Argentina (Buenos Aires)"""
    def america_South(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['Brazil']['capacity']
            load_raw = result['datacenters']['Brazil']['load']
            capacity_secondary_raw = result['datacenters']['Chile']['capacity']
            load_secondary_raw = result['datacenters']['Chile']['load']
            capacity_tertiary_raw = result['datacenters']['Peru']['capacity']
            load_tertiary_raw = result['datacenters']['Peru']['load']
            capacity_quaternary_raw = result['datacenters']['Argentina']['capacity']
            load_quaternary_raw = result['datacenters']['Argentina']['load']
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
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
            capacity_raw = result['datacenters']['US Northcentral']['capacity']
            load_raw = result['datacenters']['US Northcentral']['load']
            capacity_secondary_raw = result['datacenters']['US Northeast']['capacity']
            load_secondary_raw = result['datacenters']['US Northeast']['load']
            capacity_tertiary_raw = result['datacenters']['US Northwest']['capacity']
            load_tertiary_raw = result['datacenters']['US Northwest']['load']
            capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

    """US Southwest (Los Angeles) && US Southeast (Atlanta)"""
    def usa_South(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['US Southwest']['capacity']
            load_raw = result['datacenters']['US Southwest']['load']
            capacity_secondary_raw = result['datacenters']['US Southeast']['capacity']
            load_secondary_raw = result['datacenters']['US Southeast']['load']
            capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

    #
    #   Europe
    #
    """EU West (Luxembourg) && Spain (Mardid)"""   
    def eu_West(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['EU West']['capacity']
            load_raw = result['datacenters']['EU West']['load']
            capacity_secondary_raw = result['datacenters']['Spain']['capacity']
            load_secondary_raw = result['datacenters']['Spain']['load']
            capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        
    """EU East (Vienna) && Poland (Warsaw)"""
    def eu_East(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['EU East']['capacity']
            load_raw = result['datacenters']['EU East']['load']
            capacity_secondary_raw = result['datacenters']['Poland']['capacity']
            load_secondary_raw = result['datacenters']['Poland']['load']
            capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
    
    """EU North (Stockholm)"""
    def eu_North(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['EU North']['capacity']
            load_raw = result['datacenters']['EU North']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

    #
    #    Asia   
    #
    """India (Mumbai) && India East (Chennai)"""
    def india(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['India']['capacity']
            load_raw = result['datacenters']['India']['load']
            capacity_secondary_raw = result['datacenters']['India East']['capacity']
            load_secondary_raw = result['datacenters']['India East']['load']
            capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
    
    """Japan (Tokyo)"""
    def japan(self):

        try:
            result = get_response()
            capacity_raw = result['datacenters']['Japan']['capacity']
            load_raw = result['datacenters']['Japan']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
            
    """Emirates (Dubai)"""
    def emirates(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['Emirates']['capacity']
            load_raw = result['datacenters']['Emirates']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru

    """China Shanghai && China Tianjin && China Guangzhou"""
    def china(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['China Shanghai']['capacity']
            load_raw = result['datacenters']['China Shanghai']['load']
            capacity_secondary_raw = result['datacenters']['China Tianjin']['capacity']
            load_secondary_raw = result['datacenters']['China Tianjin']['load']
            capacity_tertiary_raw = result['datacenters']['China Guangzhou']['capacity']
            load_tertiary_raw = result['datacenters']['China Guangzhou']['load']
            capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
   
    """Singapore"""
    def singapore(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['Singapore']['capacity']
            load_raw = result['datacenters']['Singapore']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
            
    """Hong Kong"""
    def hong_kong(self):
        try:
            result = get_response()
            capacity_raw = result['datacenters']['Hong Kong']['capacity']
            load_raw = result['datacenters']['Hong Kong']['load']
            capacity_secondary_raw = load_secondary_raw = capacity_tertiary_raw = load_tertiary_raw = capacity_quaternary_raw = load_quaternary_raw = 'N/A'
            capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru = translate_ru(capacity_raw, load_raw, capacity_secondary_raw, load_secondary_raw, capacity_tertiary_raw, load_tertiary_raw, capacity_quaternary_raw, load_quaternary_raw)
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru
        except:
            capacity = load = capacity_ru = load_ru = capacity_secondary = load_secondary = capacity_secondary_ru = load_secondary_ru = capacity_tertiary = load_tertiary = capacity_tertiary_ru = load_tertiary_ru = capacity_quaternary = load_quaternary = capacity_quaternary_ru = load_quaternary_ru = 'N/A'
            return capacity, load, capacity_ru, load_ru, capacity_secondary, load_secondary, capacity_secondary_ru, load_secondary_ru, capacity_tertiary, load_tertiary, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary, load_quaternary, capacity_quaternary_ru, load_quaternary_ru