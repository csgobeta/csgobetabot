import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import seaborn as sns
import pandas as pd

from datetime import datetime
import time

import logging
from telegraph import upload_file

import config
from apps import file_manager

def graph_maker():
    while True:
        minutes = datetime.now().minute
        seconds = datetime.now().second
        microseconds = datetime.now().microsecond
        if minutes not in {0, 10, 20, 30, 40, 50}:
            snooze = ((10 - minutes%10) * 60) - (seconds + microseconds/1000000.0)
            time.sleep(snooze)
        else:
            try:
                cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)

                cache_key_list = []
                for keys, values in cacheFile.items():
                    cache_key_list.append(keys)

                player_count = cacheFile['online_player_count']
                dev_count = cacheFile['dev_player_count']

                old_player_data = pd.read_csv(config.PLAYER_CHART_FILE_PATH, parse_dates=['DateTime'])
                old_dev_data = pd.read_csv(config.DEV_CHART_FILE_PATH, parse_dates=['DateTime'])

                old_player_data.drop(0, axis=0, inplace=True)
                old_dev_data.drop(0, axis=0, inplace=True)

                temp_player_data = pd.DataFrame([[datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), player_count]], columns=['DateTime', 'Players'])
                temp_dev_data = pd.DataFrame([[datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), dev_count]], columns=['DateTime', 'Devs'])

                new_player_data = pd.concat([old_player_data, temp_player_data])
                new_dev_data = pd.concat([old_dev_data, temp_dev_data])

                new_player_data.to_csv(config.PLAYER_CHART_FILE_PATH, index=False)
                new_dev_data.to_csv(config.DEV_CHART_FILE_PATH, index=False)

                player_data = pd.read_csv(config.PLAYER_CHART_FILE_PATH, parse_dates=['DateTime'])
                dev_data = pd.read_csv(config.DEV_CHART_FILE_PATH, parse_dates=['DateTime'])

                sns.set_style('whitegrid')

                fig, ax = plt.subplots(figsize=(10, 2.5))
                ax.plot('DateTime', 'Players', data=player_data, color = 'red', linewidth = .7, marker='o', markevery=[-1])
                ax.fill_between(player_data['DateTime'], player_data['Players'], 0, facecolor = 'red', color = 'red', alpha = .4)

                ax.margins(x=0)
                ax.grid(b=True, axis='y', linestyle='--', alpha=.3)
                ax.grid(b=False, axis='x')
                ax.spines['bottom'].set_position('zero')
                ax.spines['bottom'].set_color('black')
                ax.set_ylabel('')
                ax.set_xlabel('')
                ax.xaxis.set_ticks_position('bottom') 
                ax.xaxis.set_major_locator(mdates.DayLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
                ax.legend(loc='upper left')
                ax.axhline(y=0, color='none')
                ax.axhline(y=1400000, color='none')

                plt.yticks(ticks=[0, 250000, 500000, 750000, 1000000, 1250000])
                plt.subplots_adjust(top=1, bottom=0.077, left=0, right=1)
                plt.text(0.989, 0.058, '0', transform=ax.transAxes, alpha=.3)
                plt.text(0.965, 0.215, '250k', transform=ax.transAxes, alpha=.3)
                plt.text(0.965, 0.377, '500k', transform=ax.transAxes, alpha=.3)
                plt.text(0.965, 0.54, '700k', transform=ax.transAxes, alpha=.3)
                plt.text(0.951, 0.705, '1 000k', transform=ax.transAxes, alpha=.3)
                plt.text(0.951, 0.865, '1 250k', transform=ax.transAxes, alpha=.3)
                plt.text(0.156, 0.874, 'Made by @csgobeta\nupd every 10 min', ha='center', transform=ax.transAxes, color = 'black', size = '6')
                plt.close()

                fig.savefig(config.GRAPH_IMG_FILE_PATH)
                url = upload_file(config.GRAPH_IMG_FILE_PATH)
                url = 'https://telegra.ph' + url[0]

                cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
                if cacheFile['graph_url'] != url:
                    file_manager.updateJson(config.CACHE_FILE_PATH, url, cache_key_list[22])

                
                fig2, ax = plt.subplots(figsize=(10, 2.5))
                ax.plot('DateTime', 'Devs', data=dev_data, color = 'red', linewidth = .7, marker='o', markevery=[-1])
                ax.fill_between(dev_data['DateTime'], dev_data['Devs'], 0, facecolor = 'red', color = 'red', alpha = .4)

                ax.margins(x=0)
                ax.grid(b=True, axis='y', linestyle='--', alpha=.3)
                ax.grid(b=False, axis='x')
                ax.spines['bottom'].set_position('zero')
                ax.spines['bottom'].set_color('black')
                ax.set_ylabel('')
                ax.set_xlabel('')
                ax.xaxis.set_ticks_position('bottom')
                ax.xaxis.set_major_locator(mdates.HourLocator(interval=7))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M %Z'))
                ax.legend(loc='upper left')
                ax.axhline(y=0, color='none')
                ax.axhline(y=6, color='none')

                plt.yticks(ticks=[0, 1, 2, 3, 4, 5])
                plt.subplots_adjust(top=1, bottom=0.077, left=0, right=1)
                plt.text(0.989, 0.059, '0', transform=ax.transAxes, alpha=.3)
                plt.text(0.989, 0.215, '1', transform=ax.transAxes, alpha=.3)
                plt.text(0.989, 0.368, '2', transform=ax.transAxes, alpha=.3)
                plt.text(0.989, 0.526, '3', transform=ax.transAxes, alpha=.3)
                plt.text(0.988, 0.670, '4', transform=ax.transAxes, alpha=.3)
                plt.text(0.989, 0.821, '5', transform=ax.transAxes, alpha=.3)
                plt.text(0.141, 0.874, 'Made by @csgobeta\nupd every 10 min', ha='center', transform=ax.transAxes, color = 'black', size = '6')
                plt.close()

                fig2.savefig(config.GRAPH2_IMG_FILE_PATH)
                url2 = upload_file(config.GRAPH2_IMG_FILE_PATH)
                url2 = 'https://telegra.ph' + url2[0]

                cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
                if cacheFile['graph_url2'] != url2:
                    file_manager.updateJson(config.CACHE_FILE_PATH, url2, cache_key_list[23])
                time.sleep(70)
            except Exception as e:
                print(f' - Error:\n{e}\n\n\n')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    graph_maker()