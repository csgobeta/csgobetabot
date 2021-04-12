import re
import numpy as np

DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
DICTIONARY_LENGTH = len(DICTIONARY)
CODE_PATTERN = re.compile(r"CSGO(-[%s]{5}){5}$" % DICTIONARY)


def decode(code):
    if not CODE_PATTERN.match(code):
        data = False
        return data

    else:
        charList = list(re.sub(r"CSGO\-|\-", "", code))
        charList.reverse()
        num = 0
        for c in charList:
            num = num * DICTIONARY_LENGTH + DICTIONARY.index(c)

        byteList = []
        for n in range(0, 144, 8):
            z = (num >> n) & 255
            byteList.append(z)
        byteList.reverse()

        data = sortBytes(byteList)
        return data


def sortBytes(byte):
    data = [byte[10] & 8, byte[13] & 16, byte[13]
            & 32, byte[13] & 64, byte[13] & 128]
    toggle = []
    for v in data:
        if v > 0:
            var = 1
        else:
            var = 0
        toggle.append(var)

    parameters = {
        "cl_crosshairgap": np.int8(byte[2]) / 10.0,
        "cl_crosshair_outlinethickness": byte[3] / 2.0,
        "cl_crosshaircolor_r": byte[4],
        "cl_crosshaircolor_g": byte[5],
        "cl_crosshaircolor_b": byte[6],
        "cl_crosshairalpha": byte[7],
        "cl_crosshair_dynamic_splitdist": byte[8],
        "cl_fixedcrosshairgap": np.int8(byte[9]) / 10.0,
        "cl_crosshaircolor": byte[10] & 6,
        "cl_crosshair_drawoutline": toggle[0],
        "cl_crosshair_dynamic_splitalpha_innermod": ((byte[10] & 240) >> 4) / 10.0,
        "cl_crosshair_dynamic_splitalpha_outermod": (byte[11] & 15) / 10.0,
        "cl_crosshair_dynamic_maxdist_splitratio": ((byte[11] & 240) >> 4) / 10.0,
        "cl_crosshairthickness": (byte[12] & 63) / 10.0,
        "cl_crosshairstyle": (byte[13] & 14) >> 1,
        "cl_crosshairdot": toggle[1],
        "cl_crosshairgap_useweaponvalue": toggle[2],
        "cl_crosshairusealpha": toggle[3],
        "cl_crosshair_t": toggle[4],
        "cl_crosshairsize": (((byte[15] & 31) << 8) + byte[14]) / 10.0
    }

    return parameters

# # # # #


def encode(params):
    values = toList(params)
    num = toNum(values)

    code = ""
    for _ in range(0, 25):
        num, r = divmod(num, DICTIONARY_LENGTH)
        code += DICTIONARY[r]

    return "CSGO-%s-%s-%s-%s-%s" % (code[:5], code[5:10], code[10:15], code[15:20], code[20:])


def toList(params):
    cl_crosshairgap = np.uint8(params["cl_crosshairgap"]*10)
    cl_crosshair_outlinethickness = int(
        params["cl_crosshair_outlinethickness"]*2)
    cl_crosshaircolor_r = int(params["cl_crosshaircolor_r"])
    cl_crosshaircolor_g = int(params["cl_crosshaircolor_g"])
    cl_crosshaircolor_b = int(params["cl_crosshaircolor_b"])
    cl_crosshairalpha = int(params["cl_crosshairalpha"])
    cl_crosshair_dynamic_splitdist = int(
        params["cl_crosshair_dynamic_splitdist"])
    cl_fixedcrosshairgap = np.uint8(params["cl_fixedcrosshairgap"]*10)

    byte1 = 1
    flag = True
    flag2 = True
    flag3 = True

    for i in range(256):
        data = [i & 8, i & 16, i & 32, i & 64, i & 128]
        toggle = []
        for v in data:
            if v > 0:
                var = 1
            else:
                var = 0
            toggle.append(var)

        if (i & 6 == int(params["cl_crosshaircolor"])) and (toggle[0] == int(params["cl_crosshair_drawoutline"])) and (i & 240 == (int(params["cl_crosshair_dynamic_splitalpha_innermod"]*10)) << 4):
            byte10 = i
        if (i & 15 == int(params["cl_crosshair_dynamic_splitalpha_outermod"]*10) and (i & 240 == (int(params["cl_crosshair_dynamic_maxdist_splitratio"]*10)) << 4)):
            byte11 = i
        if (i & 63 == int(params["cl_crosshairthickness"]*10)) and flag:
            byte12 = i
            flag = False
        if (i & 14 == (int(params["cl_crosshairstyle"]) << 1)) and flag2 and toggle[1:] == [int(params["cl_crosshairdot"]), int(params["cl_crosshairgap_useweaponvalue"]), int(params["cl_crosshairusealpha"]), int(params["cl_crosshair_t"])]:
            byte13 = i
            flag2 = False
        for z in range(256):
            if ((((z & 31) << 8) + i) == int(params["cl_crosshairsize"]*10)) and flag3:
                byte14 = i
                byte15 = z
                flag3 = False

        byte16 = 0
        byte17 = 0
    byte0 = byte1 + cl_crosshairgap + cl_crosshair_outlinethickness + cl_crosshaircolor_r + cl_crosshaircolor_g + cl_crosshaircolor_b + \
        cl_crosshairalpha + cl_crosshair_dynamic_splitdist + cl_fixedcrosshairgap + \
        byte10 + byte11 + byte12 + byte13 + byte14 + byte15 + byte16 + byte17
    byte0 = np.uint8(byte0)
    byteList = [byte0, byte1, cl_crosshairgap, cl_crosshair_outlinethickness, cl_crosshaircolor_r, cl_crosshaircolor_g, cl_crosshaircolor_b,
                cl_crosshairalpha, cl_crosshair_dynamic_splitdist, cl_fixedcrosshairgap, byte10, byte11, byte12, byte13, byte14, byte15, byte16, byte17]

    return byteList


def toNum(byteList):
    numHex = ""
    for i in byteList:
        rawHex = hex(i)[2:]
        if len(rawHex) < 2:
            rawHex = "0" + rawHex
        numHex += rawHex
    numHex = "0x" + numHex
    num = int(numHex, 0)

    return num
