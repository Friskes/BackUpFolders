import ctypes
import locale

localization = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]

infoMessage = 'Greetings! This program was created by Friskes.\n\nThis program is designed for automate the\
 transfer of your backup copy of the "Interface" and "WTF" folders to the game folder and to create a backup\
 copies based on the same folders.\n\nTo work with the program, it is enough to select the correct path to the\
 folder once with the game and a backup copy, which should contain the "Interface" and "WTF" folders.\n\n\
 For subsequent launches the program will remember the entered path if you move the folder with the game or\
 backup to another location, the program will ask you to re enter the correct path.\n\n\
Also, when setting the appropriate settings, the program can automatically delete folders such as\
 "Cache", "Errors", "Logs" from the game folder each time a backup is loaded.'
infoTitle = 'Info'
errorTitle = 'Error'
selectGamePath = 'Select game path'
selectBackUpPath = 'Select backup path'
badGamePath = 'You specified the wrong path to the game directory.'
badBackUpPath = 'You specified the wrong path to the backup directory.'
samePath = 'You have two identical paths.'
reversePath = 'You mixed up the paths.'
autoDeleteFolders = 'To auto delete folders\ncheck the boxes below.'
downloadBackUp = 'Download backup'
createBackUp = 'Create backup'
loading = '      Loading'
creation = '     Creation'
bUpLoaded = ' Backup loaded.'
bUpCreated = 'Backup created.'

if localization == 'ru_RU':

    infoMessage = 'Приветствую! Эта программа была создана Friskes.\n\nДанная программа предназначена для\
 автоматизации переноса вашей резервной копии папок "Interface" и "WTF" в папку с игрой и для создания резервной\
 копии на основе этих же папок.\n\nДля работы с программой достаточно выбрать один раз корректный путь к папке\
 с игрой и резервной копией в которой должны лежать папки "Interface" и "WTF".\n\nДля последующих запусков\
 программа запомнит введённый путь, если вы перенесёте папку с игрой или резервной копией в другое место,\
 программа попросит вас заного ввести корректный путь.\n\n\
Так же при установке соответствующих настроек программа может автоматически удалять такие папки как\
 "Cache", "Errors", "Logs" из папки с игрой при каждой загрузке резервной копии.'
    infoTitle = 'Инфо'
    errorTitle = 'Ошибка'
    selectGamePath = 'Выбрать путь к игре'
    selectBackUpPath = 'Выбрать путь к бэкапу'
    badGamePath = 'Вы указали не верный путь к директории игры.'
    badBackUpPath = 'Вы указали не верный путь к директории бэкапа.'
    samePath = 'Вы указали два одинаковых пути.'
    reversePath = 'Вы перепутали пути местами.'
    autoDeleteFolders = 'Для авто удаления папок\nпоставьте галочки ниже.'
    downloadBackUp = 'Загрузить бэкап'
    createBackUp = 'Создать бэкап'
    loading = '     Загрузка'
    creation = '    Создание'
    bUpLoaded = 'Бэкап загружен.'
    bUpCreated = '  Бэкап создан.'
