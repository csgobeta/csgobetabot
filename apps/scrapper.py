import requests
from bs4 import BeautifulSoup

import json
import re

from datetime import datetime

from apps import file_manager
import config

url_st = 'https://store.steampowered.com/stats/'
url_cs = 'https://blog.counter-strike.net'
url_gv = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}


class PeakOnline:
    def get_peak(self):
        try:
            soup = BeautifulSoup(requests.get(
                url_st, headers=headers).content, 'html.parser')
            string = soup.find(string="Counter-Strike: Global Offensive")
            tr = string.find_parent("tr")
            span = tr.find_all("span")
            peak24 = str(span[1]).replace('<span class="currentServers">', '').replace(
                '</span>', '').replace(',', '')
            return int(peak24)
        except:
            peak24 = 0
            return peak24


class Monthly:
    def get_unique(self):
        try:
            soup = BeautifulSoup(requests.get(
                url_cs, headers=headers).content, 'html.parser')
            unique = soup.find(
                "div", {"class": "monthly"}).string.replace(',', '')
            return int(unique)
        except:
            unique = 0
            return unique


class GameVersion:
    def get_gameVer(self):
        try:
            soup = BeautifulSoup(requests.get(
                url_gv, headers=headers).content, 'html.parser')

            data = soup.get_text()
            options = {}
            config_entries = re.split('\n|=', data)

            for key, value in zip(config_entries[0::2], config_entries[1::2]):
                cleaned_key = key.replace("[", '').replace("]", '')
                options[cleaned_key] = value

            dt = str(options['VersionDate']) + ' ' + \
                str(options['VersionTime'])
            client_version = int(options['ClientVersion'])
            server_version = int(options['ServerVersion'])
            patch_version = options['PatchVersion']
            version_timestamp = datetime.strptime(
                dt, "%b %d %Y %H:%M:%S").timestamp()

            return client_version, server_version, patch_version, version_timestamp
        except:
            client_version = server_version = version_timestamp = 0
            patch_version = 'N/A'
            return client_version, server_version, patch_version, version_timestamp
