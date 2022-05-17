import locale
import ctypes

windll = ctypes.windll.kernel32
windll.GetUserDefaultUILanguage()
localization = locale.windows_locale[windll.GetUserDefaultUILanguage()]

startingMessage = 'Greetings!\n\nThis script is designed to automate the transfer of your backup copy\
 of the "Interface" and "WTF" folders to the game folder.\nTo work with the script, it is enough to enter once\
 the correct path to the folder with the game and the backup copy\nin which folders "Interface" and "WTF" should lie.\
 For subsequent runs, the script will remember the entered path\nif you transfer folder with the game or\
 backup to another location, the script will ask you to re-enter the correct path.\n\
Also, the script can automatically delete the "Cache", "Errors", "Logs" folders from the game folder every time it is launched.\
\n\nby Friskes.\n'
enterGamePath1 = 'Enter the path to the game:\n'
enterBackUpPath1 = 'Enter the path to the backup:\n'
enterGamePath2 = 'Enter the correct path to the game:\n'
enterBackUpPath2 = 'Enter the correct path to the backup:\n'
badGamePath = '[!] You specified the wrong path to the game directory.'
badBackUpPath = '[!] You specified the wrong path to the backup directory.'
noFolders = '[!] No backup folders found for this path.'
samePath = '[!] You have two identical paths.'
deleteStart = 'I start deleting..'
deleteEnd = 'Removal completed!'
reversePath = '[!] You mixed up the paths.'
foldersMissing = 'There are no folders to delete.'
copyStart = 'I start to copy..'
copyEnd = 'Copy completed!'
autoDeleteFolders = 'To automatically delete the folders "Cache", "Errors", "Logs" enter: 3\nTo disable this function, enter: 4\n'
jobOptions = 'To download a backup, enter: 1\nTo create a backup, enter: 2\nFor information, enter: help\n'

if localization == 'ru_RU':

    startingMessage = 'Приветствую!\n\nДанный скрипт предназначен для автоматизации переноса вашей резервной копии\
 папок "Interface" и "WTF" в папку с игрой.\nДля работы со скриптом достаточно ввести один раз\
 корректный путь к папке с игрой и резервной копией в которой\nдолжны лежать папки "Interface" и "WTF".\
 Для последующих запусков скрипт запомнит введённый путь, если вы перенесёте\nпапку с игрой или\
 резервной копией в другое место, скрипт попросит вас заного ввести корректный путь.\n\
Так же скрипт может автоматически удалять папки "Cache", "Errors", "Logs" из папки с игрой при каждом запуске.\
\n\nby Friskes.\n'
    enterGamePath1 = 'Введите путь к игре:\n'
    enterBackUpPath1 = 'Введите путь к бэкапу:\n'
    enterGamePath2 = 'Введите корректный путь к игре:\n'
    enterBackUpPath2 = 'Введите корректный путь к бэкапу:\n'
    badGamePath = '[!] Вы указали не верный путь к директории игры.'
    badBackUpPath = '[!] Вы указали не верный путь к директории бэкапа.'
    noFolders = '[!] По данному пути папок для бэкапа не найдено.'
    samePath = '[!] Вы указали два одинаковых пути.'
    deleteStart = 'Начинаю удалять..'
    deleteEnd = 'Удаление завершено!'
    reversePath = '[!] Вы перепутали пути местами.'
    foldersMissing = 'Папки для удаления отсутствуют.'
    copyStart = 'Начинаю копировать..'
    copyEnd = 'Копирование завершено!'
    autoDeleteFolders = 'Для автоматического удаления папок "Cache", "Errors", "Logs" введите: 3\nДля отключения данной функции введите: 4\n'
    jobOptions = 'Чтобы загрузить бэкап введите: 1\nЧтобы создать бэкап введите: 2\nДля получения информации введите: help\n'
