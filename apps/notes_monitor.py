import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


import re
from bs4 import BeautifulSoup
import requests
import logging
import telebot
import time
import config
from apps import file_manager
from plugins import strings


blogpost_url = 'https://blog.counter-strike.net/index.php/'
patchnotes_url = 'https://blog.counter-strike.net/index.php/category/updates/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}


def notes_monitor():
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    currentVersion = cacheFile['client_version']

    soup_blog = BeautifulSoup(requests.get(
        blogpost_url, headers=headers).content, 'html.parser')
    currentBlogpost = soup_blog.find("div", {"id": "main_blog"})

    soup_notes = BeautifulSoup(requests.get(
        patchnotes_url, headers=headers).content, 'html.parser')
    currentPatchnotes = soup_notes.find("div", {"id": "main_blog"})

    while True:
        try:
            cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
            newVersion = cacheFile['client_version']

            if newVersion != currentVersion:
                while True:
                    try:
                        soup_notes = BeautifulSoup(requests.get(
                            patchnotes_url, headers=headers).content, 'html.parser')
                        newPatchnotes = soup_notes.find("div", {"id": "main_blog"})

                        if newPatchnotes != currentPatchnotes:
                            patch = cacheFile['patch_version']
                            data = newPatchnotes.find("div", {"class": "inner_post"})
                            textList = data.find_all('p')[1:]
                            url = data.find('a')['href']
                            textStr = '\n\n'.join(str(i) for i in textList)
                            cleantext = re.sub(r'<.*?>', '', textStr)
                            text = re.sub(r'–', '•', cleantext)
                            data = [text, patch, newVersion, url]
                            key = 'notes'
                            send_alert(data, key)
                            currentPatchnotes = newPatchnotes
                            currentVersion = newVersion
                            break

                        time.sleep(20)
                    except Exception as e:
                        print(f' - Error:\n{e}\n\n\n')

            soup_blog = BeautifulSoup(requests.get(
                blogpost_url, headers=headers).content, 'html.parser')
            newBlogpost = soup_blog.find("div", {"id": "main_blog"})

            if newBlogpost != currentBlogpost:
                data = newBlogpost.find("div", {"class": "inner_post"})
                title = data.find('h2').text
                textList = data.find_all('p')[1:]
                textStr = '\n\n'.join(str(i) for i in textList)
                text = re.sub(r'<.*?>', '', textStr)
                url = data.find('a')['href']
                currentBlogpost = newBlogpost
                data = [title, text, url]
                key = 'blog'
                send_alert(data, key)

            time.sleep(20)

        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(data, key):
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if key == 'notes':
        text = strings.dev_upd.format(data[1], data[2], data[0], data[3])
    else:
        text = 'NEW BLOGPOST:{}\n\n{}\n\n{}'.format(data[0], data[1], data[2])
    bot.send_message(
        config.CSGOBETA_DEV, text, disable_web_page_preview=True, parse_mode='html')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    notes_monitor()
