import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import pandas as pd
import logging
from html_telegraph_poster import upload_image

from datetime import datetime
import time
import traceback

import config
from apps import file_manager

def graph_maker():
    while True:
        try:
            t = datetime.utcnow()
            sleeptime = 600 - (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime)
            
            data = pd.read_csv(config.GRAPH_CACHE_FILE_PATH, parse_dates=['DateTime'])
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            player_count = cacheFile['online_player_count']

            data.drop(0, axis=0, inplace=True)
            temp_data = pd.DataFrame([[datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), player_count]], columns=['DateTime', 'Players'])
            new_data = pd.concat([data, temp_data])

            new_data.to_csv(config.GRAPH_CACHE_FILE_PATH, index=False)

            data = pd.read_csv(config.GRAPH_CACHE_FILE_PATH, parse_dates=['DateTime'])

            sns.set_style('whitegrid')

            fig, ax = plt.subplots(figsize=(10, 2.5))
            ax.plot('DateTime', 'Players', data=data, color = 'red', linewidth = .7)
            ax.fill_between(data['DateTime'], data['Players'], 0, facecolor = 'red', color = 'red', alpha = .4)

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
            plt.text(0.969, 0.215, '250k', transform=ax.transAxes, alpha=.3)
            plt.text(0.968, 0.377, '500k', transform=ax.transAxes, alpha=.3)
            plt.text(0.968, 0.54, '700k', transform=ax.transAxes, alpha=.3)
            plt.text(0.956, 0.705, '1 000k', transform=ax.transAxes, alpha=.3)
            plt.text(0.956, 0.865, '1 250k', transform=ax.transAxes, alpha=.3)
            plt.text(0.11, 0.899, 'Made by @csgobeta', transform=ax.transAxes, color = 'black', size = '7')
            plt.close()

            fig.savefig(config.GRAPH_IMG_FILE_PATH)
            url = upload_image(config.GRAPH_IMG_FILE_PATH)

            with open('config.py') as file:
                filedata = file.read()
                filedata = filedata.replace(config.GRAPH_URL_PATH, url)
            with open('config.py', 'w') as file:
                file.write(filedata)

        except AttributeError:
            error_message = traceback.format_exc()
            now = str(datetime.now())
            print(f'{now} - Error:\n{error_message}\n\n\n')
            time.sleep(60)
            graph_maker()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(process)d %(message)s')
    graph_maker()