import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import threading
import time

import localization as L
import BUFcore


class BUFwindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.conect = sqlite3.connect("BUFdb.db")
        self.cursor = self.conect.cursor()

        self.title("Back Up Folders")
        self.resizable(height=False, width=True)
        self.iconphoto(True, tk.PhotoImage(file=('gear20x20.png')))

        screenwidth = (self.winfo_screenwidth() // 2) - 260
        screenheight = (self.winfo_screenheight() // 2) - 140
        self.geometry('480x176+{}+{}'.format(screenwidth, screenheight))

        self.select_game_path_btn = tk.Button(self, text=L.selectGamePath, bg="grey", fg="white", width=18,
                                              cursor="hand2", command=lambda: self.select_path_btn_click('game'))
        self.select_game_path_btn.grid(column=0, row=0, padx=10, pady=10, sticky=tk.NW)

        self.select_backup_path_btn = tk.Button(self, text=L.selectBackUpPath, bg="grey", fg="white", width=18,
                                                cursor="hand2", command=lambda: self.select_path_btn_click('backup'))
        self.select_backup_path_btn.grid(column=0, row=1, padx=10, pady=0, sticky=tk.NW)

        self.download_backup_btn = tk.Button(self, text=L.downloadBackUp, bg="grey", fg="white",
                                             width=13, cursor="hand2", command=lambda: self.start_folders_transfer(False))
        self.download_backup_btn.grid(column=0, row=2, padx=370, pady=12, sticky=tk.NW)

        self.create_backup_btn = tk.Button(self, text=L.createBackUp, bg="grey", fg="white",
                                           width=13, cursor="hand2", command=lambda: self.start_folders_transfer(True))
        self.create_backup_btn.grid(column=0, row=3, padx=370, pady=0, sticky=tk.NW)

        self.info_title_btn = tk.Button(self, text=L.infoTitle, bg="grey", fg="white",
                                        cursor="hand2", command=lambda: self.message_handler('infoMessage'))
        self.info_title_btn.grid(column=0, row=2, padx=255, pady=12, sticky=tk.NW)

        self.auto_delete_folders_lbl = tk.Label(self, text=L.autoDeleteFolders, font=("Arial Bold", 11))
        self.auto_delete_folders_lbl.grid(column=0, row=2, padx=7, pady=5, sticky=tk.NW)

        self.dynamic_text_lbl = tk.Label(self, text=None, font=("Arial Bold", 12))
        self.dynamic_text_lbl.grid(column=0, row=3, padx=243, pady=0, sticky=tk.NW)

        self.game_path_lbl = tk.Label(self, text=None, font=("Arial Bold", 11), bg="white", relief="groove")
        self.game_path_lbl.grid(column=0, row=0, padx=147, pady=12, sticky=tk.NW)

        self.backup_path_lbl = tk.Label(self, text=None, font=("Arial Bold", 11), bg="white", relief="groove")
        self.backup_path_lbl.grid(column=0, row=1, padx=147, pady=2, sticky=tk.NW)

        self.game_path_lbl.configure(text=self.cursor.execute("SELECT game, backup FROM settings").fetchall()[0][0])
        self.backup_path_lbl.configure(text=self.cursor.execute("SELECT game, backup FROM settings").fetchall()[0][1])

        self.cache_chk_btn_state = tk.BooleanVar()
        self.cache_chk_btn_state.set(self.cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][0])

        self.cache_chk_btn = tk.Checkbutton(self, text='Cache', var=self.cache_chk_btn_state, relief='groove',
                                            cursor="hand2", command=lambda: self.folders_chk_btn_save('cache'))
        self.cache_chk_btn.grid(column=0, row=3, padx=6, pady=0, sticky=tk.NW)

        self.errors_chk_btn_state = tk.BooleanVar()
        self.errors_chk_btn_state.set(self.cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][1])

        self.errors_chk_btn = tk.Checkbutton(self, text='Errors', var=self.errors_chk_btn_state, relief='groove',
                                             cursor="hand2", command=lambda: self.folders_chk_btn_save('errors'))
        self.errors_chk_btn.grid(column=0, row=3, padx=96, pady=0, sticky=tk.NW)

        self.logs_chk_btn_state = tk.BooleanVar()
        self.logs_chk_btn_state.set(self.cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][2])

        self.logs_chk_btn = tk.Checkbutton(self, text='Logs', var=self.logs_chk_btn_state, relief='groove',
                                           cursor="hand2", command=lambda: self.folders_chk_btn_save('logs'))
        self.logs_chk_btn.grid(column=0, row=3, padx=186, pady=0, sticky=tk.NW)

        self.progressbar_style = ttk.Style()
        self.progressbar_style.theme_use('default')
        self.progressbar_style.configure(style="grey.Horizontal.TProgressbar", background='grey')

        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=470,
                                           style='grey.Horizontal.TProgressbar', mode="determinate", maximum=1000)
        self.progressbar.grid(column=0, row=4, padx=5, pady=5, sticky=tk.NW)

        self.mainloop()


    def select_path_btn_click(self, path_type):
        if path_type == 'game':
            directory = filedialog.askdirectory(title=L.selectGamePath)
        elif path_type == 'backup':
            directory = filedialog.askdirectory(title=L.selectBackUpPath)

        if not directory == '':
            if path_type == 'game':
                self.game_path_lbl.configure(text=directory)
            elif path_type == 'backup':
                self.backup_path_lbl.configure(text=directory)

            self.cursor.execute(f"UPDATE settings SET {path_type} = '{directory}'")
            self.conect.commit()


    def folders_chk_btn_save(self, folder_name):
        if folder_name == 'cache':
            self.cursor.execute(f"UPDATE settings SET {folder_name} = '{self.cache_chk_btn_state.get()}'")
        elif folder_name == 'errors':
            self.cursor.execute(f"UPDATE settings SET {folder_name} = '{self.errors_chk_btn_state.get()}'")
        elif folder_name == 'logs':
            self.cursor.execute(f"UPDATE settings SET {folder_name} = '{self.logs_chk_btn_state.get()}'")

        self.conect.commit()


    def message_handler(self, msg_type):
        if msg_type == 'infoMessage':
            messagebox.showinfo(L.infoTitle, L.infoMessage)
        if msg_type == 'reversePath':
            messagebox.showerror(L.errorTitle, L.reversePath)
        if msg_type == 'badGamePath':
            messagebox.showerror(L.errorTitle, L.badGamePath)
        if msg_type == 'badBackUpPath':
            messagebox.showerror(L.errorTitle, L.badBackUpPath)
        if msg_type == 'samePath':
            messagebox.showerror(L.errorTitle, L.samePath)


    def start_folders_transfer(self, reverse):
        self.reverse = reverse
        BUFcore.FoldersTransfer(self, self.reverse).start()


    def start_action(self):
        self.select_game_path_btn.configure(state=tk.DISABLED)
        self.select_backup_path_btn.configure(state=tk.DISABLED)
        self.cache_chk_btn.configure(state=tk.DISABLED)
        self.errors_chk_btn.configure(state=tk.DISABLED)
        self.logs_chk_btn.configure(state=tk.DISABLED)
        self.download_backup_btn.configure(state=tk.DISABLED)
        self.create_backup_btn.configure(state=tk.DISABLED)

        self.progressbar.configure(value=0)
        self.progressbar_style.configure(style="grey.Horizontal.TProgressbar", background='grey')

        self.progressbar_thread = AsyncAction_ProgressBar(self.progressbar)
        self.progressbar_thread.start()

        self.dynamictext_thread = AsyncAction_DynamicText(self.reverse, self.dynamic_text_lbl)
        self.dynamictext_thread.start()


    def stop_action(self):
        self.dynamictext_thread.stop()

        self.select_game_path_btn.configure(state=tk.NORMAL)
        self.select_backup_path_btn.configure(state=tk.NORMAL)
        self.cache_chk_btn.configure(state=tk.NORMAL)
        self.errors_chk_btn.configure(state=tk.NORMAL)
        self.logs_chk_btn.configure(state=tk.NORMAL)
        self.download_backup_btn.configure(state=tk.NORMAL)
        self.create_backup_btn.configure(state=tk.NORMAL)

        self.progressbar_style.configure(style="grey.Horizontal.TProgressbar", background='green')


class AsyncAction_ProgressBar(threading.Thread):
    def __init__(self, progressbar):
        super().__init__()

        self.progressbar = progressbar

    def update_bar(self, current):
        self.progressbar.configure(value=current)
        self.progressbar.update()


class AsyncAction_DynamicText(threading.Thread):
    def __init__(self, reverse, dynamic_text_lbl):
        super().__init__()

        self.reverse = reverse
        self.dynamic_text_lbl = dynamic_text_lbl
        self.flag = True

    def run(self):

        while self.flag:
            for dot in ('   ', '•  ', '•• ', '•••'):

                if not self.flag:
                    break

                if self.reverse == True:
                    self.dynamic_text_lbl.configure(text=L.creation + dot)
                elif self.reverse == False:
                    self.dynamic_text_lbl.configure(text=L.loading + dot)

                time.sleep(0.15)
        else:
            if self.reverse == True:
                self.dynamic_text_lbl.configure(text=L.bUpCreated)
            elif self.reverse == False:
                self.dynamic_text_lbl.configure(text=L.bUpLoaded)

    def stop(self):
        self.flag = False


BUFwindow()
