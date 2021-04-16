import requests
import config
from datetime import datetime


API_server_status = f'https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1?key={config.STEAM_API_KEY}'
API_csgo_players = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={config.CSGO_APP_ID}'
API_dev_players = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={config.CSGO_BETA_APP_ID}'


class ValveServersAPI:
    def get_status(self):
        try:
            response = requests.get(API_server_status)
            if response.status_code == 200:
                webapi_status = 'normal'
            elif response.status_code != 200 and datetime.today().weekday() == 1:
                webapi_status = 'maintenance'
            else:
                webapi_status = 'N/A'
            result = response.json()['result']

            timestamp = result['app']['timestamp']
            datacenters = result['datacenters']

            sessionsLogon = result['services']['SessionsLogon']
            steam_community = result['services']['SteamCommunity']

            matchmaking = result['matchmaking']
            scheduler = matchmaking['scheduler']
            online_servers = matchmaking['online_servers']
            active_players = matchmaking['online_players']
            searching_players = matchmaking['searching_players']
            search_seconds_avg = matchmaking['search_seconds_avg']

            return webapi_status, sessionsLogon, steam_community, scheduler, timestamp, online_servers, active_players, search_seconds_avg, searching_players, datacenters
        except:
            webapi_status = scheduler = sessionsLogon = steam_community = datacenters = 'N/A'
            timestamp = online_servers = active_players = search_seconds_avg = searching_players = 0
            return webapi_status, sessionsLogon, steam_community, scheduler, timestamp, online_servers, active_players, search_seconds_avg, searching_players, datacenters

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
