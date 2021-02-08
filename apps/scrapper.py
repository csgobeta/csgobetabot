import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime 

from apps import file_manager
import config

url_st = 'https://store.steampowered.com/stats/'
url_cs = 'https://blog.counter-strike.net'
url_ss = 'https://crowbar.steamstat.us/gravity.json'
url_gv = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

class PeakOnline:
    def get_peak(self):
        try:
            soup = BeautifulSoup(requests.get(url_st, headers=headers).content, 'html.parser')
            string = soup.find(string="Counter-Strike: Global Offensive")
            tr = string.find_parent("tr")
            span = tr.find_all("span")
            peak24 = str(span[1]).replace('<span class="currentServers">', '').replace('</span>', '').replace(',', '')
            return int(peak24)
        except:
            peak24 = 000
            return peak24


class Monthly:
    def get_unique(self):
        try:
            soup = BeautifulSoup(requests.get(url_cs, headers=headers).content, 'html.parser')
            unique = soup.find("div", {"class": "monthly"}).string.replace(',', '')
            return int(unique)
        except:
            unique = 000
            return unique
        
class CSGOGameCoordinator:
    def get_status(self):
        try:
            soup = BeautifulSoup(requests.get(url_ss, headers=headers).content, 'html.parser')

            data = soup.get_text()

            f = open(config.SS_CACHE_FILE_PATH, 'r+')
            f.truncate(0)
            f.close()

            f = open(config.SS_CACHE_FILE_PATH, 'a')
            f.write(data)
            f.close()
            
            f = open(config.SS_CACHE_FILE_PATH,"r")  
            parsed = json.load(fin)
            f.close()

            items = file_manager.readJson(config.SS_CACHE_FILE_PATH)
            delta = items['services'][4]
            gc_status = delta[2]

            return gc_status
        except:
            gc_status = 'N/A'
            return gc_status

class GameVersion:
    def get_gameVer(self):
        try: 
            soup = BeautifulSoup(requests.get(url_gv, headers=headers).content, 'html.parser')

            data = soup.get_text()

            f = open(config.GV_CACHE_FILE_PATH, 'r+')
            f.truncate(0)
            f.close()

            f = open(config.GV_CACHE_FILE_PATH, 'a')
            f.write(data)
            f.close()

            options = {} 
            f = open(config.GV_CACHE_FILE_PATH)
            x = f.read()
            config_entries = re.split('\n|=', x)

            for key, value in zip(config_entries[0::2], config_entries[1::2]):
                cleaned_key = key.replace("[",'').replace("]",'')
                options[cleaned_key] = value

            options['ClientVersion'] = int(options['ClientVersion'])
            options['ServerVersion'] = int(options['ServerVersion'])
            options['appID'] = int(options['appID'])
            options['SourceRevision'] = int(options['SourceRevision'])

            line = json.dumps(options, indent=4)
            fout = open(config.GV_CACHE_FILE_PATH,"w")
            fout.write(line)
            fout.close()

            items = file_manager.readJson(config.GV_CACHE_FILE_PATH)
            client_version = items['ClientVersion']
            server_version = items['ServerVersion']
            patch_version = items['PatchVersion']
            dt = str(items['VersionDate']) + ' ' + str(items['VersionTime'])
            version_timestamp = datetime.strptime(dt, "%b %d %Y %H:%M:%S").timestamp()

            return client_version, server_version, patch_version, version_timestamp
        except:
            client_version = server_version = 000
            patch_version = version_timestamp = 'N/A'
            return client_version, server_version, patch_version, version_timestamp
