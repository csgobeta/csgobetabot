import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from plugins import strings
import config
import time
import re
import telebot
import logging
import feedparser


blogpost_url = 'https://blog.counter-strike.net/index.php/feed/'
patchnotes_url = 'https://blog.counter-strike.net/index.php/category/updates/feed/'


def feed_parser():
    currentBlogpost = feedparser.parse(blogpost_url).entries
    currentPatchnotes = feedparser.parse(patchnotes_url).entries
    while True:
        try:
            newBlogpost = feedparser.parse(blogpost_url).entries
            newPatchnotes = feedparser.parse(patchnotes_url).entries
            if newBlogpost != currentBlogpost:
                newPost = newBlogpost[0]
                currentBlogpost = newBlogpost
                key = 'post'
                send_alert(newPost, key)
            if newPatchnotes != currentPatchnotes:
                newNotes = newPatchnotes[0]
                currentPatchnotes = newPatchnotes
                key = 'notes'
                send_alert(newNotes, key)
            time.sleep(60)
        except Exception as e:
            print(f' - Error:\n{e}\n\n\n')


def send_alert(data, key):
    cleancontent = re.sub(r'<.*?>', '', data.content[0].value)
    cleancontent = re.sub(r'&#8211;', '•', cleancontent)
    if key == 'post':
        cleancontent = re.sub(r'\n', '\n\n', cleancontent)
    bot = telebot.TeleBot(config.BOT_TOKEN)
    if not config.TEST_MODE:
        chatID = config.CSGOBETA_DEV
    else:
        chatID = config.OWNER
    text = f'''<b>{data.title}</b>
(Author: {data.author})

{cleancontent}

{data.link}
'''
    bot.send_message(
        chatID, text, disable_web_page_preview=True, parse_mode='html')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    feed_parser()
