from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Style, Progressbar
import localization as L
from BUFcore import main
import sqlite3

connect = sqlite3.connect("BUFdb.db")
cursor = connect.cursor()

window = Tk()
window.title("Back Up Folders")
window.resizable(height=False, width=True)
window.iconphoto(True, PhotoImage(file=('gear_icon20x20.png')))

# спавним окно при запуске посередине экрана
screenwidth = window.winfo_screenwidth() // 2 - 260 # влево вправо
screenheight = window.winfo_screenheight() // 2 - 140 # вверх вниз
window.geometry('480x176+{}+{}'.format(screenwidth, screenheight))

def button1_click():
    directory = filedialog.askdirectory()

    if not directory == '':
        pathLabel1.configure(text=directory)

        cursor.execute(f"UPDATE settings SET game = '{directory}'")
        connect.commit()

def button2_click():
    directory = filedialog.askdirectory()

    if not directory == '':
        pathLabel2.configure(text=directory)

        cursor.execute(f"UPDATE settings SET backup = '{directory}'")
        connect.commit()

def message_handler(arg=0):
    if arg == 0:
        messagebox.showinfo(L.infoTitle, L.infoMessage)
    if arg == 1:
        messagebox.showerror(L.errorTitle, L.reversePath)
    if arg == 2:
        messagebox.showerror(L.errorTitle, L.badGamePath)
    if arg == 3:
        messagebox.showerror(L.errorTitle, L.badBackUpPath)
    if arg == 4:
        messagebox.showerror(L.errorTitle, L.samePath)

enable = True

def run_main_false():
    global enable
    if enable:
        enable = False
        enable = main(False)

def run_main_true():
    global enable
    if enable:
        enable = False
        enable = main(True)

button1 = Button(window, text=L.selectGamePath, bg="grey", fg="white", width=18, cursor="hand2", command=button1_click)
button1.grid(column=0, row=0, padx=10, pady=10, sticky=NW)

button2 = Button(window, text=L.selectBackUpPath, bg="grey", fg="white", width=18, cursor="hand2", command=button2_click)
button2.grid(column=0, row=1, padx=10, pady=0, sticky=NW)

button3 = Button(window, text=L.downloadBackUp, bg="grey", fg="white", width=13, cursor="hand2", command=run_main_false)
button3.grid(column=0, row=2, padx=370, pady=12, sticky=NW)

button4 = Button(window, text=L.createBackUp, bg="grey", fg="white", width=13, cursor="hand2", command=run_main_true)
button4.grid(column=0, row=3, padx=370, pady=0, sticky=NW)

button5 = Button(window, text=L.infoTitle, bg="grey", fg="white", cursor="hand2", command=message_handler)
button5.grid(column=0, row=2, padx=255, pady=12, sticky=NW)

label1 = Label(window, text=L.autoDeleteFolders, font=("Arial Bold", 11))
label1.grid(column=0, row=2, padx=7, pady=5, sticky=NW)

pathLabel1 = Label(window, text=None, font=("Arial Bold", 11), bg="white", relief="groove")
pathLabel1.grid(column=0, row=0, padx=147, pady=12, sticky=NW)

pathLabel2 = Label(window, text=None, font=("Arial Bold", 11), bg="white", relief="groove")
pathLabel2.grid(column=0, row=1, padx=147, pady=2, sticky=NW)

pathLabel1.configure(text=cursor.execute("SELECT game, backup FROM settings").fetchall()[0][0])
pathLabel2.configure(text=cursor.execute("SELECT game, backup FROM settings").fetchall()[0][1])

def check_button1_save():
    cursor.execute(f"UPDATE settings SET cache = '{check_button1_state.get()}'")
    connect.commit()

def check_button2_save():
    cursor.execute(f"UPDATE settings SET errors = '{check_button2_state.get()}'")
    connect.commit()

def check_button3_save():
    cursor.execute(f"UPDATE settings SET logs = '{check_button3_state.get()}'")
    connect.commit()

check_button1_state = BooleanVar()
check_button1_state.set(cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][0])

check_button1 = Checkbutton(window, text='Cache', var=check_button1_state, relief='groove', cursor="hand2", command=check_button1_save)
check_button1.grid(column=0, row=3, padx=6, pady=0, sticky=NW)

check_button2_state = BooleanVar()
check_button2_state.set(cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][1])

check_button2 = Checkbutton(window, text='Errors', var=check_button2_state, relief='groove', cursor="hand2", command=check_button2_save)
check_button2.grid(column=0, row=3, padx=96, pady=0, sticky=NW)

check_button3_state = BooleanVar()
check_button3_state.set(cursor.execute("SELECT cache, errors, logs FROM settings").fetchall()[0][2])

check_button3 = Checkbutton(window, text='Logs', var=check_button3_state, relief='groove', cursor="hand2", command=check_button3_save)
check_button3.grid(column=0, row=3, padx=186, pady=0, sticky=NW)

statusbar_style = Style()
statusbar_style.theme_use('default')
statusbar_style.configure("grey.Horizontal.TProgressbar", background='grey')

statusbar = Progressbar(window, orient=HORIZONTAL, length=470, style='grey.Horizontal.TProgressbar', mode="determinate")
statusbar.grid(column=0, row=4, padx=5, pady=5, sticky=NW)

def update_statusbar(val):

    statusbar_style.configure("grey.Horizontal.TProgressbar", background='grey')
    if val == 100:
        statusbar_style.configure("grey.Horizontal.TProgressbar", background='green')

    statusbar.configure(value=val)
    statusbar.update()

window.mainloop()
