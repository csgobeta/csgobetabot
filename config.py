TESTBOT = '' # Test Telegram Bot API Key
CSGOBETABOT = '' # Telegram Bot API Key, more information: https://core.telegram.org/bots/api

TEST_MODE = False # Test mode

if TEST_MODE: 
    BOT_TOKEN = TESTBOT
else:
    BOT_TOKEN = CSGOBETABOT

KEY = '' # from https://steamcommunity.com/dev/apikey

OWNER = '' # Telegram Bot Owner ID
AQ = '' # Telegram Bot Owner ID

CSGOBETACHAT = '' # Telegram Chat ID
CSGOBETACHANNEL = '' # Telegram Channel ID

LOGCHANNEL = '' # Telegram Channel ID

STEAM_USERNAME = '' # Steam Username
STEAM_PASS = '' # Steam Password

CACHE_FILE_PATH = 'data/cache.json'
SS_CACHE_FILE_PATH = 'data/ss_cache.json'
GV_CACHE_FILE_PATH = 'data/gv_cache.json'
GUNS_CACHE_FILE_PATH = 'data/guns_db.json'
