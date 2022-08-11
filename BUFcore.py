import os
import stat
import shutil
import sqlite3
import threading

import BUFgui


def remove_readonly(func, path, _):
    '''Clear the readonly bit and reattempt the removal'''
    os.chmod(path, stat.S_IWRITE)
    func(path)


class FoldersTransfer(threading.Thread):
    def __init__(self, buf_window, reverse):
        super().__init__()

        self.conect = sqlite3.connect("BUFdb.db")
        self.cursor = self.conect.cursor()

        self.buf_window = buf_window
        self.reverse = reverse

        self.current = 0
        self.maximum = 0

        self.gameFolder = self.cursor.execute("SELECT game, backup FROM settings").fetchall()[0][0]
        self.backUpFolder = self.cursor.execute("SELECT game, backup FROM settings").fetchall()[0][1]
        self.deleteCache = self.cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0]

        self.gameFolder = self.gameFolder.replace('/', '\\') + '\\'
        self.backUpFolder = self.backUpFolder.replace('/', '\\') + '\\'


    def exception_checking(self):
        if 'Data' in os.listdir(self.backUpFolder) and not 'Data' in os.listdir(self.gameFolder):
            if 'Interface' in os.listdir(self.gameFolder) and 'WTF' in os.listdir(self.gameFolder):
                self.buf_window.message_handler('reversePath')
                return True

        if self.gameFolder == self.backUpFolder:
            self.buf_window.message_handler('samePath')
            return True

        if not 'Data' in os.listdir(self.gameFolder):
            self.buf_window.message_handler('badGamePath')
            return True

        if not self.reverse and not 'Interface' in os.listdir(self.backUpFolder) or \
           not self.reverse and not 'WTF' in os.listdir(self.backUpFolder):
            self.buf_window.message_handler('badBackUpPath')
            return True


    def number_of_files(self, path):
        all_files = [os.path.join(folders_path, files)
        for folders_path, _, list_files in os.walk(path)
        for files in list_files]

        self.maximum += len(all_files)


    def copy3(self, src, dst, *, follow_symlinks=True):

        self.current += 1
        self.buf_window.progressbar_thread.update_bar(self.current)

        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
        shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
        return dst


    def run(self):
        if self.exception_checking() == True:
            return

        self.buf_window.start_action()

        if self.reverse:
            self.gameFolder, self.backUpFolder = self.backUpFolder, self.gameFolder

        self.folder = os.listdir(self.gameFolder)

        if 'Interface' in self.folder:
            shutil.rmtree(self.gameFolder + 'Interface', onerror=remove_readonly)

        if 'WTF' in self.folder:
            shutil.rmtree(self.gameFolder + 'WTF', onerror=remove_readonly)

        if self.deleteCache[0] == 'True':
            if 'Cache' in self.folder and not self.reverse:
                shutil.rmtree(self.gameFolder + 'Cache', onerror=remove_readonly)

        if self.deleteCache[1] == 'True':
            if 'Errors' in self.folder and not self.reverse:
                shutil.rmtree(self.gameFolder + 'Errors', onerror=remove_readonly)

        if self.deleteCache[2] == 'True':
            if 'Logs' in self.folder and not self.reverse:
                shutil.rmtree(self.gameFolder + 'Logs', onerror=remove_readonly)

        self.number_of_files(self.backUpFolder + 'Interface')
        self.number_of_files(self.backUpFolder + 'WTF')
        self.buf_window.progressbar.configure(maximum=self.maximum)

        shutil.copytree(self.backUpFolder + 'Interface', self.gameFolder + 'Interface', copy_function=self.copy3)
        shutil.copytree(self.backUpFolder + 'WTF', self.gameFolder + 'WTF', copy_function=self.copy3)

        self.buf_window.stop_action()

        return
