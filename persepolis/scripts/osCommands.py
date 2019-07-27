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

import os
import platform
import shutil
import subprocess

from persepolis.constants import OS

os_type = platform.system()


def touch(file_path):
    if not(os.path.isfile(file_path)):
        f = open(file_path, 'w')
        f.close()

# xdgOpen opens files or folders


def xdgOpen(file_path):
    if os_type == OS.LINUX or os_type == OS.FREE_BSD or os_type == OS.OPEN_BSD:  # GNU/Linux systems
        subprocess.Popen(['xdg-open', file_path], shell=False)

    elif os_type == OS.DARWIN:  # OS X systems
        subprocess.Popen(['open', file_path], shell=False)

    elif os_type == OS.WINDOWS:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen(['cmd', '/C', 'start', file_path,  file_path],
                         shell=False, creationflags=CREATE_NO_WINDOW)


def remove(file_path):  # remove file with path of file_path
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return 'ok'  # function returns  this , if opertation was successful
        except:
            return 'cant'  # function returns this , if operation was not successful
    else:
        return 'no'  # function returns this , if file is not existed


def removeDir(folder_path):  # removeDir removes folder : folder_path
    if os.path.isdir(folder_path):  # check folder_path existance
        try:
            shutil.rmtree(folder_path)  # remove folder
            return 'ok'
        except:
            return 'cant'  # return 'cant' if removing was not successful
    else:
        return 'no'  # return 'no' if file didn't existed


def makeDirs(folder_path):  # make new folders
    os.makedirs(folder_path, exist_ok=True)

# move downloaded file to another destination.
def moveFile(old_file_path, new_folder_path):
    if os.path.isfile(old_file_path) and os.path.isdir(new_folder_path):
        try:
            shutil.move(old_file_path, new_folder_path) 
            return 1
        except:
            return 0
    else:
        return 0
