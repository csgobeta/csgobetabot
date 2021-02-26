TESTBOT = '' # Telegram Test Bot API Key
CSGOBETABOT = '' # Telegram Bot API Key, more information: https://core.telegram.org/bots/api

TEST_MODE = False # Test mode

if TEST_MODE: 
    BOT_TOKEN = TESTBOT
else:
    BOT_TOKEN = CSGOBETABOT

OWNER = '' # Telegram Bot Owner ID
AQ = '' # Telegram Bot Owner ID

CSGOBETACHAT = '' # Telegram Chat ID
CSGOBETACHANNEL = '' # Telegram Channel ID

LOGCHANNEL = '' # Telegram Log Channel ID

STEAM_API_KEY = '' # from https://steamcommunity.com/dev/apikey
STEAM_USERNAME = ''
STEAM_PASS = ''

TWITTER_API_KEY = '' # https://developer.twitter.com/en/apply-for-access
TWITTER_API_KEY_S = ''
TWITTER_TOKEN = ''
TWITTER_TOKEN_S = ''

CSGO_APP_ID = '730'
CSGO_STEAM_PROFILE_ID = '76561198082857351'
CSGO_TWITTER_ID = '353780675'

CACHE_FILE_PATH = 'data/cache.json'
SS_CACHE_FILE_PATH = 'data/ss_cache.json'
GV_CACHE_FILE_PATH = 'data/gv_cache.json'
GUNS_CACHE_FILE_PATH = 'data/guns_db.json'

PLAYER_CHART_FILE_PATH = 'data/player_chart.csv'
DEV_CHART_FILE_PATH = 'data/dev_chart.csv'
GRAPH_IMG_FILE_PATH = 'data/graph.png'
GRAPH2_IMG_FILE_PATH = 'data/graph_devs.png'

USER_DB_FILE_PATH = 'data/user_db.csv'
USER_MESSAGE_FILE_PATH = 'data/msg.txt'
