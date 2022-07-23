import os, stat
import shutil
import BUFgui as gui
import sqlite3

connect = sqlite3.connect("BUFdb.db")
cursor = connect.cursor()

def main(rev):
    reverse = rev

    gameFolder = cursor.execute("SELECT game, backup FROM settings").fetchall()[0][0]
    backUpFolder = cursor.execute("SELECT game, backup FROM settings").fetchall()[0][1]

    gameFolder = gameFolder.replace('/', '\\') + '\\'
    backUpFolder = backUpFolder.replace('/', '\\') + '\\'

    if 'Data' in os.listdir(backUpFolder) and not 'Data' in os.listdir(gameFolder):
        if 'Interface' in os.listdir(gameFolder) and 'WTF' in os.listdir(gameFolder):
            gui.message_handler(1)
            return True

    if not 'Data' in os.listdir(gameFolder):
        gui.message_handler(2)
        return True

    if not reverse and not 'Interface' in os.listdir(backUpFolder) or not reverse and not 'WTF' in os.listdir(backUpFolder):
        gui.message_handler(3)
        return True

    if gameFolder == backUpFolder:
        gui.message_handler(4)
        return True

    deleteCache = cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0]

    # инвертируем значения переменных, теперь в gameFolder содержаться значения backUpFolder и наоборот
    if reverse:
        gameFolder, backUpFolder = backUpFolder, gameFolder

    folder = os.listdir(gameFolder) # Возвращает список из имён файлов в искомой папке

    def remove_readonly(func, path, _):
        '''Clear the readonly bit and reattempt the removal'''
        os.chmod(path, stat.S_IWRITE)
        func(path)

    gui.info_dynamic_text(reverse, 0)
    gui.update_statusbar(14)
    if 'Interface' in folder:
        shutil.rmtree(gameFolder + 'Interface', onerror=remove_readonly)

    gui.update_statusbar(28)
    if 'WTF' in folder:
        shutil.rmtree(gameFolder + 'WTF', onerror=remove_readonly)

    gui.update_statusbar(42)
    if deleteCache[0] == 'True':
        if 'Cache' in folder and not reverse:
            shutil.rmtree(gameFolder + 'Cache', onerror=remove_readonly)

    gui.update_statusbar(56)
    if deleteCache[1] == 'True':
        if 'Errors' in folder and not reverse:
            shutil.rmtree(gameFolder + 'Errors', onerror=remove_readonly)

    gui.update_statusbar(70)
    if deleteCache[2] == 'True':
        if 'Logs' in folder and not reverse:
            shutil.rmtree(gameFolder + 'Logs', onerror=remove_readonly)
    gui.update_statusbar(84)

    shutil.copytree(backUpFolder + 'Interface', gameFolder + 'Interface')
    shutil.copytree(backUpFolder + 'WTF', gameFolder + 'WTF')
    gui.info_dynamic_text(reverse, 1)
    gui.update_statusbar(100)

    return True
