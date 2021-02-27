from telebot import types

# Delete keyboard
markup_del = types.ReplyKeyboardRemove(False)


### English ###


# Back buttons
back_button_en = types.KeyboardButton('⏪ Back')
back_button_alt_en = types.KeyboardButton('⏪ Bаck')
back_button_alt_en_2 = types.KeyboardButton('⏪ Вack')
back_button_alt_en_3 = types.KeyboardButton('⏪ Bасk')

# Default
markup_en = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
server_status_en = types.KeyboardButton('Server status')
matchmaking_en = types.KeyboardButton('MM stats')
devcount_en = types.KeyboardButton('Online devs')
dc_en = types.KeyboardButton('Data centers')
other_en = types.KeyboardButton('Other')
markup_en.add(server_status_en, matchmaking_en, devcount_en, dc_en, other_en)

# Other
markup_other_en = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
timer_en = types.KeyboardButton('Cap reset')
gv_en = types.KeyboardButton('Game version')
guns_en = types.KeyboardButton('Gun database')
markup_other_en.add(gv_en, timer_en, guns_en)
markup_other_en.add(back_button_en)

# DC
markup_DC_en = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
europe_en = types.KeyboardButton('Europe')
asia_en = types.KeyboardButton('Asia')
south_africa_en = types.KeyboardButton('South Africa')
south_america_en = types.KeyboardButton('South America')
australia_en = types.KeyboardButton('Australia')
usa_en =  types.KeyboardButton('USA')
markup_DC_en.add(asia_en, australia_en, europe_en, south_africa_en, south_america_en, usa_en, back_button_en)

# DC Asia
markup_DC_Asia_en = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
india_en = types.KeyboardButton('India')
emirates_en = types.KeyboardButton('Emirates')
china_en = types.KeyboardButton('China')
singapore_en = types.KeyboardButton('Singapore')
hong_kong_en = types.KeyboardButton('Hong Kong')
japan_en = types.KeyboardButton('Japan')
markup_DC_Asia_en.add(china_en, emirates_en, hong_kong_en, india_en, japan_en, singapore_en, back_button_alt_en)

# DC Europe
markup_DC_EU_en = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West_en = types.KeyboardButton('West')
eu_East_en = types.KeyboardButton('East')
eu_North_en = types.KeyboardButton('North')
markup_DC_EU_en.add(eu_East_en, eu_North_en, eu_West_en, back_button_alt_en)

# DC USA
markup_DC_USA_en = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest_en = types.KeyboardButton('Nоrth')
usa_Southwest_en = types.KeyboardButton('South')
markup_DC_USA_en.add(usa_Northwest_en, usa_Southwest_en, back_button_alt_en)

# Guns
markup_guns_en = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols_en = types.KeyboardButton('Pistols')
smgs_en = types.KeyboardButton('SMGs')
rifles_en = types.KeyboardButton('Rifles')
heavy_en = types.KeyboardButton('Heavy')
markup_guns_en.add(pistols_en, smgs_en, rifles_en, heavy_en, back_button_alt_en_2)

# Pistols
markup_pistols_en = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
usps = types.KeyboardButton('USP-S')
p2000 = types.KeyboardButton('P2000')
glock = types.KeyboardButton('Glock-18')
dualies = types.KeyboardButton('Dual Berettas')
p250 = types.KeyboardButton('P250')
cz75 = types.KeyboardButton('CZ75-Auto')
five_seven = types.KeyboardButton('Five-SeveN')
tec = types.KeyboardButton('Tec-9')
deagle = types.KeyboardButton('Desert Eagle')
r8 = types.KeyboardButton('R8 Revolver')
markup_pistols_en.add(usps, p2000, glock, dualies, p250, cz75, five_seven, tec, deagle, r8)
markup_pistols_en.add(back_button_alt_en_3)

# SMGs
markup_smgs_en = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
mp9 = types.KeyboardButton('MP9')
mac10 = types.KeyboardButton('MAC-10')
mp7 = types.KeyboardButton('MP7')
mp5 = types.KeyboardButton('MP5-SD')
ump = types.KeyboardButton('UMP-45')
p90 = types.KeyboardButton('P90')
pp = types.KeyboardButton('PP-Bizon')
markup_smgs_en.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs_en.add(back_button_alt_en_3)

# Rifles
markup_rifles_en = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
famas = types.KeyboardButton('Famas')
galil = types.KeyboardButton('Galil AR')
m4a4 = types.KeyboardButton('M4A4')
m4a1 = types.KeyboardButton('M4A1-S')
ak = types.KeyboardButton('AK-47')
aug = types.KeyboardButton('AUG')
sg = types.KeyboardButton('SG 553')
ssg = types.KeyboardButton('SSG 08')
awp = types.KeyboardButton('AWP')
scar = types.KeyboardButton('SCAR-20')
g3sg1 = types.KeyboardButton('G3SG1')
markup_rifles_en.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles_en.add(back_button_alt_en_3)

# Heavy
markup_heavy_en = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
nova = types.KeyboardButton('Nova')
xm1014 = types.KeyboardButton('XM1014')
mag7 = types.KeyboardButton('MAG-7')
sawedoff = types.KeyboardButton('Sawed-Off')
m249 = types.KeyboardButton('M249')
negev = types.KeyboardButton('Negev')
markup_heavy_en.add(nova, xm1014, mag7, sawedoff, m249, negev)
markup_heavy_en.add(back_button_alt_en_3)


### Russian ###


# Back Buttons
back_button_ru = types.KeyboardButton('⏪ Назад')
back_button_alt_ru = types.KeyboardButton('⏪ Нaзад')
back_button_alt_2_ru = types.KeyboardButton('⏪ Haзaд')
back_button_alt_3_ru = types.KeyboardButton('⏪ Haзад')

# Default
markup_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
server_status_ru = types.KeyboardButton('Статус серверов')
mathcmaking_ru = types.KeyboardButton('Статистика ММ')
devcount_ru = types.KeyboardButton('Разработчиков в игре')
dc_ru = types.KeyboardButton('Дата-центры')
other_ru = types.KeyboardButton('Другое')
markup_ru.add(server_status_ru, mathcmaking_ru, devcount_ru, dc_ru, other_ru)

# Other
markup_other_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
gv_ru = types.KeyboardButton('Версия игры')
guns_ru = types.KeyboardButton('База данных оружий')
timer_ru = types.KeyboardButton('Сброс ограничений')
markup_other_ru.add(gv_ru, timer_ru, guns_ru)
markup_other_ru.add(back_button_ru)

# DC
markup_DC_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
europe_ru = types.KeyboardButton('Европа')
asia_ru = types.KeyboardButton('Азия')
africa_ru = types.KeyboardButton('Южная Африка')
south_america_ru = types.KeyboardButton('Южная Америка')
australia_ru = types.KeyboardButton('Австралия') 
usa_ru =  types.KeyboardButton('США')
markup_DC_ru.add(australia_ru, asia_ru, europe_ru, usa_ru, south_america_ru, africa_ru, back_button_ru)

# DC Europe
markup_DC_EU_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
eu_West_ru = types.KeyboardButton('Запад')
eu_East_ru = types.KeyboardButton('Восток')
eu_North_ru = types.KeyboardButton('Север')
markup_DC_EU_ru.add(eu_East_ru, eu_West_ru, eu_North_ru, back_button_alt_ru)

# DC Asia
markup_DC_Asia_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
india_ru = types.KeyboardButton('Индия')
emirates_ru = types.KeyboardButton('Эмираты')
china_ru = types.KeyboardButton('Китай')
singapore_ru = types.KeyboardButton('Сингапур')
hong_kong_ru = types.KeyboardButton('Гонконг')
japan_ru = types.KeyboardButton('Япония')
markup_DC_Asia_ru.add(hong_kong_ru, india_ru, china_ru, singapore_ru, emirates_ru, japan_ru, back_button_alt_ru)

# DC USA
markup_DC_USA_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
usa_Northwest_ru = types.KeyboardButton('Сeвер')
usa_Southwest_ru = types.KeyboardButton('Юг')
markup_DC_USA_ru.add(usa_Northwest_ru, usa_Southwest_ru, back_button_alt_ru)

# Guns
markup_guns_ru = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
pistols = types.KeyboardButton('Пистолеты')
smgs = types.KeyboardButton('Пистолеты-пулемёты')
rifles = types.KeyboardButton('Винтовки')
heavy = types.KeyboardButton('Тяжёлое оружие')
markup_guns_ru.add(pistols, smgs, rifles, heavy, back_button_alt_2_ru)

# Pistols
markup_pistols_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_pistols_ru.add(usps, p2000, glock, dualies, p250, cz75, five_seven, tec, deagle, r8)
markup_pistols_ru.add(back_button_alt_3_ru)

# SMGs
markup_smgs_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_smgs_ru.add(mp9, mac10, mp7, mp5, ump, p90, pp)
markup_smgs_ru.add(back_button_alt_3_ru)

# Rifles
markup_rifles_ru = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
markup_rifles_ru.add(famas, galil, m4a4, m4a1, ak, aug, sg, ssg, awp, scar, g3sg1)
markup_rifles_ru.add(back_button_alt_3_ru)

# Heavy Russian
markup_heavy_ru = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
markup_heavy_ru.add(nova, xm1014, mag7, sawedoff, m249, negev)
markup_heavy_ru.add(back_button_alt_3_ru)