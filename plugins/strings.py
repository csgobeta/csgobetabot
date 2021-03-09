### Text for initial Commands ###
# English
cmdStart_en = '''👋🏼 Hey, {}!
This bot is designed to check the number of online players and the availability of CS:GO servers.

For more information type /help.'''
cmdHelp_en = '''<a href="https://telegra.ph/Detailed-description-03-07">‎‎‎‎</a>ℹ️ This bot is designed by @csgobeta. Source code on <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.

telegra.ph/Detailed-description-03-07'''
cmdFeedback_en = '''💬 Please, tell us about your <b>suggestions</b> or <b>problems</b> that you have encountered using our bot.

Use /cancel to cancel this command.'''
# Russian
cmdStart_ru = '''👋🏼 Привет, {}!
Этот бот предназначен для проверки количества онлайн игроков и доступности CS:GO серверов.

Для большей информации воспользуйтесь /help.'''
cmdHelp_ru = '''<a href="https://telegra.ph/Podrobnoe-opisanie-03-07">‎‎‎‎‎‎‎</a>ℹ️ Этот бот разработан каналом @csgobeta. Исходный код на <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.

telegra.ph/Podrobnoe-opisanie-03-07'''
cmdFeedback_ru = '''💬 Пожалуйста, расскажите о Ваших <b>пожеланиях</b> или <b>проблемах</b>, из которыми Вы столкнулись, используя бота.

Используйте /cancel, чтобы отменить команду.'''


### Text for Status ###
# English
status_en = '''{} <b>CS:GO service status:</b>

• Game coordinator: {}
• Server connection: {}
• Matchmaking scheduler: {}
• Player inventories: {}
• Steam web API: {}

Updated on: {} UTC'''
# Russian
status_ru = '''{} <b>Состояние служб CS:GO:</b>

• Игровой координатор: {}
• Подключение к серверам: {}
• Планировщик матчмейкинга: {}
• Инвентари игроков: {}
• Steam веб-API: {}

Обновлено: {} UTC'''


### Text for Matchmaking ###
# English
mm_en = '''<a href="{}">‎‎‎‎</a>📊 <b>Matchmaking statistics:</b>

• Online servers: {:,}
• Online players: {:,}
• Active players: {:,}
• Players searching: {:,}
• Average search time: {}s'''
# Russian
mm_ru = '''<a href="{}">‎‎‎‎</a>⁠📊 <b>Статистика матчмейкинга:</b>

• Онлайн серверов: {:,}
• Онлайн игроков: {:,}
• Активных игроков: {:,}
• Игроков в поиске: {:,}
• Среднее время поиска: {} с.'''


### Text for Additional info ###
# English
additionalInfo_en = '''📁 <b>Additional information:</b>

• 24-hour peak: {:,}
• All-time peak: {:,}
• Monthly unique players: {:,}

Updated on: {} UTC'''
# Russian
additionalInfo_ru = '''📁 <b>Дополнительная информация:</b>

• 24-часовой пик: {:,}
• Рекордный пик: {:,}
• Ежемесячные уникальные игроки: {:,}

Обновлено: {} UTC'''


### Text for Dev count ###
# English
devCount_en = '''<a href="{}">⁠‎‎‎</a>🧑‍💻 <b>Beta-version of CS:GO (ID710):</b>

• Online developers: {}
• All-time peak: {}

Updated on: {} UTC

🏢 Current time at Valve headquarters: {}'''
# Russian
devCount_ru = '''<a href="{}">⁠‎‎‎</a>🧑‍💻 <b>Бета-версия CS:GO (ID710):</b>

• Онлайн разработчиков: {}
• Рекордный пик: {}

Обновлено: {} UTC

🏢 Текущее время в штаб-квартире Valve: {}'''


### Text for Timer ###
# English
timer_en = '⏳ Time left until experience and drop cap reset: {}d {}h {}m {}s'
# Russian
timer_ru = '⏳ Время до сброса ограничений опыта и дропа: {} д. {} ч. {} м. {} с.'


### Text for Game Version ###
# English
gameversion_en = '''⚙️ Current game version: <code>{} ({}/{})</code>

Latest CS:GO update: {} UTC'''
# Russian
gameversion_ru = '''⚙️ Текущая версия игры: <code>{} ({}/{})</code>

Последнее обновление CS:GO: {} UTC'''


### URL examples ###
# English
url_ex_en = '''📖 Please, enter one of the following options:
        
• Profile URL (ex: https://steamcommunity.com/id/csgobetaN2),
• Steam ID (ex: 76561199148006660)
• Custom URL (ex: csgobetaN1)

Use /cancel to cancel this command.'''
# Russian
url_ex_ru = '''🔗 Пожалуйста, введите один из следующих вариантов:

• Ссылка на профиль (напр: https://steamcommunity.com/id/csgobetaN2)
• Steam ID (напр: 76561199148006660)
• Личная ссылка (напр: csgobetaN1)

Используйте /cancel, чтобы отменить команду.'''


### Profile information ###
# English
bans_en = '''🔍 <b>General profile information:</b>

• Custom URL: <code>{}</code>
• Steam ID: <code>{}</code>
• Account ID: <code>{}</code>
• Steam2 ID: <code>{}</code>
• Steam3 ID: <code>{}</code>
• Invite URL: {}
• CS:GO friend code: <i>{}</i>

📛 <b>Bans and restrictions:</b>

• Game bans: {}
• VAC bans: {}
• Community ban: {}
• Trade ban: {}'''
# Russian
bans_ru = '''🔍 <b>Общая информация профиля:</b>

• Личная ссылка: <code>{}</code>
• Steam ID: <code>{}</code>
• Account ID: <code>{}</code>
• Steam2 ID: <code>{}</code>
• Steam3 ID: <code>{}</code>
• Пригласительная ссылка: {}
• Код друга CS:GO: <i>{}</i>

📛 <b>Запреты и ограничения:</b>

• Игровые баны: {}
• VAC баны: {}
• Бан в сообществе: {}
• Трейд бан: {}'''


### In-game stats ###
# English
stats_en = '''📊 <b>General in-game statistics:</b>

• Total playtime (official matchmaking): {}h
• Total kills: {}
• Total deaths: {}
• K/D ratio: {}

🔫 <b>Gun statistics:</b>

• Total AK-47 kills: {}
• AK-47 accuracy: {}%

• Total M4 kills: {}
• M4 accuracy: {}%

• Total AWP kills: {}
• AWP accuracy: {}%'''
# Russian
stats_ru = '''📊 <b>Общая игровая статистика:</b>

• Общее время в игре (оф. матчмейкинг): {} ч.
• Всего убийств: {}
• Всего смертей: {}
• Соотношение У/С: {}

🔫 <b>Статистика оружий:</b>

• Всего убийств из AK-47: {}
• Точность AK-47: {}%

• Всего убийств из M4: {}
• Точность M4: {}%

• Всего убийств из AWP: {}
• Точность AWP: {}%'''


### Text for Wrong Request ###
# English
unknownRequest_en = '⚠️ Nothing found, please use of the following buttons:'
# Russian
unknownRequest_ru = '⚠️ Ничего не найдено, пожалуйста, воспользуйтесь одной из приведённых кнопок:'


### Text for Wrong API ###
# English
wrongAPI_en = '💀 Issues with Steam API, please try again later.'
# Russian
wrongAPI_ru = '💀 Проблемы из Steam API, пожалуйста, попробуйте позже.'


### Text for Maintenance ###
# English
maintenance_en = '🛠️ Steam servers are down for the weekly maintenance, please try again later.'
# Russian
maintenance_ru = '🛠️ Сервера Steam отключены для еженедельного тех. обслуживания, пожалуйста, попробуйте позже.'


### Text if something is wrong ###
# English
wrongBOT_en = '🧐 Sorry, something’s not right. Please try again later.'
# Russian
wrongBOT_ru = '🧐 Извините, что-то не так. Пожалуйста, попробуйте позже.'


### Text for new BuildID ###
#Russian
notiNewBuild_ru = '''⚡️ Обнаружено новое обновление Counter-Strike: Global Offensive. Пост со списком изменений выйдет в ближайшее время.

ID новой сборки: <code>{}</code>'''


### Text for new DPR BuildID ###
#Russian
notiNewDPRBuild_ru = '''🔒 Защищённая паролем DPR* сборка CS:GO была обновлена. Это может означать, что в скором времени выйдет новое обновление.

<i>*DPR — developer pre-release</i>

ID новой сборки: <code>{}</code>'''


### Text for Workshop Changes ###
#Russian
notiNewMap_ru = '''🆕 Официальный аккаунт CS:GO в Steam загрузил карту <b>{}</b> в Мастерскую для совместимости из будущими версиями игры.

В последующих обновлениях игры стоит ожидать некоторые изменения на данной карте.

🔗 steamcommunity.com/sharedfiles/filedetails/?id={}'''

notiNewMaps_ru = '''🆕 Официальный аккаунт CS:GO в Steam загрузил карты <b>{}</b> в Мастерскую для совместимости из будущими версиями игры.

В последующих обновлениях игры стоит ожидать некоторые изменения на данных картах.

🔗 steamcommunity.com/profiles/76561198082857351/myworkshopfiles/'''


### Text for new Player Peak ###
#Russian
notiNewPlayerPeak_ru = '''🤩 Зарегистрирован новый рекордный пик онлайн игроков в Counter-Strike: Global Offensive.

Количество игроков: {}'''


### Text for new Dev Peak ###
#Russian
notiNewDevPeak_ru = '''🔍 Зарегистрирован новый рекордный пик онлайн разработчиков в бета-версии Counter-Strike: Global Offensive.

Количество разработчиков: {}'''


### Text for new Tweet ###
#Russian
notiNewTweet_ru = '''💬 Официальный аккаунт CS:GO в Twitter:

«{}»

🔗 twitter.com/csgo/status/{}'''


### Text for DC ###
# English
dc_africa_en = '''🇿🇦 South Africaʼs DC status:

• Location: Johannesburg
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_australia_en = '''🇦🇺 Australiaʼs DC status:

• Location: Sydney
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_north_eu_en = '''🇸🇪 Swedenʼs DC status:

• Location: Stockholm
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_west_eu_en = '''🇩🇪 Germanyʼs DC status:

• Location: Frankfurt
• Load: {}
• Capacity: {}

🇪🇸 Spainʼs DC status:

• Location: Mardid
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_east_eu_en = '''🇦🇹 Austriaʼs DC status:

• Location: Vienna
• Load: {}
• Capacity: {}

🇵🇱 Polandʼs DC status:

• Location: Warsaw
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_north_us_en = '''🇺🇸 Northcentral DC status:

• Location: Chicago
• Load: {}
• Capacity: {}

🇺🇸 Northeast DC status:

• Location: Sterling
• Load: {}
• Capacity: {}

🇺🇸 Northwest DC status:

• Location: Moses Lake
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_south_us_en = '''🇺🇸 Southwest DC status:

• Location: Los Angeles
• Load: {}
• Capacity: {}

🇺🇸 Southeast DC status:

• Location: Atlanta
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_south_america_en = '''🇧🇷 Brazilʼs DC status:

• Location: Sao Paulo
• Load: {}
• Capacity: {}

🇨🇱 Chileʼs DC status:

• Location: Santiago
• Load: {}
• Capacity: {}

🇵🇪 Peruʼs DC status:

• Location: Lima
• Load: {}
• Capacity: {}

🇦🇷 Argentinaʼs DC Status:

• Location: Buenos Aires
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_india_en = '''🇮🇳 Indiaʼs DC status:

• Location: Mumbai
• Load: {}
• Capacity: {}

• Location: Chennai
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_japan_en = '''🇯🇵 Japanʼs DC status:

• Location: Tokyo
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_china_en = '''🇨🇳 Chinaʼs DC status:

• Location: Shanghai
• Load: {}
• Capacity: {}

• Location: Tianjin
• Load: {}
• Capacity: {}

• Location: Guangzhou
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_emirates_en = '''🇦🇪 Emiratesʼ DC status:

• Location: Dubai
• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_singapore_en = '''🇸🇬 Singaporeʼs DC status:

• Load: {}
• Capacity: {}

Updated on: {} UTC'''

dc_hong_kong_en = '''🇭🇰 Hong Kongʼs DC status:

• Load: {}
• Capacity: {}

Updated on: {} UTC'''
# Russian
dc_africa_ru = '''🇿🇦 Состояние дата-центра Южной Африки:

• Расположение: Йоханнесбург
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''
dc_australia_ru = '''🇦🇺 Состояние дата-центра Австралии:

• Расположение: Сидней
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_north_eu_ru = '''🇸🇪 Состояние дата-центра Швеции:

• Расположение: Стокгольм
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_west_eu_ru = '''🇩🇪 Состояние дата-центра Германии:

• Расположение: Франкфурт
• Загруженность: {}
• Доступность: {}

🇪🇸 Состояние дата-центра Испании:

• Расположение: Мадрид
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_east_eu_ru = '''🇦🇹 Состояние дата-центра Австрии:

• Расположение: Вена
• Загруженность: {}
• Доступность: {}

🇵🇱 Состояние дата-центра Польши:

• Расположение: Варшава
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_north_us_ru = '''🇺🇸 Состояние северо-центрального дата-центра:

• Расположение: Чикаго
• Загруженность: {}
• Доступность: {}

🇺🇸 Состояние северо-восточного дата-центра:

• Расположение: Стерлинг
• Загруженность: {}
• Доступность: {}

🇺🇸 Состояние северо-западного дата-центра:

• Расположение: Мозеиз Лейк
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_south_us_ru = '''🇺🇸 Состояние юго-западного дата-центра:

• Расположение: Лос-Анджелес
• Загруженность: {}
• Доступность: {}

🇺🇸 Состояние юго-восточного дата-центра:

• Расположение: Атланта
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_south_america_ru = '''🇧🇷 Состояние дата-центра Бразилии:

• Расположение: Сан-Паулу
• Загруженность: {}
• Доступность: {}

🇨🇱 Состояние дата-центра Чили:

• Расположение: Сантьяго
• Загруженность: {}
• Доступность: {}

🇵🇪 Состояние дата-центра Перу:

• Расположение: Лима
• Загруженность: {}
• Доступность: {}

🇦🇷 Состояние дата-центра Аргентины:

• Расположение: Буэнос-Айрес
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_india_ru = '''🇮🇳 Состояние дата-центров Индии:

• Расположение: Мумбаи
• Загруженность: {}
• Доступность: {}

• Расположение: Ченнай
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_japan_ru = '''🇯🇵 Состояние дата-центра Японии:

• Расположение: Токио
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_china_ru = '''🇨🇳 Состояние дата-центров Китая:

• Расположение: Шанхай
• Загруженность: {}
• Доступность: {}

• Расположение: Тяньцзинь
• Загруженность: {}
• Доступность: {}

• Расположение: Гуанчжоу
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_emirates_ru = '''🇦🇪 Состояние дата-центра Эмиратов:

• Расположение: Дубай
• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_singapore_ru = '''🇸🇬 Состояние дата-центра Сингапура:

• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''

dc_hong_kong_ru = '''🇭🇰 Состояние дата-центра Гонконга:

• Загруженность: {}
• Доступность: {}

Обновлено: {} UTC'''


"""Text for Guns"""
#Russian
gun_data_ru = '''🗂 Детальная информация про {}:

• Происхождение: {}
• Стоимость: {}$
• Обойма: {}/{}
• Скорострельность: {} в/м.
• Награда за убийство: {}$
• Мобильность: {} ед.

• Бронепробиваемость: {}%
• Дальность поражения (стоя / сидя): {} / {} м.

• Время, за которое достаётся оружие: {} с.
• Перезарядка: {} / {} с.
(готовность обоймы / готовность к стрельбе)

💢 Информация об уроне:
(противник в броне / без брони)

• Голова: {} / {}
• Грудь и руки: {} / {}
• Живот: {} / {}
• Ноги: {} / {}'''
#English
gun_data_en = '''🗂 Detailed information about {}:

• Origin: {}
• Cost: ${}
• Clip size: {}/{}
• Fire rate: {} RPM
• Kill reward: ${}
• Movement speed: {} units

• Armor penetration: {}%
• Range accuracy (stand / crouch): {}m / {}m

• Draw time: {}s
• Reload time: {}s / {}s
(clip ready / fire ready)

💢 Damage information:
(enemy with armor / without armor)

• Head: {} / {}
• Chest and arms: {} / {}
• Stomach: {} / {}
• Legs: {} / {}'''