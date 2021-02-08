# based on: https://github.com/ericwoolard/CS-GO-Update-Notifier

import io
import json
import os
import sys


def save(path, data_str, mode='w'):
    path = ensureAbsPath(path)
    try:
        with io.open(path, mode, encoding='utf-8') as f:
            f.write(str(data_str))
    except IOError:
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError as oserr:
                pass
        if os.path.isdir(directory):
            return save(path, data_str, mode)
        else:
            print(f'Could not write to {path}')
            return False
    else:
        return True


def read(path):
    path = ensureAbsPath(path)
    try:
        fileContents = ''
        with open(path) as f:
            fileContents = f.read()
        return fileContents
    except IOError:
        print(f'Could not find or open file: {path}')
        return False


def ensureAbsPath(path):
    botRootDir = os.path.dirname(os.path.abspath(sys.argv[0])) + '/'
    return path if os.path.isabs(path) else botRootDir + path


def saveJson(path, data):
    return save(
        path,
        json.dumps(
            data,
            ensure_ascii=False,
            indent=4,
            separators=(',', ': ')
        )
    )


def readJson(path):
    f = read(path)
    if f:
        try:
            return json.loads(f)
        except ValueError:
            print(f'Could not parse JSON file: {path}')
            return False
    else:
        return False


def updateJson(path, v, k):
    jsonFile = open(path, 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    tmp = data[k]
    data[k] = v

    jsonFile = open(path, "w+")
    jsonFile.write(json.dumps(data, indent=4))
    jsonFile.close()
