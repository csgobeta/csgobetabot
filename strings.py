'''Text for initial Commands'''
# English
cmdStart_en = '👋🏼 Hey, {}!\nThis bot is designed to check the number of online players and the availability of CS:GO servers.\n\nFor more information type /help.'
cmdHelp_en = 'ℹ️ This bot is designed by @csgobeta. Source code on <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.\n\n<b>Here are the available commands:</b>\n/status – сheck the status of the servers\n/devcount - show the amount of devs in beta\n/timer - show the time left until cap reset\n/dc – see the status of a specific data center\n/feedback – leave feedback about the bot\n/help – get this message\n\nNote that this bot also works automatically, no need to add it anywhere. Simply open any of your chats and type ‘<code>@csgobetabot </code>‘ in the message field. Then tap on a result to send.'
cmdFeedback_en = "💬 Please, tell us about your <b>suggestions</b> or <b>problems</b> that you have encountered using our bot.\n\nUse /cancel to cancel this command."
# Russian
cmdStart_ru = '👋🏼 Привет, {}!\nЭтот бот предназначен для проверки количества онлайн игроков и доступности CS:GO серверов.\n\nДля большей информации воспользуйтесь /help.'
cmdHelp_ru = 'ℹ️ Этот бот разработан каналом @csgobeta. Исходный код на <a href="https://github.com/csgobeta/csgobetabot">GitHub</a>.\n\n<b>Доступные команды:</b>\n/status – проверить доступность серверов\n/devcount - показать количество разработчиков в бета-версии\n/timer - показать время до сброса ограничений\n/dc – посмотреть состояние определённого дата-центра (на английском языке)\n/feedback – оставить фидбэк про бота\n/help – получить это сообщение\n\nОбратите внимание, что этот бот также работает автоматически, нет необходимости добавлять его куда-либо. Просто откройте любой из Ваших чатов и введите ‘<code>@csgobetabot </code>ʼ в поле сообщения. Затем нажмите на результат для отправки.'
cmdFeedback_ru = '💬 Пожалуйста, расскажите о Ваших <b>пожеланиях</b> или <b>проблемах</b>, с которыми Вы столкнулись, используя бота.\n\nИспользуйте /cancel, чтобы отменить команду.'


'''Text for Status'''
status_tags = ['server status', 'статус серверов', '/status']
# English
statusNormal_en = '<a href="{}">⁠</a>{} Server status:\n\n• Game coordinator: {}\n• Server connection: {}\n• Matchmaking scheduler: {}\n• Player inventories: {}\n\n'
# Russian
statusNormal_ru = '<a href="{}">⁠</a>{} Статус серверов:\n\n• Игровой координатор: {}\n• Подключение к серверам: {}\n• Планировщик матчмейкинга: {}\n• Инвентари игроков: {}\n\n'

'''Text for Matchmaking'''
# English
mmNormal_en = '📊 Matchmaking statistics:\n\n• Online servers: {:,}\n• Online players: {:,}\n• Active players: {:,}\n• Searching players: {:,}\n• Average search time: {}s\n\n'
# Russian
mmNormal_ru = '📊 Статистика матчмейкинга:\n\n• Онлайн серверов: {:,}\n• Онлайн игроков: {:,}\n• Активных игроков: {:,}\n• Игроков в поиске: {:,}\n• Среднее время поиска: {} с.\n\n'

'''Text for Additional info'''
# English
additionalInfo_en = '📁 Additional information:\n\n• 24-hour peak: {:,}\n• All-time peak: {:,}\n• Monthly unique players: {:,}\n\nUpdated on: {} UTC'
# Russian
additionalInfo_ru = '📁 Дополнительная информация:\n\n• 24-часовой пик: {:,}\n• Рекордный пик: {:,}\n• Ежемесячные уникальные игроки: {:,}\n\nОбновлено: {} UTC'

'''Text for Dev count'''
dev_count_tags = ['online devs', 'разработчиков в игре', '/devcount']
# English
devCount_en = '<a href="{}">⁠</a>🧑‍💻 Beta-version of CS:GO (ID710):\n\n• Online devs: {}\n• All-time peak: {}\n\nUpdated on: {} UTC\n\n🏢 Current time at Valve headquarters: {}'
# Russian
devCount_ru = '<a href="{}">⁠</a>🧑‍💻 Бета-версия CS:GO (ID710):\n\n• Онлайн разработчиков: {}\n• Рекордный пик: {}\n\nОбновлено: {} UTC\n\n🏢 Текущее время в штаб-квартире Valve: {}'


'''Text for Timer'''
cap_reset_tags = ['cap reset', 'сброс ограничений', '/timer']
# English
timer_en = '⏳ Time left until experience and drop cap reset: {}d {}h {}m {}s'
# Russian
timer_ru = '⏳ Время до сброса ограничений опыта и дропа: {} д. {} ч. {} м. {} с.'


'''Text for Game Version'''
gameversion_tags = ['game version', 'версия игры', '/gamever']
# English
gameversion_en = '⚙️ Current game version: <code>{}</code>\n\n• Client version: {}\n• Server version: {}\n\nLatest update: {} UTC'
# Russian
gameversion_ru = '⚙️ Текущая версия игры: <code>{}</code>\n\n• Клиентская версия: {}\n• Серверная версия: {}\n\nПоследнее обновление: {} UTC'

'''Text for Wrong Request'''
# English
unknownRequest_en = '🤷‍♀️ Nothing found, please use one of the following commands:'
# Russian
unknownRequest_ru = '🤷‍♀️ Ничего не найдено, пожалуйста, воспользуйтесь одной из приведённых команд:'


'''Text for Wrong API'''
# English
wrongAPI_en = "💀 Issues with Valve's API, please try again later."
# Russian
wrongAPI_ru = '💀 Проблемы с API Valve, пожалуйста, попробуйте позже.'

'''Text for Maintenance'''
# English
maintenance_en = "🛠️ Valve servers are down for the weekly maintenance, please try again later."
# Russian
maintenance_ru = '🛠️ Сервера Valve отключены для еженедельного тех. обслуживания, пожалуйста, попробуйте позже.'


'''Text if something is wrong'''
# English
wrongBOT_en = '🧐 Sorry, something’s not right. Please try again later.'
# Russian
wrongBOT_ru = '🧐 Извините, что-то не так. Пожалуйста, попробуйте позже.'


'''Text for new BuildID'''
#Russian
notiNewBuild_ru = '🆕 Обнаружено новое обновление Counter-Strike: Global Offensive. Пост со списком изменений выйдет в ближайшее время.\n\nID новой сборки: `{}`'

'''Text for Workshop Changes'''
#Russian
notiNewMap_ru = '🆕 Официальный аккаунт CS:GO в Steam загрузил карту *{}* в Мастерскую для совместимости с будущими версиями игры.\n\nВ последующих обновлениях игры стоит ожидать некоторые изменения на данной карте.\n\n{}'
notiNewMaps_ru = '🆕 Официальный аккаунт CS:GO в Steam загрузил карты *{}* в Мастерскую для совместимости с будущими версиями игры.\n\nВ последующих обновлениях игры стоит ожидать некоторые изменения на данных картах.\n\nhttps://steamcommunity.com/profiles/76561198082857351/myworkshopfiles/'

'''Text for new Player Peak'''
#Russian
notiNewPlayerPeak_ru = '🤩 Зарегистрирован новый рекордный пик онлайн игроков в Counter-Strike: Global Offensive. \n\nКоличество игроков: {}'

'''Text for new Dev Peak'''
#Russian
notiNewDevPeak_ru = '😲 Зарегистрирован новый рекордный пик онлайн разработчиков в бета-версии Counter-Strike: Global Offensive. \n\nКоличество разработчиков: {}'


'''Text for DC'''
# English
dc_africa_en = '🇿🇦 South Africaʼs DC status:\n\n• Location: Johannesburg\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_australia_en = '🇦🇺 Australiaʼs DC status:\n\n• Location: Sydney\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_north_eu_en = '🇸🇪 Swedenʼs DC status:\n\n• Location: Stockholm\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_west_eu_en = '🇱🇺 Luxembourgʼs DC status:\n\n• Location: Luxembourg\n• Load: {}\n• Capacity: {}\n\n🇪🇸 Spainʼs DC status:\n\n• Location: Mardid\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_east_eu_en = '🇦🇹 Austriaʼs DC status:\n\n• Location: Vienna\n• Load: {}\n• Capacity: {}\n\n🇵🇱 Polandʼs DC status:\n\n• Location: Warsaw\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_north_us_en = '🇺🇸 Northcentral DC status:\n\n• Location: Chicago\n• Load: {}\n• Capacity: {}\n\n🇺🇸 Northeast DC status:\n\n• Location: Sterling\n• Load: {}\n• Capacity: {}\n\n🇺🇸 Northwest DC status:\n\n• Location: Moses Lake\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_south_us_en = '🇺🇸 Southwest DC status:\n\n• Location: Los Angeles\n• Load: {}\n• Capacity: {}\n\n🇺🇸 Southeast DC status:\n\n• Location: Atlanta\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_south_america_en = '🇧🇷 Brazilʼs DC status:\n\n• Location: Sao Paulo\n• Load: {}\n• Capacity: {}\n\n🇨🇱 Chileʼs DC status:\n\n• Location: Santiago\n• Load: {}\n• Capacity: {}\n\n🇵🇪 Peruʼs DC status:\n\n• Location: Lima\n• Load: {}\n• Capacity: {}\n\n🇦🇷 Argentinaʼs DC Status:\n\n• Location: Buenos Aires\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_india_en = '🇮🇳 Indiaʼs DC status:\n\n• Location: Mumbai\n• Load: {}\n• Capacity: {}\n\n• Location: Chennai\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_japan_en = '🇯🇵 Japanʼs DC status:\n\n• Location: Tokyo\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_china_en = '🇨🇳 Chinaʼs DC status: \n\n• Location: Shanghai\n• Load: {}\n• Capacity: {}\n\n• Location: Tianjin\n• Load: {}\n• Capacity: {}\n\n• Location: Guangzhou\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_emirates_en = '🇦🇪 Emiratesʼ DC status:\n\n• Location: Dubai\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_singapore_en = '🇸🇬 Singaporeʼs DC status:\n\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
dc_hong_kong_en = '🇭🇰 Hong Kongʼs DC status:\n\n• Load: {}\n• Capacity: {}\n\nUpdated on: {} UTC'
# Russian
dc_africa_ru = '🇿🇦 Состояние дата-центра Южной Африки:\n\n• Расположение: Йоханнесбург\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_australia_ru = '🇦🇺 Состояние дата-центра Австралии:\n\n• Расположение: Сидней\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_north_eu_ru = '🇸🇪 Состояние дата-центра Швеции:\n\n• Расположение: Стокгольм\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_west_eu_ru = '🇱🇺 Состояние дата-центра Люксембурга:\n\n• Расположение: Люксембург\n• Загруженность: {}\n• Доступность: {}\n\n🇪🇸 Состояние дата-центра Испании:\n\n• Расположение: Мадрид\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_east_eu_ru = '🇦🇹 Состояние дата-центра Австрии:\n\n• Расположение: Вена\n• Загруженность: {}\n• Доступность: {}\n\n🇵🇱 Состояние дата-центра Польши:\n\n• Расположение: Варшава\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_north_us_ru = '🇺🇸 Состояние северо-центрального дата-центра:\n\n• Расположение: Чикаго\n• Загруженность: {}\n• Доступность: {}\n\n🇺🇸 Состояние северо-восточного дата-центра:\n\n• Расположение: Стерлинг\n• Загруженность: {}\n• Доступность: {}\n\n🇺🇸 Состояние северо-западного дата-центра:\n\n• Расположение: Мозес Лейк\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_south_us_ru = '🇺🇸 Состояние юго-западного дата-центра:\n\n• Расположение: Лос-Анджелес\n• Загруженность: {}\n• Доступность: {}\n\n🇺🇸 Состояние юго-восточного дата-центра:\n\n• Расположение: Атланта\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_south_america_ru = '🇧🇷 Состояние дата-центра Бразилии:\n\n• Расположение: Сан-Паулу\n• Загруженность: {}\n• Доступность: {}\n\n🇨🇱 Состояние дата-центра Чили:\n\n• Расположение: Сантьяго\n• Загруженность: {}\n• Доступность: {}\n\n🇵🇪 Состояние дата-центра Перу:\n\n• Расположение: Лима\n• Загруженность: {}\n• Доступность: {}\n\n🇦🇷 Состояние дата-центра Аргентины:\n\n• Расположение: Буэнос-Айрес\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_india_ru = '🇮🇳 Состояние дата-центров Индии:\n\n• Расположение: Мумбаи\n• Загруженность: {}\n• Доступность: {}\n\n• Расположение: Ченнай\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_japan_ru = '🇯🇵 Состояние дата-центра Японии:\n\n• Расположение: Токио\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_china_ru = '🇨🇳 Состояние дата-центров Китая: \n\n• Расположение: Шанхай\n• Загруженность: {}\n• Доступность: {}\n\n• Расположение: Тяньцзинь\n• Загруженность: {}\n• Доступность: {}\n\n• Расположение: Гуанчжоу\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_emirates_ru = '🇦🇪 Состояние дата-центра Эмиратов:\n\n• Расположение: Дубай\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_singapore_ru = '🇸🇬 Состояние дата-центра Сингапура:\n\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'
dc_hong_kong_ru = '🇭🇰 Состояние дата-центра Гонконга:\n\n• Загруженность: {}\n• Доступность: {}\n\nОбновлено: {} UTC'


'''Tags for inline DC'''
# General
dc_tags = ['dc', 'data center', 'data centers', 
                    'дц', 'дата центер', 'дата центры', 'дата-центер', 
                    'дата-центры','/dc']
european_tags = ['eu', 'europe', 
                    'европа', 
                    '/europe']
asian_tags = ['as', 'asia', 
                    'азия', 
                    '/asia']
american_tags = ['na', 'north america', 'usa', 'united states', 
                    'северная америка', 'сша', 'соединённые штаты', 
                    '/usa']
australian_tags = ['au', 'australia', 'sydney', 
                    'австралия', 'сидней', 
                    '/australia']
african_tags = ['za', 'africa', 'south africa', 'johannesburg', 
                    'африка', 'южная африка', 'йоханнесбург']

# Detailed
south_american_tags = ['sa', 'south america', 'brazil', 'sao paolo', 'chile', 'santiago', 'peru', 'lima', 'argentina', 'buenos aires',
                    'южная америка', 'бразилия', 'сан-паулу', 'сан паулу', 'чили', 'сантьяго', 'перу', 'лима', 'аргентина', 'буэнос-айрес', 'буэнос айрес',
                    '/south_africa']
north_european_tags = ['north europe', 'sweden', 'stockholm', 
                    'северная европа', 'швеция', 'стокгольм', 
                    'north', 'север', '/eu_north']
east_european_tags = ['east europe', 'austria', 'vienna', 'poland', 'warsaw', 
                    'восточная европа', 'австрия', 'вена', 'польша', 'варшава',
                    'east', 'восток', '/eu_east']
west_european_tags = ['west europe', 'luxembourg', 'spain', 'madrid', 
                    'западная европа', 'люксембург', 'испания', 'мадрид', 
                    'west', 'запад', '/eu_west']
northern_usa_tags = ['northcentral', 'northeast', 'northwest', 'chicago', 'sterling', 'moses lake', 
                    'северо-центр', 'северо-восток', 'северо-запад', 'чикаго', 'стерлинг', 'мозес лейк', 
                    'nоrth', 'сeвер', '/usa_north']
southern_usa_tags = ['southeast', 'southwest', 'los angeles', 'atalanta', 
                    'юго-запад', 'юго-восток', 'лос-анджелес', 'лос анджелес', 'атланта', 
                    'south', 'юг', '/usa_south']
chinese_tags = ['china', 'shanghai', 'tianjin', 'guangzhou', 
                    'китай', 'шанхай', 'тяньцзинь', 'гуанчжоу',
                    '/china']
emirati_tags = ['emirates', 'dubai', 
                    'эмираты', 'дубай',
                    '/emirates']
hong_kongese_tags = ['hong kong', 
                    'гонконг',
                    '/hong_kong']
indian_tags = ['india', 'mumbai', 'chennai', 
                    'индия', 'мумбаи',  'ченнай',
                    '/india']
japanese_tags = ['japan', 'tokyo', 
                    'япония', 'токио',
                    '/japan']
singaporean_tags = ['singapore', 
                    'сингапур',
                    '/singapore']

"""Text for Archive data"""
#Russian
gun_data_ru = '🗂 Детальная информация про {}:\n\n• Происхождение: {}\n• Стоимость: {}$\n• Обойма: {}/{}\n• Скорострельность: {} в/м.\n• Награда за убийство: {}$\n• Мобильность: {} ед.\n\n• Бронепробиваемость: {}%\n• Дальность поражения (стоя / сидя): {} / {} м.\n\n• Время, за которое достаётся оружие: {} с.\n• Перезарядка: {} / {} с.\n(готовность обоймы / готовность к стрельбе)\n\n💢 Информация об уроне:\n(противник в броне / без брони)\n\n• Голова: {} / {}\n• Грудь и руки: {} / {}\n• Живот: {} / {}\n• Ноги: {} / {}'
origin_list_ru = ['Германия', 'Австрия', 'Италия', 'Швейцария', 'Чехия', 'Бельгия', 'Швеция', 'Израль',
                'Соединённые Штаты', 'Россия', 'Франция', 'Соединённое Королевство', 'Южная Африка']
#English
gun_data_en = '🗂 Detailed information about {}:\n\n• Origin: {}\n• Cost: ${}\n• Clip size: {}/{}\n• Fire rate: {} RPM\n• Kill reward: ${}\n• Movement speed: {} units\n\n• Armor penetration: {}%\n• Range accuracy (stand / crouch): {}m / {}m\n\n• Draw time: {}s\n• Reload time: {}s / {}s\n(clip ready / fire ready)\n\n💢 Damage information:\n(enemy with armor / without armor)\n\n• Head: {} / {}\n• Chest and arms: {} / {}\n• Stomach: {} / {}\n• Legs: {} / {}'
origin_list_en = ['Germany', 'Austria', 'Italy', 'Switzerland', 'Czech Republic', 'Belgium', 'Sweden', 'Israel',
                'United States', 'Russia', 'France', 'United Kingdom', 'South Africa']
###
gun_name_list = ['usp-s', 'p2000', 'glock-18', 'dual berettas', 'p250', 'cz75-auto', 'five-seven', 'tec-9', 'desert eagle', 'r8 revolver',
                'mp9', 'mac-10', 'mp7', 'mp5-sd', 'ump-45','p90', 'pp-bizon', 'famas', 'galil ar', 'm4a4', 'm4a1-s', 'ak-47', 'aug',
                'sg 553', 'ssg 08', 'awp', 'scar-20', 'g3sg1', 'nova', 'xm1014', 'mag-7', 'sawed-off', 'm249', 'negev']
gun_id_list = ['usps', 'p2000', 'glock18', 'dualberettas', 'p250', 'cz75auto', 'fiveseven', 'tec9', 'deserteagle', 'r8revolver',
                'mp9', 'mac10', 'mp7', 'mp5sd', 'ump45','p90', 'ppbizon', 'famas', 'galilar', 'm4a4', 'm4a1s', 'ak47', 'aug',
                'sg553', 'ssg08', 'awp', 'scar20', 'g3sg1', 'nova', 'xm1014', 'mag7', 'sawedoff', 'm249', 'negev']
gun_tags = ['gun database', 'база данных оружий', '/guns']