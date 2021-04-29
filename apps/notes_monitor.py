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
import subprocess
import config
from apps import file_manager
from plugins import strings


blogpost_url = 'https://blog.counter-strike.net/index.php/'
patchnotes_url = 'https://blog.counter-strike.net/index.php/category/updates/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
timeout = 180
timeout_start = time.time()


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
                steamcmd = str(subprocess.check_output(['steamcmd', '+login', config.STEAM_USERNAME, config.STEAM_PASS, '+app_status 730', '+quit']))
                regex = re.findall(r'downloaded: \d+/\d+', steamcmd)
                size = regex[0].split('/')
                patch = cacheFile['patch_version']
                key = 'notes'
                patchnotes = False
                while time.time() < timeout_start + timeout:
                    try:
                        soup_notes = BeautifulSoup(requests.get(
                            patchnotes_url, headers=headers).content, 'html.parser')
                        newPatchnotes = soup_notes.find("div", {"id": "main_blog"})

                        if newPatchnotes != currentPatchnotes:
                            patchnotes = True
                            data = newPatchnotes.find("div", {"class": "inner_post"})
                            textList = data.find_all('p')[1:]
                            textStr = '\n\n'.join(str(i) for i in textList)
                            cleantext = re.sub(r'<.*?>', '', textStr)
                            text = re.sub(r'–', '•', cleantext)
                            url = data.find('a')['href']
                            data = [text, patch, newVersion, url, size[1]]
                            send_alert(data, key)
                            currentPatchnotes = newPatchnotes
                            currentVersion = newVersion
                            break

                        time.sleep(20)
                    except Exception as e:
                        print(f' - Error:\n{e}\n\n\n')

                if not patchnotes:
                    text = 'no patchnotes found, pls check url below'
                    url = 'steamdb.info/patchnotes/{}'.format(cacheFile['public_build_ID'])
                    data = [text, patch, newVersion, url, size[1]]
                    send_alert(data, key)
                    currentVersion = newVersion

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
        text_en = strings.dev_upd_en.format(data[1], data[2], data[0], data[4], data[3])
        text_ru = strings.dev_upd_ru.format(data[1], data[2], data[0], data[4], data[3])
        bot.send_message(
            config.CSGOBETA_DEV, text_en, disable_web_page_preview=True, parse_mode='html')
        bot.send_message(
            config.CSGOBETA_DEV, text_ru, disable_web_page_preview=True, parse_mode='html')
    else:
        text = 'NEW BLOGPOST:{}\n\n{}\n\n{}'.format(data[0], data[1], data[2])
        bot.send_message(
            config.CSGOBETA_DEV, text, disable_web_page_preview=True, parse_mode='html')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    notes_monitor()
