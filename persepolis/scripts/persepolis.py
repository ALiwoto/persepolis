# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
import platform

# finding os platform
os_type = platform.system()

# Don't run persepolis as root!
if os_type == 'Linux' or os_type == 'FreeBSD'  or os_type == 'OpenBSD' or os_type == 'Darwin':
    uid = os.getuid()
    if uid == 0:
        print('Do not run persepolis as root.')
        sys.exit(1)


from persepolis.scripts.newopen import Open
from persepolis.scripts import osCommands
import time
import ast
import argparse
import struct
import json

# initialization
home_address = os.path.expanduser("~")

# persepolis config_folder
if os_type == 'Linux' or os_type == 'FreeBSD'  or os_type == 'OpenBSD':
    config_folder = os.path.join(str(home_address), ".config/persepolis_download_manager")
elif os_type == 'Darwin':
    config_folder = os.path.join(str(home_address), "Library/Application Support/persepolis_download_manager")
elif os_type == 'Windows' :
    config_folder = os.path.join(str(home_address), 'AppData\Local\persepolis_download_manager')

# persepolis tmp folder in /tmp
if os_type != 'Windows':
    user_name_split = home_address.split('/')
    user_name = user_name_split[2]
    persepolis_tmp = '/tmp/persepolis_' + user_name
else:
    persepolis_tmp = os.path.join(str(home_address), 'AppData', 'Local', 'persepolis_tmp')


global lock_file_validation

# if lock_file_validation == True >> not another instanse running , else another instanse of persepolis running
if os_type != 'Windows':
    import fcntl
# persepolis lock file
    lock_file = '/tmp/persepolis_exec_' + user_name + '.lock'

# creating lock file
    fp = open(lock_file, 'w')

    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)

        lock_file_validation = True # Lock file created successfully!
    except IOError:
        lock_file_validation = False # creating lock_file was unsuccessful! So persepolis is still running
else: # for windows
    # pypiwin32 must be installed by pip
    from win32event import CreateMutex
    from win32api import GetLastError
    from winerror import ERROR_ALREADY_EXISTS
    from sys import exit

    handle = CreateMutex(None, 1, 'persepolis_download_manager')

    if GetLastError() == ERROR_ALREADY_EXISTS:
        lock_file_validation = False 
    else:
        lock_file_validation = True

if lock_file_validation: 
    from persepolis.scripts import initialization
    from persepolis.scripts.mainwindow import MainWindow


    if os_type == 'Linux' or os_type == 'FreeBSD'  or os_type == 'OpenBSD': # setting "Persepolis Download Manager" name for this process in linux and bsd 
        try:
            from setproctitle import setproctitle
            setproctitle("persepolis")
        except:
            print("Warning : setproctitle is not installed!")


from PyQt5.QtWidgets import QApplication  
from PyQt5.QtGui import QFont   
from PyQt5.QtCore import QCoreApplication, QSettings
from persepolis.gui.palettes import DarkRedPallete, DarkBluePallete, ArcDarkRedPallete, ArcDarkBluePallete, LightRedPallete, LightBluePallete
from persepolis.scripts.bubble import notifySend
from persepolis.scripts.error_window import ErrorWindow
import traceback



# load persepolis_settings
persepolis_setting = QSettings('persepolis_download_manager', 'persepolis')

class PersepolisApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def setPersepolisStyle(self, style):
        # setting style
        self.persepolis_style = style
        self.setStyle(style)

    def setPersepolisFont(self, font, font_size, custom_font):
        # font and font_size
        self.persepolis_font = font
        self.persepolis_font_size = font_size

        if custom_font == 'yes':
            self.setFont(QFont(font , font_size ))
# color_scheme 
    def setPersepolisColorScheme(self, color_scheme):
        self.persepolis_color_scheme = color_scheme
        if color_scheme == 'Persepolis Dark Red':
            persepolis_dark_red = DarkRedPallete()
            self.setPalette(persepolis_dark_red)
            self.setStyleSheet("QMenu::item:selected {background-color : #d64937 ;color : white} QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")
        elif color_scheme == 'Persepolis Dark Blue':
            persepolis_dark_blue = DarkBluePallete()
            self.setPalette(persepolis_dark_blue)
            self.setStyleSheet("QMenu::item:selected { background-color : #2a82da ;color : white } QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")
        elif color_scheme == 'Persepolis ArcDark Red':
            persepolis_arcdark_red = ArcDarkRedPallete()
            self.setPalette(persepolis_arcdark_red)
            self.setStyleSheet("QMenu::item:selected {background-color : #bf474d ; color : white} QToolTip { color: #ffffff; background-color: #353945; border: 1px solid white; } QPushButton {background-color: #353945  } QTabWidget {background-color : #353945;} QMenu {background-color: #353945 }")

        elif color_scheme == 'Persepolis ArcDark Blue':
            persepolis_arcdark_blue = ArcDarkBluePallete()
            self.setPalette(persepolis_arcdark_blue)
            self.setStyleSheet("QMenu::item:selected {background-color : #5294e2 ; color : white } QToolTip { color: #ffffff; background-color: #353945; border: 1px solid white; } QPushButton {background-color: #353945  } QTabWidget {background-color : #353945;} QMenu {background-color: #353945 }")
        elif color_scheme == 'Persepolis Light Red':
            persepolis_light_red = LightRedPallete()
            self.setPalette(persepolis_light_red)
            self.setStyleSheet("QMenu::item:selected {background-color : #d64937 ;color : white} QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")

        elif color_scheme == 'Persepolis Light Blue':
            persepolis_light_blue = LightBluePallete()
            self.setPalette(persepolis_light_blue)
            self.setStyleSheet("QMenu::item:selected { background-color : #2a82da ;color : white } QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")



# creating  terminal arguments  

parser = argparse.ArgumentParser(description='Persepolis Download Manager')
parser.add_argument('chromium', nargs = '?', default = 'no', help='this switch is used for chrome native messaging in Linux and Mac')
parser.add_argument('--link', action='store', nargs = 1, help='Download link.(Use "" for links)')
parser.add_argument('--referer', action='store', nargs = 1, help='Set an http referrer (Referer). This affects all http/https downloads.  If * is given, the download URI is also used as the referrer.')
parser.add_argument('--cookie', action='store', nargs = 1, help='Cookie')
parser.add_argument('--agent', action='store', nargs = 1, help='Set user agent for HTTP(S) downloads.  Default: aria2/$VERSION, $VERSION is replaced by package version.')
parser.add_argument('--headers',action='store', nargs = 1, help='Append HEADER to HTTP request header. ')
parser.add_argument('--name', action='store', nargs = 1, help='The  file  name  of  the downloaded file. ')
parser.add_argument('--default', action='store_true', help='restore default setting')
parser.add_argument('--clear', action='store_true', help='Clear download list and user setting!')
parser.add_argument('--tray', action='store_true', help="Persepolis is starting in tray icon. It's useful when you want to put persepolis in system's startup.")
parser.add_argument('--parent-window', action='store', nargs = 1, help='this switch is used for chrome native messaging in Windows')
parser.add_argument('--version', action='version', version='Persepolis Download Manager 2.5a0')
args = parser.parse_args()

# Mozilla firefox flashgot will send download information whith terminal arguments(link , referer , cookie , agent , headers , name )
# persepolis plugins (for chromium and chrome and opera and vivaldi and firefox) are using native message host system for 
# sending download information to persepolis.
# see this repo for more information:
#   https://github.com/persepolisdm/Persepolis-WebExtension

# if --execute >> yes  >>> persepolis main window  will starts 
# if --execute >> no >>> persepolis started before!


add_link_dictionary = {}
if args.chromium != 'no' or args.parent_window:

# Platform specific configuration
    if os_type == "Windows":
  # Set the default I/O mode to O_BINARY in windows
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    # Send message to chrome extension
    message = '{"enable": true, "version": "1.85"}'.encode('utf-8')
    sys.stdout.buffer.write((struct.pack('I', len(message))))
    sys.stdout.buffer.write(message)
    sys.stdout.flush()

    

    text_length_bytes = sys.stdin.buffer.read(4)

    # Unpack message length as 4 byte integer.
    text_length = struct.unpack('i', text_length_bytes)[0]

    # Read the text (JSON object) of the message.
    text = sys.stdin.buffer.read(text_length).decode("utf-8")
    if text:
        if not 'url' in text:
            sys.exit(0)

        data = json.loads(text)
        url = str(data['url'])

        if url:
            args.link = str(url)
            if 'referrer' in data.keys():
                args.referer = data['referrer']

            if 'filename' in data.keys() and data['filename'] != '':
                args.name = os.path.basename(str(data['filename']))
                
            if 'useragent' in data.keys():
                args.agent = data['useragent']
                
            if 'cookies' in data.keys():
                args.cookie = data['cookies']

if args.clear:
    status = osCommands.removeDir(str(config_folder))
    if status == 'ok' or status == 'no' :
        print ('Download list cleard!')
    else:
        print("persepolis can't clear download list")

    sys.exit(0)

if args.default:
    persepolis_setting = QSettings('persepolis_download_manager', 'persepolis')
    persepolis_setting.clear()
    persepolis_setting.sync()
    print ('Persepolis restored default')
    sys.exit(0)


if args.link :
    add_link_dictionary ['link'] = "".join(args.link)
    
# if plugins call persepolis, then start persepolis in system tray 
    args.tray = True

if args.referer :
    add_link_dictionary['referer'] = "".join(args.referer)

if args.cookie :
    add_link_dictionary['load-cookies'] = "".join(args.cookie)

if args.agent :
    add_link_dictionary['user-agent'] = "".join(args.agent)

if args.headers :
    add_link_dictionary['header'] = "".join(args.headers)

if args.name :
    add_link_dictionary ['out'] = "".join(args.name)
# when flashgot calls persepolis  then persepolis is creating a request file in /tmp folder . this file contains download information
# persepolis mainwindow checks /tmp for flashgot request file every 2 seconds ( see CheckFlashgot class in mainwindow.py )
# when requset received by CheckFlashgot, a popup window (AddLinkWindow) is coming up and window is getting additional download information from user (port , proxy , ...) and download starts and request file deleted
if ('link' in add_link_dictionary):   
    # adding add_link_dictionary to persepolis-flashgot
    flashgot_file = os.path.join(persepolis_tmp, 'persepolis-flashgot')
    f = open(flashgot_file, "a")
    f.writelines(str(add_link_dictionary) + '\n')
    f.close()
    flashgot_ready = os.path.join(persepolis_tmp, 'persepolis-flashgot-ready')
    osCommands.touch(flashgot_ready)

if args.tray:
    start_in_tray = 'yes'
else:
    start_in_tray = 'no'


def main():
    if lock_file_validation: # if lock_file is existed , it means persepolis is still running! 
    # setting color_scheme and style
    # see palettes.py and setting.py

        persepolis_download_manager = PersepolisApplication(sys.argv)

        # setting organization name and domain and apllication name
        QCoreApplication.setOrganizationName('persepolis_download_manager')
        QCoreApplication.setApplicationName('persepolis')

        # Persepolis setting
        persepolis_download_manager.setting = QSettings()


        # getting user's desired font and style , ... from setting
        custom_font = persepolis_download_manager.setting.value('settings/custom-font')
        font = persepolis_download_manager.setting.value('settings/font')
        font_size = int(persepolis_download_manager.setting.value('settings/font-size'))
        style = persepolis_download_manager.setting.value('settings/style')
        color_scheme = persepolis_download_manager.setting.value('settings/color-scheme')


        persepolis_download_manager.setPersepolisStyle(style)

        persepolis_download_manager.setPersepolisFont(font, font_size, custom_font)

        persepolis_download_manager.setPersepolisColorScheme(color_scheme)

        try:
            mainwindow = MainWindow(start_in_tray, persepolis_download_manager, persepolis_download_manager.setting)
            if start_in_tray == 'yes':
                mainwindow.hide()
            else:
                mainwindow.show()

        except Exception:
            from persepolis.scripts import logger
            error_message = str(traceback.format_exc())
            logger.sendToLog(error_message, "ERROR")

            # Resetting persepolis
            error_window = ErrorWindow(error_message)
            error_window.show()
         
        sys.exit(persepolis_download_manager.exec_())

    else:
        print('persepolis is still running')
    # this section warns user that program is still running and no need to run it again
    # and creating a file to notify mainwindow for showing
        if not('link' in add_link_dictionary):
            show_window_file = os.path.join(persepolis_tmp, 'show-window')
            f = open(show_window_file, 'w')
            f.close()
        sys.exit(0)


