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
#

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
import os
from persepolis.gui import icons_resource
from persepolis.scripts import osCommands
import platform

os_type = platform.system()

home_address = os.path.expanduser("~")

# config_folder
if os_type == 'Linux' or os_type == 'FreeBSD' or os_type == 'OpenBSD':
    config_folder = os.path.join(
        str(home_address), ".config/persepolis_download_manager")
elif os_type == 'Darwin':
    config_folder = os.path.join(
        str(home_address), "Library/Application Support/persepolis_download_manager")
elif os_type == 'Windows':
    config_folder = os.path.join(
        str(home_address), 'AppData', 'Local', 'persepolis_download_manager')


class ErrorWindow(QWidget):
    def __init__(self, text):
        super().__init__()
# finding windows_size
        self.setMinimumSize(QtCore.QSize(363, 300))
        self.setWindowIcon(QIcon.fromTheme('persepolis', QIcon(':/persepolis.svg')))
        self.setWindowTitle('Persepolis Download Manager')

        verticalLayout = QVBoxLayout(self)
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addStretch(1)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.insertPlainText(text)

        verticalLayout.addWidget(self.text_edit)

        self.label2 = QLabel(self)
        self.label2.setText('Reseting persepolis may solving problem.\nDo not panic!If you add your download links again,\npersepolis will resume your downloads\nPlease copy this error message and press "Report Issue" button\nand open a new issue in Github for it.\nWe answer you as soon as possible. \nreporting this issue help us to improve persepolis.\nThank you!')
        verticalLayout.addWidget(self.label2)

        self.report_pushButton = QPushButton(self)
        self.report_pushButton.setText("Report Issue")
        horizontalLayout.addWidget(self.report_pushButton)

        self.reset_persepolis_pushButton = QPushButton(self)
        self.reset_persepolis_pushButton.clicked.connect(
            self.resetPushButtonPressed)
        self.reset_persepolis_pushButton.setText('Reset Persepolis')
        horizontalLayout.addWidget(self.reset_persepolis_pushButton)

        self.close_pushButton = QPushButton(self)
        self.close_pushButton.setText('close')
        horizontalLayout.addWidget(self.close_pushButton)

        verticalLayout.addLayout(horizontalLayout)

        self.report_pushButton.clicked.connect(self.reportPushButtonPressed)
        self.close_pushButton.clicked.connect(self.closePushButtonPressed)

    def reportPushButtonPressed(self, button):
        osCommands.xdgOpen('https://github.com/persepolisdm/persepolis/issues')

    def closePushButtonPressed(self, button):
        self.close()

    def resetPushButtonPressed(self, button):
        osCommands.removeDir(str(config_folder))
