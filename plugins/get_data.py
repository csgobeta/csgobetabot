import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import config
from plugins.addons import translate
from plugins.addons import time_converter
from plugins import strings
from apps import file_manager
from telegraph import Telegraph
import validators
import requests
import datetime
import time
import re
from steam.steamid import SteamID
from steam import steamid

def server_status():
    '''Get the status of CS:GO servers'''
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    gcCache = cacheFile['game_coordinator']
    slCache = cacheFile['sessionsLogon']
    sCache = cacheFile['scheduler']
    piCache = cacheFile['steam_community']
    wsCache = cacheFile['valve_webapi']

    array = [gcCache, slCache, sCache, piCache, wsCache]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    gcRCache, slRCache, sRCache, piRCache, wsRCache = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4]

    if gcCache != 'normal' or slCache != 'normal':
        tick = '❌'
    else:
        tick = '✅'

    status_text_en = strings.status_en.format(
        tick, gcCache, slCache, sCache, piCache, wsCache, tsCache)
    status_text_ru = strings.status_ru.format(
        tick, gcRCache, slRCache, sRCache, piRCache, wsRCache, tsRCache)

    return status_text_en, status_text_ru


def mm_stats():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url']
    pcCache, scCache = cacheFile['online_player_count'], cacheFile['online_server_count']
    apCache, ssCache, spCache = cacheFile['active_player_count'], cacheFile[
        'search_seconds_avg'], cacheFile['searching_players']
    p24Cache, paCache, uqCache = cacheFile['peak_24_hours'], cacheFile['peak_all_time'], cacheFile['unique_monthly']

    mm_text_en = strings.mm_en.format(
        url, scCache, pcCache, apCache, spCache, ssCache)
    mm_text_ru = strings.mm_ru.format(
        url, scCache, pcCache, apCache, spCache, ssCache)

    addInf_text_en = strings.additionalInfo_en.format(
        p24Cache, paCache, uqCache, tsCache)
    addInf_text_ru = strings.additionalInfo_ru.format(
        p24Cache, paCache, uqCache, tsRCache)

    mm_stats_text_en = mm_text_en + '\n\n' + addInf_text_en
    mm_stats_text_ru = mm_text_ru + '\n\n' + addInf_text_ru

    return mm_stats_text_en, mm_stats_text_ru


def devcount():
    '''Get the count of online devs'''
    tsCache, tsRCache, tsVCache, tsVRCache = time_converter()[0], time_converter()[
        1], time_converter()[4], time_converter()[5]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    url = cacheFile['graph_url2']
    dcCache, dpCache = cacheFile['dev_player_count'], cacheFile['dev_all_time_peak']
    devcount_text_en = strings.devCount_en.format(
        url, dcCache, dpCache, tsCache, tsVCache)
    devcount_text_ru = strings.devCount_ru.format(
        url, dcCache, dpCache, tsRCache, tsVRCache)
    return devcount_text_en, devcount_text_ru


def timer():
    '''Get drop cap reset time'''
    wanted_day = 'wednesday'
    wanted_time = 00

    list = [['monday', 0], ['tuesday', 1], ['wednesday', 2], [
        'thursday', 3], ['friday', 4], ['saturday', 5], ['sunday', 6]]

    for i in list:
        if wanted_day == i[0]:
            number_wanted_day = i[1]

    today = datetime.datetime.today().weekday()  # delivers the actual day
    # describes how many days are left until the wanted day
    delta_days = number_wanted_day - today
    actual_time = time.localtime(time.time())  # delivers the actual time

    if wanted_time > actual_time[3]:
        delta_hours = wanted_time - actual_time[3]
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]
    else:
        delta_days = delta_days - 1
        delta_hours = 23 - actual_time[3] + wanted_time
        delta_mins = 59 - actual_time[4]
        delta_secs = 59 - actual_time[5]

    if delta_days < 0:
        delta_days = delta_days + 7
    timer_text_en = strings.timer_en.format(
        delta_days, delta_hours, delta_mins, delta_secs)
    timer_text_ru = strings.timer_ru.format(
        delta_days, delta_hours, delta_mins, delta_secs)
    return timer_text_en, timer_text_ru


def gameversion():
    '''Get the version of the game'''
    vdCache, vdRCache = time_converter()[2], time_converter()[3]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    cvCache, svCache, pvCache = cacheFile['client_version'], cacheFile['server_version'], cacheFile['patch_version']
    gameversion_text_en = strings.gameversion_en.format(
        pvCache, cvCache, svCache, vdCache)
    gameversion_text_ru = strings.gameversion_ru.format(
        pvCache, cvCache, svCache, vdRCache)
    return gameversion_text_en, gameversion_text_ru


def gun_info(gun_id):
    '''Get archived data about guns'''
    cacheFile = file_manager.readJson(config.GUNS_CACHE_FILE_PATH)
    raw_data = list(filter(lambda x: x['id'] == gun_id, cacheFile['data']))
    data = raw_data[0]
    key_list = []
    value_list = []
    for key, value in data.items():
        key_list.append(key)
        value_list.append(value)
    name, price = value_list[1], value_list[2]
    origin, origin_ru = value_list[3], ''
    clip_size, reserve_ammo = value_list[4], value_list[5]
    fire_rate, kill_reward, movement_speed = value_list[6], value_list[10], value_list[8]
    armor_penetration, accurate_range_stand, accurate_range_crouch = value_list[
        9], value_list[11], value_list[12]
    draw_time, reload_clip_ready, reload_fire_ready = value_list[
        13], value_list[14], value_list[15]
    origin_list_ru = ['Германия', 'Австрия', 'Италия', 'Швейцария', 'Чехия', 'Бельгия', 'Швеция', 'Израль',
                      'Соединённые Штаты', 'Россия', 'Франция', 'Соединённое Королевство', 'Южная Африка']
    origin_list_en = ['Germany', 'Austria', 'Italy', 'Switzerland', 'Czech Republic', 'Belgium', 'Sweden', 'Israel',
                      'United States', 'Russia', 'France', 'United Kingdom', 'South Africa']
    unarmored_damage_head, unarmored_damage_chest_and_arm, unarmored_damage_stomach, unarmored_damage_leg = value_list[
        16], value_list[17], value_list[18], value_list[19]
    armored_damage_head, armored_damage_chest_and_arm, armored_damage_stomach, armored_damage_leg = value_list[
        20], value_list[21], value_list[22], value_list[23]
    for en, ru in zip(origin_list_en, origin_list_ru):
        if origin in en:
            origin_ru = ru
    gun_data_text_en = strings.gun_data_en.format(name, origin, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                                  armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                                  armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                                  armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    gun_data_text_ru = strings.gun_data_ru.format(name, origin_ru, price, clip_size, reserve_ammo, fire_rate, kill_reward, movement_speed,
                                                  armor_penetration, accurate_range_stand, accurate_range_crouch, draw_time, reload_clip_ready, reload_fire_ready,
                                                  armored_damage_head, unarmored_damage_head, armored_damage_chest_and_arm, unarmored_damage_chest_and_arm,
                                                  armored_damage_stomach, unarmored_damage_stomach, armored_damage_leg, unarmored_damage_leg)
    return gun_data_text_en, gun_data_text_ru


def url_checker(data):
    if data.startswith('steamcommunity'):
        data = 'https://' + data
    elif validators.url(data):
        pass
    elif data.isdigit() and len(data) == 17:
        data = f'https://steamcommunity.com/profiles/{data}'
    else:
        data = f'https://steamcommunity.com/id/{data}'
    return data


def ban_info(data):
    try:
        steam64 = steamid.from_url(url_checker(data))

        bans = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1?key={config.STEAM_API_KEY}&steamids={steam64}'
        vanity = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_API_KEY}&steamids={steam64}'
        faceitAPI = f'https://api.faceit.com/search/v2/players?query={steam64}'

        vanityURL = requests.get(vanity).json(
        )['response']['players'][0]['profileurl'].split('/')[-2]
        steamID = SteamID(steam64).as_64
        if vanityURL == str(steamID):
            vanityURL = 'not set'
            vanityURLR = 'не указана'
        else:
            vanityURLR = vanityURL
        accountID = SteamID(steam64).id
        steam2ID = SteamID(steam64).as_steam2
        steam3ID = SteamID(steam64).as_steam3
        inviteUrl = SteamID(steam64).invite_url
        csgoCode = SteamID(steam64).as_csgo_friend_code
        responseFaceit = requests.get(faceitAPI).json()['payload']['results']
        nicknames = [y for i in responseFaceit for x,
                     y in i.items() if x == 'nickname']
        faceitBans = [y for i in responseFaceit for x,
                      y in i.items() if x == 'status']
        faceitURLS = '\n'.join(
            'https://www.faceit.com/en/players/{}'.format(x) for x in nicknames)
        if len(faceitURLS) == 0:
            faceitURLS = '<code>not found</code>'
        if 'banned' in faceitBans:
            faceitBan = 'banned'
            faceitBanR = 'забанен'
        else:
            faceitBan = 'none'
            faceitBanR = 'нет'

        banData = requests.get(bans).json()['players'][0]
        if banData['VACBanned']:
            vacBan = str(banData['NumberOfVACBans']) + \
                ' (days since last ban: ' + \
                str(banData['DaysSinceLastBan']) + ')'
            vacBanR = str(banData['NumberOfVACBans']) + \
                ' (дней с момента последнего бана: ' + \
                str(banData['DaysSinceLastBan']) + ')'
        else:
            vacBan = 0
            vacBanR = 0
        gameBans = banData['NumberOfGameBans']
        if banData['CommunityBanned']:
            communityBan = 'banned'
            communityBanR = 'забанен'
        else:
            communityBan = 'none'
            communityBanR = 'нет'
        if banData['EconomyBan'] == 'banned':
            tradeBanR = 'забанен'
        else:
            tradeBan = 'none'
            tradeBanR = 'нет'

        bans_text_en = strings.bans_en.format(vanityURL, steamID, accountID, steam2ID, steam3ID, inviteUrl,
                                              csgoCode, faceitURLS, gameBans, vacBan, communityBan, tradeBan, faceitBan)
        bans_text_ru = strings.bans_ru.format(vanityURLR, steamID, accountID, steam2ID, steam3ID, inviteUrl,
                                              csgoCode, faceitURLS, gameBans, vacBanR, communityBanR, tradeBanR, faceitBanR)
        return bans_text_en, bans_text_ru
    except Exception as e:
        print('\n\nError:' + str(e) + '\n\n')
        bans_text_en, bans_text_ru = '⚠️ Invalid request.', '⚠️ Неверный запрос.'
        return bans_text_en, bans_text_ru


def csgo_stats(data):
    try:
        steam64 = steamid.from_url(url_checker(data))
        statsURL = f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={config.CSGO_APP_ID}&key={config.STEAM_API_KEY}&steamid={steam64}'
        response = requests.get(statsURL)
        if response.status_code == 500:
            url_en = '''<a href="https://i.imgur.com/CAjblvT.mp4">‎‎‎‎‎‎‎‎‎‎‎‎</a>❕ This account is private, statistics are not available. Please, change your privacy settings.'''
            url_ru = '''<a href="https://i.imgur.com/CAjblvT.mp4">‎‎‎‎‎‎‎‎‎‎‎‎‎‎</a>❕ Этот аккаунт приватный, невозможно получить статистику. Пожалуйста, поменяйте настройки приватности.'''
        else:
            data = response.json()['playerstats']['stats']
            try:
                totalPlayedTime = int("{:.0f}".format(list(
                    filter(lambda x: x['name'] == 'total_time_played', data))[0]['value'] / 3600))
            except:
                totalPlayedTime = 0
            try:
                totalKills = int(
                    list(filter(lambda x: x['name'] == 'total_kills', data))[0]['value'])
            except:
                totalKills = 0
            try:
                totalDeaths = int(
                    list(filter(lambda x: x['name'] == 'total_deaths', data))[0]['value'])
            except:
                totalDeaths = 0
            if totalKills != 0 and totalDeaths != 0:
                kdRatio = "{:.2f}".format(totalKills / totalDeaths)
            else:
                kdRatio = 0
            try:
                totalRoundsPlayed = int(
                    list(filter(lambda x: x['name'] == 'total_rounds_played', data))[0]['value'])
            except:
                totalRoundsPlayed = 0
            try:
                totalMatchesPlayed = int(
                    list(filter(lambda x: x['name'] == 'total_matches_played', data))[0]['value'])
            except:
                totalMatchesPlayed = 0
            try:
                totalMatchesWon = int(
                    list(filter(lambda x: x['name'] == 'total_matches_won', data))[0]['value'])
            except:
                totalMatchesWon = 0
            try:
                totalPistolRoundsWon = int(
                    list(filter(lambda x: x['name'] == 'total_wins_pistolround', data))[0]['value'])
            except:
                totalPistolRoundsWon = 0
            if totalMatchesPlayed != 0 and totalMatchesWon != 0:
                matchWinPercentage = "{:.2f}".format(
                    totalMatchesWon / totalMatchesPlayed * 100)
            else:
                matchWinPercentage = 0

            try:
                totalShots = int(
                    list(filter(lambda x: x['name'] == 'total_shots_fired', data))[0]['value'])
            except:
                totalShots = 0
            try:
                totalHits = int(
                    list(filter(lambda x: x['name'] == 'total_shots_hit', data))[0]['value'])
            except:
                totalHits = 0
            if totalHits != 0 and totalShots != 0:
                hitAccuracy = "{:.2f}".format(totalHits / totalShots * 100)
            else:
                hitAccuracy = 0

            map_wins_list = [i for i in data if re.match(
                r'total_wins_map_+', i['name'])]
            round_wins_list = [i for i in data if re.match(
                r'total_rounds_map_+', i['name'])]

            temp_map_name = list(filter(lambda x: x['value'] == max(
                i['value'] for i in map_wins_list), data))[0]['name'].split('_')[-1]
            temp_map_data = [x for x in map_wins_list if x['value'] == max(
                i['value'] for i in map_wins_list)]
            temp_round_data = [
                x for x in round_wins_list if x['name'].endswith(temp_map_name)]
            bestMapWins = temp_map_data[0]['value']
            bestMapRounds = temp_round_data[0]['value']

            bestMapPercentage = "{:.2f}".format(
                bestMapWins / bestMapRounds * 100)
            mapName = temp_map_name.capitalize()

            try:
                totalKillsHS = list(
                    filter(lambda x: x['name'] == 'total_kills_headshot', data))[0]['value']
            except:
                totalKillsHS = 0
            if totalKillsHS != 0 and totalKills != 0:
                hsAccuracy = "{:.2f}".format(totalKillsHS / totalKills * 100)
            else:
                hsAccuracy = 0

            try:
                totalDamageDone = list(
                    filter(lambda x: x['name'] == 'total_damage_done', data))[0]['value']
            except:
                totalDamageDone = 0
            try:
                totalWeaponDonated = list(
                    filter(lambda x: x['name'] == 'total_weapons_donated', data))[0]['value']
            except:
                totalWeaponDonated = 0
            try:
                totalBrokenWindows = list(
                    filter(lambda x: x['name'] == 'total_broken_windows', data))[0]['value']
            except:
                totalBrokenWindows = 0
            try:
                totalBombsPlanted = list(
                    filter(lambda x: x['name'] == 'total_planted_bombs', data))[0]['value']
            except:
                totalBombsPlanted = 0
            try:
                totalMVPs = list(filter(lambda x: x['name'] == 'total_mvps', data))[
                    0]['value']
            except:
                totalMVPs = 0
            try:
                totalBombsDefused = list(
                    filter(lambda x: x['name'] == 'total_defused_bombs', data))[0]['value']
            except:
                totalBombsDefused = 0
            try:
                totalMoneyEarned = list(
                    filter(lambda x: x['name'] == 'total_money_earned', data))[0]['value']
            except:
                totalMoneyEarned = 0
            try:
                totalHostagesResc = list(
                    filter(lambda x: x['name'] == 'total_rescued_hostages', data))[0]['value']
            except:
                totalHostagesResc = 0

            try:
                totalKnifeKills = list(
                    filter(lambda x: x['name'] == 'total_kills_knife', data))[0]['value']
            except:
                totalKnifeKills = 0
            try:
                totalKnifeDuelsWon = list(
                    filter(lambda x: x['name'] == 'total_kills_knife_fight', data))[0]['value']
            except:
                totalKnifeDuelsWon = 0
            try:
                totalKillsEnemyWeapon = list(
                    filter(lambda x: x['name'] == 'total_kills_enemy_weapon', data))[0]['value']
            except:
                totalKillsEnemyWeapon = 0
            try:
                totalKillsEnemyBlinded = list(
                    filter(lambda x: x['name'] == 'total_kills_enemy_blinded', data))[0]['value']
            except:
                totalKillsEnemyBlinded = 0
            try:
                totalKillsZoomedEnemy = list(filter(
                    lambda x: x['name'] == 'total_kills_against_zoomed_sniper', data))[0]['value']
            except:
                totalKillsZoomedEnemy = 0
            try:
                totalHEKills = list(
                    filter(lambda x: x['name'] == 'total_kills_hegrenade', data))[0]['value']
            except:
                totalHEKills = 0
            try:
                totalMolotovKills = list(
                    filter(lambda x: x['name'] == 'total_kills_molotov', data))[0]['value']
            except:
                totalMolotovKills = 0
            try:
                totalZeusShots = list(
                    filter(lambda x: x['name'] == 'total_shots_taser', data))[0]['value']
            except:
                totalZeusShots = 0
            try:
                totalZeusKills = list(
                    filter(lambda x: x['name'] == 'total_kills_taser', data))[0]['value']
            except:
                totalZeusKills = 0
            if totalZeusKills != 0 and totalZeusShots != 0:
                ZeusAccuracy = "{:.2f}".format(
                    totalZeusKills / totalZeusShots * 100)
            else:
                ZeusAccuracy = 0

            try:
                totalAk47Kills = list(filter(lambda x: x['name'] == 'total_kills_ak47', data))[
                    0]['value']
            except:
                totalAk47Kills = 0
            try:
                totalAk47Shots = list(filter(lambda x: x['name'] == 'total_shots_ak47', data))[
                    0]['value']
            except:
                totalAk47Shots = 0
            try:
                totalAk47Hits = list(filter(lambda x: x['name'] == 'total_hits_ak47', data))[
                    0]['value']
            except:
                totalAk47Hits = 0
            if totalAk47Hits != 0 and totalAk47Shots != 0:
                Ak47Accuracy = "{:.2f}".format(
                    totalAk47Hits / totalAk47Shots * 100)
            else:
                Ak47Accuracy = 0

            try:
                totalM4Kills = list(filter(lambda x: x['name'] == 'total_kills_m4a1', data))[
                    0]['value']
            except:
                totalM4Kills = 0
            try:
                totalM4Shots = list(filter(lambda x: x['name'] == 'total_shots_m4a1', data))[
                    0]['value']
            except:
                totalM4Shots = 0
            try:
                totalM4Hits = list(filter(lambda x: x['name'] == 'total_hits_m4a1', data))[
                    0]['value']
            except:
                totalM4Hits = 0

            if totalM4Hits != 0 and totalM4Shots != 0:
                m4Accuracy = "{:.2f}".format(totalM4Hits / totalM4Shots * 100)
            else:
                m4Accuracy = 0

            try:
                totalAWPKills = list(filter(lambda x: x['name'] == 'total_kills_awp', data))[
                    0]['value']
            except:
                totalAWPKills = 0
            try:
                totalAWPShots = list(filter(lambda x: x['name'] == 'total_shots_awp', data))[
                    0]['value']
            except:
                totalAWPShots = 0
            try:
                totalAWPHits = list(filter(lambda x: x['name'] == 'total_hits_awp', data))[
                    0]['value']
            except:
                totalAWPHits = 0
            if totalAWPHits != 0 and totalAWPShots != 0:
                AWPAccuracy = "{:.2f}".format(
                    totalAWPHits / totalAWPShots * 100)
            else:
                AWPAccuracy = 0

            try:
                totalGlockKills = list(
                    filter(lambda x: x['name'] == 'total_kills_glock', data))[0]['value']
            except:
                totalGlockKills = 0
            try:
                totalGlockShots = list(
                    filter(lambda x: x['name'] == 'total_shots_glock', data))[0]['value']
            except:
                totalGlockShots = 0
            try:
                totalGlockHits = list(filter(lambda x: x['name'] == 'total_hits_glock', data))[
                    0]['value']
            except:
                totalGlockHits = 0
            if totalGlockHits != 0 and totalGlockShots != 0:
                GlockAccuracy = "{:.2f}".format(
                    totalGlockHits / totalGlockShots * 100)
            else:
                GlockAccuracy = 0

            try:
                totalUSPKills = list(
                    filter(lambda x: x['name'] == 'total_kills_hkp2000', data))[0]['value']
            except:
                totalUSPKills = 0
            try:
                totalUSPShots = list(
                    filter(lambda x: x['name'] == 'total_shots_hkp2000', data))[0]['value']
            except:
                totalUSPShots = 0
            try:
                totalUSPHits = list(filter(lambda x: x['name'] == 'total_hits_hkp2000', data))[
                    0]['value']
            except:
                totalUSPHits = 0
            if totalUSPHits != 0 and totalUSPShots != 0:
                USPAccuracy = "{:.2f}".format(
                    totalUSPHits / totalUSPShots * 100)
            else:
                USPAccuracy = 0

            try:
                totalP250Kills = list(filter(lambda x: x['name'] == 'total_kills_p250', data))[
                    0]['value']
            except:
                totalP250Kills = 0
            try:
                totalP250Shots = list(filter(lambda x: x['name'] == 'total_shots_p250', data))[
                    0]['value']
            except:
                totalP250Shots = 0
            try:
                totalP250Hits = list(filter(lambda x: x['name'] == 'total_hits_p250', data))[
                    0]['value']
            except:
                totalP250Hits = 0
            if totalP250Hits != 0 and totalP250Shots != 0:
                P250Accuracy = "{:.2f}".format(
                    totalP250Hits / totalP250Shots * 100)
            else:
                P250Accuracy = 0

            try:
                totalDualiesKills = list(
                    filter(lambda x: x['name'] == 'total_kills_elite', data))[0]['value']
            except:
                totalDualiesKills = 0
            try:
                totalDualiesShots = list(
                    filter(lambda x: x['name'] == 'total_shots_elite', data))[0]['value']
            except:
                totalDualiesShots = 0
            try:
                totalDualiesHits = list(
                    filter(lambda x: x['name'] == 'total_hits_elite', data))[0]['value']
            except:
                totalDualiesHits = 0
            if totalDualiesHits != 0 and totalDualiesShots != 0:
                DualiesAccuracy = "{:.2f}".format(
                    totalDualiesHits / totalDualiesShots * 100)
            else:
                DualiesAccuracy = 0

            try:
                totalFiveSevenKills = list(
                    filter(lambda x: x['name'] == 'total_kills_fiveseven', data))[0]['value']
            except:
                totalFiveSevenKills = 0
            try:
                totalFiveSevenShots = list(
                    filter(lambda x: x['name'] == 'total_shots_fiveseven', data))[0]['value']
            except:
                totalFiveSevenShots = 0
            try:
                totalFiveSevenHits = list(
                    filter(lambda x: x['name'] == 'total_hits_fiveseven', data))[0]['value']
            except:
                totalFiveSevenHits = 0
            if totalFiveSevenHits != 0 and totalFiveSevenShots != 0:
                FiveSevenAccuracy = "{:.2f}".format(
                    totalFiveSevenHits / totalFiveSevenShots * 100)
            else:
                FiveSevenAccuracy = 0

            try:
                totalTec9Kills = list(filter(lambda x: x['name'] == 'total_kills_tec9', data))[
                    0]['value']
            except:
                totalTec9Kills = 0
            try:
                totalTec9Shots = list(filter(lambda x: x['name'] == 'total_shots_tec9', data))[
                    0]['value']
            except:
                totalTec9Shots = 0
            try:
                totalTec9Hits = list(filter(lambda x: x['name'] == 'total_hits_tec9', data))[
                    0]['value']
            except:
                totalTec9Hits = 0
            if totalTec9Hits != 0 and totalTec9Shots != 0:
                Tec9Accuracy = "{:.2f}".format(
                    totalTec9Hits / totalTec9Shots * 100)
            else:
                Tec9Accuracy = 0

            try:
                totalDeagleKills = list(
                    filter(lambda x: x['name'] == 'total_kills_deagle', data))[0]['value']
            except:
                totalDeagleKills = 0
            try:
                totalDeagleShots = list(
                    filter(lambda x: x['name'] == 'total_shots_deagle', data))[0]['value']
            except:
                totalDeagleShots = 0
            try:
                totalDeagleHits = list(
                    filter(lambda x: x['name'] == 'total_hits_deagle', data))[0]['value']
            except:
                totalDeagleHits = 0
            if totalDeagleHits != 0 and totalDeagleShots != 0:
                DeagleAccuracy = "{:.2f}".format(
                    totalDeagleHits / totalDeagleShots * 100)
            else:
                DeagleAccuracy = 0

            try:
                totalMac10Kills = list(
                    filter(lambda x: x['name'] == 'total_kills_mac10', data))[0]['value']
            except:
                totalMac10Kills = 0
            try:
                totalMac10Shots = list(
                    filter(lambda x: x['name'] == 'total_shots_mac10', data))[0]['value']
            except:
                totalMac10Shots = 0
            try:
                totalMac10Hits = list(filter(lambda x: x['name'] == 'total_hits_mac10', data))[
                    0]['value']
            except:
                totalMac10Hits = 0
            if totalMac10Hits != 0 and totalMac10Shots != 0:
                Mac10Accuracy = "{:.2f}".format(
                    totalMac10Hits / totalMac10Shots * 100)
            else:
                Mac10Accuracy = 0

            try:
                totalMp7Kills = list(filter(lambda x: x['name'] == 'total_kills_ump45', data))[
                    0]['value']
            except:
                totalMp7Kills = 0
            try:
                totalMp7Shots = list(filter(lambda x: x['name'] == 'total_shots_ump45', data))[
                    0]['value']
            except:
                totalMp7Shots = 0
            try:
                totalMp7Hits = list(filter(lambda x: x['name'] == 'total_hits_ump45', data))[
                    0]['value']
            except:
                totalMp7Hits = 0
            if totalMp7Hits != 0 and totalMp7Shots != 0:
                Mp7Accuracy = "{:.2f}".format(
                    totalMp7Hits / totalMp7Shots * 100)
            else:
                Mp7Accuracy = 0

            try:
                totalMp9Kills = list(filter(lambda x: x['name'] == 'total_kills_mp9', data))[
                    0]['value']
            except:
                totalMp9Kills = 0
            try:
                totalMp9Shots = list(filter(lambda x: x['name'] == 'total_shots_mp9', data))[
                    0]['value']
            except:
                totalMp9Shots = 0
            try:
                totalMp9Hits = list(filter(lambda x: x['name'] == 'total_hits_mp9', data))[
                    0]['value']
            except:
                totalMp9Hits = 0
            if totalMp9Hits != 0 and totalMp9Shots != 0:
                Mp9Accuracy = "{:.2f}".format(
                    totalMp9Hits / totalMp9Shots * 100)
            else:
                Mp9Accuracy = 0

            try:
                totalUMPKills = list(filter(lambda x: x['name'] == 'total_kills_ump45', data))[
                    0]['value']
            except:
                totalUMPKills = 0
            try:
                totalUMPShots = list(filter(lambda x: x['name'] == 'total_shots_ump45', data))[
                    0]['value']
            except:
                totalUMPShots = 0
            try:
                totalUMPHits = list(filter(lambda x: x['name'] == 'total_hits_ump45', data))[
                    0]['value']
            except:
                totalUMPHits = 0
            if totalUMPHits != 0 and totalUMPShots != 0:
                UMPAccuracy = "{:.2f}".format(
                    totalUMPHits / totalUMPShots * 100)
            else:
                UMPAccuracy = 0

            try:
                totalBizonKills = list(
                    filter(lambda x: x['name'] == 'total_kills_bizon', data))[0]['value']
            except:
                totalBizonKills = 0
            try:
                totalBizonShots = list(
                    filter(lambda x: x['name'] == 'total_shots_bizon', data))[0]['value']
            except:
                totalBizonShots = 0
            try:
                totalBizonHits = list(filter(lambda x: x['name'] == 'total_hits_bizon', data))[
                    0]['value']
            except:
                totalBizonHits = 0
            if totalBizonHits != 0 and totalBizonShots != 0:
                BizonAccuracy = "{:.2f}".format(
                    totalBizonHits / totalBizonShots * 100)
            else:
                BizonAccuracy = 0

            try:
                totalP90Kills = list(filter(lambda x: x['name'] == 'total_kills_p90', data))[
                    0]['value']
            except:
                totalP90Kills = 0
            try:
                totalP90Shots = list(filter(lambda x: x['name'] == 'total_shots_p90', data))[
                    0]['value']
            except:
                totalP90Shots = 0
            try:
                totalP90Hits = list(filter(lambda x: x['name'] == 'total_hits_p90', data))[
                    0]['value']
            except:
                totalP90Hits = 0
            if totalP90Hits != 0 and totalP90Shots != 0:
                P90Accuracy = "{:.2f}".format(
                    totalP90Hits / totalP90Shots * 100)
            else:
                FamasAccuracy = 0

            try:
                totalFamasKills = list(
                    filter(lambda x: x['name'] == 'total_kills_famas', data))[0]['value']
            except:
                totalFamasKills = 0
            try:
                totalFamasShots = list(
                    filter(lambda x: x['name'] == 'total_shots_famas', data))[0]['value']
            except:
                totalFamasShots = 0
            try:
                totalFamasHits = list(filter(lambda x: x['name'] == 'total_hits_famas', data))[
                    0]['value']
            except:
                totalFamasHits = 0
            if totalFamasHits != 0 and totalFamasShots != 0:
                FamasAccuracy = "{:.2f}".format(
                    totalFamasHits / totalFamasShots * 100)
            else:
                FamasAccuracy = 0

            try:
                totalGalilKills = list(
                    filter(lambda x: x['name'] == 'total_kills_galilar', data))[0]['value']
            except:
                totalGalilKills = 0
            try:
                totalGalilShots = list(
                    filter(lambda x: x['name'] == 'total_shots_galilar', data))[0]['value']
            except:
                totalGalilShots = 0
            try:
                totalGalilHits = list(
                    filter(lambda x: x['name'] == 'total_hits_galilar', data))[0]['value']
            except:
                totalGalilHits = 0
            if totalGalilHits != 0 and totalGalilShots != 0:
                GalilAccuracy = "{:.2f}".format(
                    totalGalilHits / totalGalilShots * 100)
            else:
                GalilAccuracy = 0

            try:
                totalAugKills = list(filter(lambda x: x['name'] == 'total_kills_aug', data))[
                    0]['value']
            except:
                totalAugKills = 0
            try:
                totalAugShots = list(filter(lambda x: x['name'] == 'total_shots_aug', data))[
                    0]['value']
            except:
                totalAugShots = 0
            try:
                totalAugHits = list(filter(lambda x: x['name'] == 'total_hits_aug', data))[
                    0]['value']
            except:
                totalAugHits = 0
            if totalAugHits != 0 and totalAugShots != 0:
                AugAccuracy = "{:.2f}".format(
                    totalAugHits / totalAugShots * 100)
            else:
                AugAccuracy = 0

            try:
                totalSgKills = list(filter(lambda x: x['name'] == 'total_kills_sg556', data))[
                    0]['value']
            except:
                totalSgKills = 0
            try:
                totalSgShots = list(filter(lambda x: x['name'] == 'total_shots_sg556', data))[
                    0]['value']
            except:
                totalSgShots = 0
            try:
                totalSgHits = list(filter(lambda x: x['name'] == 'total_hits_sg556', data))[
                    0]['value']
            except:
                totalSgHits = 0
            if totalSgHits != 0 and totalSgShots != 0:
                SgAccuracy = "{:.2f}".format(totalSgHits / totalSgShots * 100)
            else:
                SgAccuracy = 0

            try:
                totalSsgKills = list(filter(lambda x: x['name'] == 'total_kills_ssg08', data))[
                    0]['value']
            except:
                totalSsgKills = 0
            try:
                totalSsgShots = list(filter(lambda x: x['name'] == 'total_shots_ssg08', data))[
                    0]['value']
            except:
                totalSsgShots = 0
            try:
                totalSsgHits = list(filter(lambda x: x['name'] == 'total_hits_ssg08', data))[
                    0]['value']
            except:
                totalSsgHits = 0
            if totalSsgHits != 0 and totalSsgShots != 0:
                SsgAccuracy = "{:.2f}".format(
                    totalSsgHits / totalSsgShots * 100)
            else:
                SsgAccuracy = 0

            try:
                totalScarKills = list(
                    filter(lambda x: x['name'] == 'total_kills_scar20', data))[0]['value']
            except:
                totalScarKills = 0
            try:
                totalScarShots = list(
                    filter(lambda x: x['name'] == 'total_shots_scar20', data))[0]['value']
            except:
                totalScarShots = 0
            try:
                totalScarHits = list(filter(lambda x: x['name'] == 'total_hits_scar20', data))[
                    0]['value']
            except:
                totalScarHits = 0
            if totalScarHits != 0 and totalScarShots != 0:
                ScarAccuracy = "{:.2f}".format(
                    totalScarHits / totalScarShots * 100)
            else:
                ScarAccuracy = 0

            try:
                totalG3SGKills = list(
                    filter(lambda x: x['name'] == 'total_kills_g3sg1', data))[0]['value']
            except:
                totalG3SGKills = 0
            try:
                totalG3SGShots = list(
                    filter(lambda x: x['name'] == 'total_shots_g3sg1', data))[0]['value']
            except:
                totalG3SGShots = 0
            try:
                totalG3SGHits = list(filter(lambda x: x['name'] == 'total_hits_g3sg1', data))[
                    0]['value']
            except:
                totalG3SGHits = 0
            if totalG3SGHits != 0 and totalG3SGShots != 0:
                G3SGAccuracy = "{:.2f}".format(
                    totalG3SGHits / totalG3SGShots * 100)
            else:
                G3SGAccuracy = 0

            try:
                totalNovaKills = list(filter(lambda x: x['name'] == 'total_kills_nova', data))[
                    0]['value']
            except:
                totalNovaKills = 0
            try:
                totalNovaShots = list(filter(lambda x: x['name'] == 'total_shots_nova', data))[
                    0]['value']
            except:
                totalNovaShots = 0
            try:
                totalNovaHits = list(filter(lambda x: x['name'] == 'total_hits_nova', data))[
                    0]['value']
            except:
                totalNovaHits = 0
            if totalNovaHits != 0 and totalNovaShots != 0:
                NovaAccuracy = "{:.2f}".format(
                    totalNovaHits / totalNovaShots * 100)
            else:
                Mag7Accuracy = 0

            try:
                totalMag7Kills = list(filter(lambda x: x['name'] == 'total_kills_mag7', data))[
                    0]['value']
            except:
                totalMag7Kills = 0
            try:
                totalMag7Shots = list(filter(lambda x: x['name'] == 'total_shots_mag7', data))[
                    0]['value']
            except:
                totalMag7Shots = 0
            try:
                totalMag7Hits = list(filter(lambda x: x['name'] == 'total_hits_mag7', data))[
                    0]['value']
            except:
                totalMag7Hits = 0
            if totalMag7Hits != 0 and totalMag7Shots != 0:
                Mag7Accuracy = "{:.2f}".format(
                    totalMag7Hits / totalMag7Shots * 100)
            else:
                Mag7Accuracy = 0

            try:
                totalSawedoffKills = list(
                    filter(lambda x: x['name'] == 'total_kills_sawedoff', data))[0]['value']
            except:
                totalSawedoffKills = 0
            try:
                totalSawedoffShots = list(
                    filter(lambda x: x['name'] == 'total_shots_sawedoff', data))[0]['value']
            except:
                totalSawedoffShots = 0
            try:
                totalSawedoffHits = list(
                    filter(lambda x: x['name'] == 'total_hits_sawedoff', data))[0]['value']
            except:
                totalSawedoffHits = 0
            if totalSawedoffHits != 0 and totalSawedoffShots != 0:
                SawedoffAccuracy = "{:.2f}".format(
                    totalSawedoffHits / totalSawedoffShots * 100)
            else:
                SawedoffAccuracy = 0

            try:
                totalXm1014Kills = list(
                    filter(lambda x: x['name'] == 'total_kills_xm1014', data))[0]['value']
            except:
                totalXm1014Kills = 0
            try:
                totalXm1014Shots = list(
                    filter(lambda x: x['name'] == 'total_shots_xm1014', data))[0]['value']
            except:
                totalXm1014Shots = 0
            try:
                totalXm1014Hits = list(
                    filter(lambda x: x['name'] == 'total_hits_xm1014', data))[0]['value']
            except:
                totalXm1014Hits = 0
            if totalXm1014Hits != 0 and totalXm1014Shots != 0:
                Xm1014Accuracy = "{:.2f}".format(
                    totalXm1014Hits / totalXm1014Shots * 100)
            else:
                Xm1014Accuracy = 0

            try:
                totalNegevKills = list(
                    filter(lambda x: x['name'] == 'total_kills_negev', data))[0]['value']
            except:
                totalNegevKills = 0
            try:
                totalNegevShots = list(
                    filter(lambda x: x['name'] == 'total_shots_negev', data))[0]['value']
            except:
                totalNegevShots = 0
            try:
                totalNegevHits = list(filter(lambda x: x['name'] == 'total_hits_negev', data))[
                    0]['value']
            except:
                totalNegevHits = 0
            if totalNegevHits != 0 and totalNegevShots != 0:
                NegevAccuracy = "{:.2f}".format(
                    totalNegevHits / totalNegevShots * 100)
            else:
                NegevAccuracy = 0

            try:
                totalM249Kills = list(filter(lambda x: x['name'] == 'total_kills_m249', data))[
                    0]['value']
            except:
                totalM249Kills = 0
            try:
                totalM249Shots = list(filter(lambda x: x['name'] == 'total_shots_m249', data))[
                    0]['value']
            except:
                totalM249Shots = 0
            try:
                totalM249Hits = list(filter(lambda x: x['name'] == 'total_hits_m249', data))[
                    0]['value']
            except:
                totalM249Hits = 0
            if totalM249Hits != 0 and totalM249Shots != 0:
                M249Accuracy = "{:.2f}".format(
                    totalM249Hits / totalM249Shots * 100)
            else:
                M249Accuracy = 0

            stats_text_en = strings.stats_en.format(totalPlayedTime, totalKills, totalDeaths, kdRatio,
                                                    totalMatchesPlayed, totalMatchesWon, matchWinPercentage, totalRoundsPlayed, totalPistolRoundsWon,
                                                    totalShots, totalHits, hitAccuracy, hsAccuracy,
                                                    mapName, bestMapPercentage,
                                                    totalMVPs, totalMoneyEarned, totalHostagesResc, totalWeaponDonated, totalBrokenWindows,
                                                    totalDamageDone, totalBombsPlanted, totalBombsDefused,
                                                    totalKnifeKills, totalHEKills, totalMolotovKills, totalZeusShots, totalZeusKills, ZeusAccuracy,
                                                    totalKnifeDuelsWon, totalKillsEnemyWeapon, totalKillsEnemyBlinded, totalKillsZoomedEnemy,
                                                    totalAk47Shots, totalAk47Hits, totalAk47Kills, Ak47Accuracy,
                                                    totalM4Shots, totalM4Hits, totalM4Kills, m4Accuracy,
                                                    totalAWPShots, totalAWPHits, totalAWPKills, AWPAccuracy,
                                                    totalGlockShots, totalGlockHits, totalGlockKills, GlockAccuracy,
                                                    totalUSPShots, totalUSPHits, totalUSPKills, USPAccuracy,
                                                    totalP250Shots, totalP250Hits, totalP250Kills, P250Accuracy,
                                                    totalDualiesShots, totalDualiesHits, totalDualiesKills, DualiesAccuracy,
                                                    totalFiveSevenShots, totalFiveSevenHits, totalFiveSevenKills, FiveSevenAccuracy,
                                                    totalTec9Shots, totalTec9Hits, totalTec9Kills, Tec9Accuracy,
                                                    totalDeagleShots, totalDeagleHits, totalDeagleKills, DeagleAccuracy,
                                                    totalMac10Shots, totalMac10Hits, totalMac10Kills, Mac10Accuracy,
                                                    totalMp7Shots, totalMp7Hits, totalMp7Kills, Mp7Accuracy,
                                                    totalMp9Shots, totalMp9Hits, totalMp9Kills, Mp9Accuracy,
                                                    totalUMPShots, totalUMPHits, totalUMPKills, UMPAccuracy,
                                                    totalBizonShots, totalBizonHits, totalBizonKills, BizonAccuracy,
                                                    totalP90Shots, totalP90Hits, totalP90Kills, P90Accuracy,
                                                    totalFamasShots, totalFamasHits, totalFamasKills, FamasAccuracy,
                                                    totalGalilShots, totalGalilHits, totalGalilKills, GalilAccuracy,
                                                    totalAugShots, totalAugHits, totalAugKills, AugAccuracy,
                                                    totalSgShots, totalSgHits, totalSgKills, SgAccuracy,
                                                    totalSsgShots, totalSsgHits, totalSsgKills, SsgAccuracy,
                                                    totalScarShots, totalScarHits, totalScarKills, ScarAccuracy,
                                                    totalG3SGShots, totalG3SGHits, totalG3SGKills, G3SGAccuracy,
                                                    totalNovaShots, totalNovaHits, totalNovaKills, NovaAccuracy,
                                                    totalMag7Shots, totalMag7Hits, totalMag7Kills, Mag7Accuracy,
                                                    totalSawedoffShots, totalSawedoffHits, totalSawedoffKills, SawedoffAccuracy,
                                                    totalXm1014Shots, totalXm1014Hits, totalXm1014Kills, Xm1014Accuracy,
                                                    totalNegevShots, totalNegevHits, totalNegevKills, NegevAccuracy,
                                                    totalM249Shots, totalM249Hits, totalM249Kills, M249Accuracy)

            stats_text_ru = strings.stats_ru.format(totalPlayedTime, totalKills, totalDeaths, kdRatio,
                                                    totalMatchesPlayed, totalMatchesWon, matchWinPercentage, totalRoundsPlayed, totalPistolRoundsWon,
                                                    totalShots, totalHits, hitAccuracy, hsAccuracy,
                                                    mapName, bestMapPercentage,
                                                    totalMVPs, totalMoneyEarned, totalHostagesResc, totalWeaponDonated, totalBrokenWindows,
                                                    totalDamageDone, totalBombsPlanted, totalBombsDefused,
                                                    totalKnifeKills, totalHEKills, totalMolotovKills, totalZeusShots, totalZeusKills, ZeusAccuracy,
                                                    totalKnifeDuelsWon, totalKillsEnemyWeapon, totalKillsEnemyBlinded, totalKillsZoomedEnemy,
                                                    totalAk47Shots, totalAk47Hits, totalAk47Kills, Ak47Accuracy,
                                                    totalM4Shots, totalM4Hits, totalM4Kills, m4Accuracy,
                                                    totalAWPShots, totalAWPHits, totalAWPKills, AWPAccuracy,
                                                    totalGlockShots, totalGlockHits, totalGlockKills, GlockAccuracy,
                                                    totalUSPShots, totalUSPHits, totalUSPKills, USPAccuracy,
                                                    totalP250Shots, totalP250Hits, totalP250Kills, P250Accuracy,
                                                    totalDualiesShots, totalDualiesHits, totalDualiesKills, DualiesAccuracy,
                                                    totalFiveSevenShots, totalFiveSevenHits, totalFiveSevenKills, FiveSevenAccuracy,
                                                    totalTec9Shots, totalTec9Hits, totalTec9Kills, Tec9Accuracy,
                                                    totalDeagleShots, totalDeagleHits, totalDeagleKills, DeagleAccuracy,
                                                    totalMac10Shots, totalMac10Hits, totalMac10Kills, Mac10Accuracy,
                                                    totalMp7Shots, totalMp7Hits, totalMp7Kills, Mp7Accuracy,
                                                    totalMp9Shots, totalMp9Hits, totalMp9Kills, Mp9Accuracy,
                                                    totalUMPShots, totalUMPHits, totalUMPKills, UMPAccuracy,
                                                    totalBizonShots, totalBizonHits, totalBizonKills, BizonAccuracy,
                                                    totalP90Shots, totalP90Hits, totalP90Kills, P90Accuracy,
                                                    totalFamasShots, totalFamasHits, totalFamasKills, FamasAccuracy,
                                                    totalGalilShots, totalGalilHits, totalGalilKills, GalilAccuracy,
                                                    totalAugShots, totalAugHits, totalAugKills, AugAccuracy,
                                                    totalSgShots, totalSgHits, totalSgKills, SgAccuracy,
                                                    totalSsgShots, totalSsgHits, totalSsgKills, SsgAccuracy,
                                                    totalScarShots, totalScarHits, totalScarKills, ScarAccuracy,
                                                    totalG3SGShots, totalG3SGHits, totalG3SGKills, G3SGAccuracy,
                                                    totalNovaShots, totalNovaHits, totalNovaKills, NovaAccuracy,
                                                    totalMag7Shots, totalMag7Hits, totalMag7Kills, Mag7Accuracy,
                                                    totalSawedoffShots, totalSawedoffHits, totalSawedoffKills, SawedoffAccuracy,
                                                    totalXm1014Shots, totalXm1014Hits, totalXm1014Kills, Xm1014Accuracy,
                                                    totalNegevShots, totalNegevHits, totalNegevKills, NegevAccuracy,
                                                    totalM249Shots, totalM249Hits, totalM249Kills, M249Accuracy)

            telegraph = Telegraph(access_token=config.TELEGRAPH_ACCESS_TOKEN)

            telegraph_response_en = telegraph.create_page(
                f'Statistics #{steam64}', html_content=stats_text_en, author_name='@csgobetabot', author_url='https://t.me/csgobetabot')
            telegraph_response_ru = telegraph.create_page(
                f'Статистика #{steam64}', html_content=stats_text_ru, author_name='@csgobetabot', author_url='https://t.me/csgobetabot')

            url_en = telegraph_response_en['url']
            url_ru = telegraph_response_ru['url']

        return url_en, url_ru
    except Exception as e:
        print('\n\nError:' + str(e) + '\n\n')
        url_en, url_ru = '⚠️ Invalid request.', '⚠️ Неверный запрос.'
        return url_en, url_ru


### DATA CENTERS ###


def dc_africa():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    africa_dc = cacheFile['datacenters']['South Africa']
    capacity, load = africa_dc['capacity'], africa_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    africa_text_ru = strings.dc_africa_ru.format(
        load_ru, capacity_ru, tsRCache)
    africa_text_en = strings.dc_africa_en.format(load, capacity, tsCache)
    return africa_text_en, africa_text_ru


def dc_australia():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    australia_dc = cacheFile['datacenters']['Australia']
    capacity, load = australia_dc['capacity'], australia_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    australia_text_ru = strings.dc_australia_ru.format(
        load_ru, capacity_ru, tsRCache)
    australia_text_en = strings.dc_australia_en.format(load, capacity, tsCache)
    return australia_text_en, australia_text_ru


def dc_eu_north():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    sweden_dc = cacheFile['datacenters']['EU North']
    capacity, load = sweden_dc['capacity'], sweden_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    eu_north_text_ru = strings.dc_north_eu_ru.format(
        load_ru, capacity_ru, tsRCache)
    eu_north_text_en = strings.dc_north_eu_en.format(load, capacity, tsCache)
    return eu_north_text_en, eu_north_text_ru


def dc_eu_west():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    germany_dc = cacheFile['datacenters']['EU West']
    spain_dc = cacheFile['datacenters']['Spain']
    capacity, load = germany_dc['capacity'], germany_dc['load']
    capacity_secondary, load_secondary = spain_dc['capacity'], spain_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    eu_west_text_ru = strings.dc_west_eu_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_west_text_en = strings.dc_west_eu_en.format(
        load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_west_text_en, eu_west_text_ru


def dc_eu_east():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    austria_dc = cacheFile['datacenters']['EU East']
    poland_dc = cacheFile['datacenters']['Poland']
    capacity, load = austria_dc['capacity'], austria_dc['load']
    capacity_secondary, load_secondary = poland_dc['capacity'], poland_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    eu_east_text_ru = strings.dc_east_eu_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    eu_east_text_en = strings.dc_east_eu_en.format(
        load, capacity, load_secondary, capacity_secondary, tsCache)
    return eu_east_text_en, eu_east_text_ru


def dc_usa_north():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    chicago_dc = cacheFile['datacenters']['US Northcentral']
    sterling_dc = cacheFile['datacenters']['US Northeast']
    moseslake_dc = cacheFile['datacenters']['US Northwest']
    capacity, load = chicago_dc['capacity'], chicago_dc['load']
    capacity_secondary, load_secondary = sterling_dc['capacity'], sterling_dc['load']
    capacity_tertiary, load_tertiary = moseslake_dc['capacity'], moseslake_dc['load']
    array = [capacity, load, capacity_secondary,
             load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5]
    usa_north_text_ru = strings.dc_north_us_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    usa_north_text_en = strings.dc_north_us_en.format(
        load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return usa_north_text_en, usa_north_text_ru


def dc_usa_south():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    losangeles_dc = cacheFile['datacenters']['US Southwest']
    atlanta_dc = cacheFile['datacenters']['US Southeast']
    capacity, load = losangeles_dc['capacity'], losangeles_dc['load']
    capacity_secondary, load_secondary = atlanta_dc['capacity'], atlanta_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    usa_south_text_ru = strings.dc_south_us_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    usa_south_text_en = strings.dc_south_us_en.format(
        load, capacity, load_secondary, capacity_secondary, tsCache)
    return usa_south_text_en, usa_south_text_ru


def dc_south_america():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    brazil_dc = cacheFile['datacenters']['Brazil']
    chile_dc = cacheFile['datacenters']['Chile']
    peru_dc = cacheFile['datacenters']['Peru']
    argentina_dc = cacheFile['datacenters']['Argentina']
    capacity, load = brazil_dc['capacity'], brazil_dc['load']
    capacity_secondary, load_secondary = chile_dc['capacity'], chile_dc['load']
    capacity_tertiary, load_tertiary = peru_dc['capacity'], peru_dc['load']
    capacity_quaternary, load_quaternary = argentina_dc['capacity'], argentina_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary,
             capacity_tertiary, load_tertiary, capacity_quaternary, load_quaternary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru, capacity_quaternary_ru, load_quaternary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5], array_ru[6], array_ru[7]
    south_america_text_ru = strings.dc_south_america_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, load_quaternary_ru, capacity_quaternary_ru, tsRCache)
    south_america_text_en = strings.dc_south_america_en.format(
        load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, load_quaternary, capacity_quaternary, tsCache)
    return south_america_text_en, south_america_text_ru


def dc_india():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    mumbai_dc = cacheFile['datacenters']['India']
    chennai_dc = cacheFile['datacenters']['India East']
    capacity, load = mumbai_dc['capacity'], mumbai_dc['load']
    capacity_secondary, load_secondary = chennai_dc['capacity'], chennai_dc['load']
    array = [capacity, load, capacity_secondary, load_secondary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3]
    india_text_ru = strings.dc_india_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, tsRCache)
    india_text_en = strings.dc_india_en.format(
        load, capacity, load_secondary, capacity_secondary, tsCache)
    return india_text_en, india_text_ru


def dc_japan():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    japan_dc = cacheFile['datacenters']['Japan']
    capacity, load = japan_dc['capacity'], japan_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    japan_text_ru = strings.dc_japan_ru.format(load_ru, capacity_ru, tsRCache)
    japan_text_en = strings.dc_japan_en.format(load, capacity, tsCache)
    return japan_text_en, japan_text_ru


def dc_china():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    shanghai_dc = cacheFile['datacenters']['China Shanghai']
    tianjin_dc = cacheFile['datacenters']['China Tianjin']
    guangzhou_dc = cacheFile['datacenters']['China Guangzhou']
    capacity, load = shanghai_dc['capacity'], shanghai_dc['load']
    capacity_secondary, load_secondary = tianjin_dc['capacity'], tianjin_dc['load']
    capacity_tertiary, load_tertiary = guangzhou_dc['capacity'], guangzhou_dc['load']
    array = [capacity, load, capacity_secondary,
             load_secondary, capacity_tertiary, load_tertiary]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru, capacity_secondary_ru, load_secondary_ru, capacity_tertiary_ru, load_tertiary_ru = array_ru[
        0], array_ru[1], array_ru[2], array_ru[3], array_ru[4], array_ru[5]
    china_text_ru = strings.dc_china_ru.format(
        load_ru, capacity_ru, load_secondary_ru, capacity_secondary_ru, load_tertiary_ru, capacity_tertiary_ru, tsRCache)
    china_text_en = strings.dc_china_en.format(
        load, capacity, load_secondary, capacity_secondary, load_tertiary, capacity_tertiary, tsCache)
    return china_text_en, china_text_ru


def dc_emirates():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    emirates_dc = cacheFile['datacenters']['Emirates']
    capacity, load = emirates_dc['capacity'], emirates_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    emirates_text_ru = strings.dc_emirates_ru.format(
        load_ru, capacity_ru, tsRCache)
    emirates_text_en = strings.dc_emirates_en.format(load, capacity, tsCache)
    return emirates_text_en, emirates_text_ru


def dc_singapore():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    singapore_dc = cacheFile['datacenters']['Singapore']
    capacity, load = singapore_dc['capacity'], singapore_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    singapore_text_ru = strings.dc_singapore_ru.format(
        load_ru, capacity_ru, tsRCache)
    singapore_text_en = strings.dc_singapore_en.format(load, capacity, tsCache)
    return singapore_text_en, singapore_text_ru


def dc_hong_kong():
    tsCache, tsRCache = time_converter()[0], time_converter()[1]
    cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
    hongkong_dc = cacheFile['datacenters']['Hong Kong']
    capacity, load = hongkong_dc['capacity'], hongkong_dc['load']
    array = [capacity, load]
    array_ru = []
    for data in array:
        data_ru = translate(data)
        array_ru.append(data_ru)
    capacity_ru, load_ru = array_ru[0], array_ru[1]
    hong_kong_text_ru = strings.dc_hong_kong_ru.format(
        load_ru, capacity_ru, tsRCache)
    hong_kong_text_en = strings.dc_hong_kong_en.format(load, capacity, tsCache)
    return hong_kong_text_en, hong_kong_text_ru
