import os, stat
import shutil
import time
import localization as L

PATH = 'path.txt'
PATH2 = 'cache.txt'

def re_entering(key, str):
    if not str == None:
        string = str.replace(r'\\', '\\')

    if key == 'game':
        gameFolder = input(L.enterGamePath2)

        file = open(PATH, 'w')
        file.write(gameFolder + '\\' + '\n')
        file.write(string)
        file.close()

    if key == 'backup':
        backUpFolder = input(L.enterBackUpPath2)

        file = open(PATH, 'w')
        file.write(string + '\n')
        file.write(backUpFolder + '\\')
        file.close()

    if key == 'all':
        gameFolder = input(L.enterGamePath2)
        backUpFolder = input(L.enterBackUpPath2)

        file = open(PATH, 'w')
        file.write(gameFolder + '\\' + '\n')
        file.write(backUpFolder + '\\')
        file.close()
    main()

def starting_settings():
    file = open(PATH, 'r')
    paths = file.readlines() # Прочитать файл и передать текст построчно в переменную в виде списка
    file.close()

    def wrapper():
        print(L.startingMessage)
        message = input(L.autoDeleteFolders)

        if message != '3' and message != '4':
            wrapper()
            return
        if message == '3':
            deleteCache = 'True'
        if message == '4':
            deleteCache = 'False'

        file = open(PATH2, 'w')
        file.write(deleteCache)
        file.close()

    if len(paths) == 0:
        wrapper()

        gameFolder = input(L.enterGamePath1)
        backUpFolder = input(L.enterBackUpPath1)

        file = open(PATH, 'w')
        file.write(gameFolder + '\\' + '\n')
        file.write(backUpFolder + '\\')
        file.close()

    message = input(L.jobOptions)
    if message != '1' and message != '2':
        while message != '1' and message != '2':
            if not message == 'help':
                message = input(L.jobOptions)
            else:
                wrapper()
                message = input(L.jobOptions)

    if message == '1':
        reverse = False
    if message == '2':
        reverse = True

    file = open(PATH2, 'r')
    deleteCache = file.readlines()
    file.close()

    return reverse, deleteCache

def main():
    reverse, deleteCache = starting_settings()

    file = open(PATH, 'r')
    paths = file.readlines()
    file.close()

    gameFolder = paths[0].strip().replace('\\', r'\\')
    backUpFolder = paths[1].replace('\\', r'\\')

    # инвертируем значения переменных, теперь в gameFolder содержаться значения backUpFolder и наоборот
    if reverse:
        gameFolder, backUpFolder = backUpFolder, gameFolder

    if not os.path.exists(gameFolder): # Проверка существования пути к папке
        print(L.badGamePath)
        re_entering('game', backUpFolder)
        return

    if not os.path.exists(backUpFolder):
        print(L.badBackUpPath)
        re_entering('backup', gameFolder)
        return

    if not 'Interface' in os.listdir(backUpFolder) or not 'WTF' in os.listdir(backUpFolder):
        print(L.noFolders)
        re_entering('backup', gameFolder)
        return

    if gameFolder == backUpFolder or backUpFolder == gameFolder:
        print(L.samePath)
        re_entering('all', None)
        return

    folder = os.listdir(gameFolder) # Возвращает список из имён файлов в искомой папке

    def remove_readonly(func, path, _):
        '''Clear the readonly bit and reattempt the removal'''
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if 'Cache' in folder or 'Errors' in folder or 'Logs' in folder or 'Interface' in folder or 'WTF' in folder:

        if ( not reverse and 'Data' in folder ) or ( reverse and 'Data' in os.listdir(backUpFolder) ):
            print(L.deleteStart)
            if 'Interface' in folder:
                shutil.rmtree(gameFolder + 'Interface', onerror=remove_readonly)
            if 'WTF' in folder:
                shutil.rmtree(gameFolder + 'WTF', onerror=remove_readonly)

            if deleteCache == ['True']:
                if 'Cache' in folder:
                    shutil.rmtree(gameFolder + 'Cache', onerror=remove_readonly)
                if 'Errors' in folder:
                    shutil.rmtree(gameFolder + 'Errors', onerror=remove_readonly)
                if 'Logs' in folder:
                    shutil.rmtree(gameFolder + 'Logs', onerror=remove_readonly)
            print(L.deleteEnd)
        else:
            print(L.reversePath)
            if not reverse:
                re_entering('backup', backUpFolder)
            if reverse:
                re_entering('backup', gameFolder)
    else:
        print(L.foldersMissing)

    while True:
        if 'Interface' and 'WTF' not in os.listdir(gameFolder):
            print(L.copyStart)
            shutil.copytree(backUpFolder + 'Interface', gameFolder + 'Interface')
            shutil.copytree(backUpFolder + 'WTF', gameFolder + 'WTF')
            print(L.copyEnd)
            break
    time.sleep(2)

if __name__ == '__main__':
    main()
