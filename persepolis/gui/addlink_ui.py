# -*- coding: utf-8 -*-
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDateTimeEdit, QDoubleSpinBox, QPushButton, QComboBox, QSpinBox, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QWidget, QFileDialog, QMessageBox, QSizePolicy, QGridLayout, QCheckBox, QFrame, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from persepolis.gui import icons_resource



class AddLinkWindow_Ui(QWidget):
    def __init__(self, persepolis_setting):
        super().__init__()
        self.persepolis_setting = persepolis_setting

        # get icons name
        icons = ':/' + \
            str(self.persepolis_setting.value('settings/icons')) + '/'

        self.setMinimumSize(QtCore.QSize(520, 265))
        self.setWindowIcon(QIcon.fromTheme('persepolis', QIcon(':/persepolis.svg')))

        window_verticalLayout = QVBoxLayout()
        window_verticalLayout.setContentsMargins(-1, 10, -1, -1)


        self.link_frame = QFrame(self)
        self.link_frame.setFrameShape(QFrame.StyledPanel)
        self.link_frame.setFrameShadow(QFrame.Raised)

        horizontalLayout_2 = QHBoxLayout(self.link_frame)

        self.link_verticalLayout = QVBoxLayout()

        # link ->
        self.link_horizontalLayout = QHBoxLayout()
        self.link_label = QLabel(self.link_frame)
        self.link_horizontalLayout.addWidget(self.link_label)

        self.link_lineEdit = QLineEdit(self.link_frame)
        self.link_horizontalLayout.addWidget(self.link_lineEdit)

        self.link_verticalLayout.addLayout(self.link_horizontalLayout)

        horizontalLayout_2.addLayout(self.link_verticalLayout)
        window_verticalLayout.addWidget(self.link_frame)

        # add change_name field ->
        change_name_horizontalLayout = QHBoxLayout()
        self.change_name_checkBox = QCheckBox(self.link_frame)
        change_name_horizontalLayout.addWidget(self.change_name_checkBox)

        self.change_name_lineEdit = QLineEdit(self.link_frame)
        change_name_horizontalLayout.addWidget(self.change_name_lineEdit)

        self.link_verticalLayout.addLayout(change_name_horizontalLayout)

        # add_category ->
        queue_horizontalLayout = QHBoxLayout()

        self.queue_frame = QFrame(self)
        self.queue_frame.setFrameShape(QFrame.StyledPanel)
        self.queue_frame.setFrameShadow(QFrame.Raised)

        add_queue_horizontalLayout = QHBoxLayout(self.queue_frame)

        self.add_queue_label = QLabel(self.queue_frame)
        add_queue_horizontalLayout.addWidget(self.add_queue_label)

        self.add_queue_comboBox = QComboBox(self.queue_frame)
        add_queue_horizontalLayout.addWidget(self.add_queue_comboBox)

        queue_horizontalLayout.addWidget(self.queue_frame)
        queue_horizontalLayout.addStretch(1)

        self.size_label = QLabel(self)
        queue_horizontalLayout.addWidget(self.size_label)

        window_verticalLayout.addLayout(queue_horizontalLayout)

        # options_pushButton
        options_horizontalLayout = QHBoxLayout()

        self.options_pushButton = QPushButton(self)
        self.options_pushButton.setFlat(True)

        options_horizontalLayout.addWidget(self.options_pushButton)

        options_horizontalLayout.addStretch(1)

        window_verticalLayout.addLayout(options_horizontalLayout)

        # proxy ->
        proxy_verticalLayout = QVBoxLayout()

        proxy_horizontalLayout = QHBoxLayout()

        self.proxy_checkBox = QCheckBox(self)
        self.detect_proxy_pushButton = QPushButton(self)
        self.detect_proxy_label = QLabel(self)

        proxy_horizontalLayout.addWidget(self.proxy_checkBox)
        proxy_horizontalLayout.addWidget(self.detect_proxy_label)
        proxy_horizontalLayout.addWidget(self.detect_proxy_pushButton)

        proxy_verticalLayout.addLayout(proxy_horizontalLayout)

        self.proxy_frame = QFrame(self)
        self.proxy_frame.setFrameShape(QFrame.StyledPanel)
        self.proxy_frame.setFrameShadow(QFrame.Raised)

        gridLayout = QGridLayout(self.proxy_frame)

        self.ip_lineEdit = QLineEdit(self.proxy_frame)
        self.ip_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        gridLayout.addWidget(self.ip_lineEdit, 0, 1, 1, 1)

        self.proxy_pass_label = QLabel(self.proxy_frame)
        gridLayout.addWidget(self.proxy_pass_label, 2, 2, 1, 1)

        self.proxy_pass_lineEdit = QLineEdit(self.proxy_frame)
        self.proxy_pass_lineEdit.setEchoMode(QLineEdit.Password)
        gridLayout.addWidget(self.proxy_pass_lineEdit, 2, 3, 1, 1)

        self.ip_label = QLabel(self.proxy_frame)
        gridLayout.addWidget(self.ip_label, 0, 0, 1, 1)

        self.proxy_user_lineEdit = QLineEdit(self.proxy_frame)
        gridLayout.addWidget(self.proxy_user_lineEdit, 0, 3, 1, 1)

        self.proxy_user_label = QLabel(self.proxy_frame)
        gridLayout.addWidget(self.proxy_user_label, 0, 2, 1, 1)

        self.port_label = QLabel(self.proxy_frame)
        gridLayout.addWidget(self.port_label, 2, 0, 1, 1)

        self.port_spinBox = QSpinBox(self.proxy_frame)
        self.port_spinBox.setMaximum(65535)
        self.port_spinBox.setSingleStep(1)
        gridLayout.addWidget(self.port_spinBox, 2, 1, 1, 1)
        proxy_verticalLayout.addWidget(self.proxy_frame)
        window_verticalLayout.addLayout(proxy_verticalLayout)

        # download UserName & Password ->
        download_horizontalLayout = QHBoxLayout()
        download_horizontalLayout.setContentsMargins(-1, 10, -1, -1)

        download_verticalLayout = QVBoxLayout()
        self.download_checkBox = QCheckBox(self)
        download_verticalLayout.addWidget(self.download_checkBox)

        self.download_frame = QFrame(self)
        self.download_frame.setFrameShape(QFrame.StyledPanel)
        self.download_frame.setFrameShadow(QFrame.Raised)

        gridLayout_2 = QGridLayout(self.download_frame)

        self.download_user_lineEdit = QLineEdit(self.download_frame)
        gridLayout_2.addWidget(self.download_user_lineEdit, 0, 1, 1, 1)

        self.download_user_label = QLabel(self.download_frame)
        gridLayout_2.addWidget(self.download_user_label, 0, 0, 1, 1)

        self.download_pass_label = QLabel(self.download_frame)
        gridLayout_2.addWidget(self.download_pass_label, 1, 0, 1, 1)

        self.download_pass_lineEdit = QLineEdit(self.download_frame)
        self.download_pass_lineEdit.setEchoMode(QLineEdit.Password)
        gridLayout_2.addWidget(self.download_pass_lineEdit, 1, 1, 1, 1)
        download_verticalLayout.addWidget(self.download_frame)
        download_horizontalLayout.addLayout(download_verticalLayout)

        # select folder ->
        self.folder_frame = QFrame(self)
        self.folder_frame.setFrameShape(QFrame.StyledPanel)
        self.folder_frame.setFrameShadow(QFrame.Raised)

        gridLayout_3 = QGridLayout(self.folder_frame)

        self.download_folder_lineEdit = QLineEdit(self.folder_frame)
        gridLayout_3.addWidget(self.download_folder_lineEdit, 2, 0, 1, 1)

        self.folder_pushButton = QPushButton(self.folder_frame)
        gridLayout_3.addWidget(self.folder_pushButton, 3, 0, 1, 1)
        self.folder_pushButton.setIcon(QIcon(icons + 'folder'))

        self.folder_label = QLabel(self.folder_frame)
        self.folder_label.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout_3.addWidget(self.folder_label, 1, 0, 1, 1)
        download_horizontalLayout.addWidget(self.folder_frame)
        window_verticalLayout.addLayout(download_horizontalLayout)

        # start time ->
        time_limit_horizontalLayout = QHBoxLayout()
        time_limit_horizontalLayout.setContentsMargins(-1, 10, -1, -1)

        start_verticalLayout = QVBoxLayout()
        self.start_checkBox = QCheckBox(self)
        start_verticalLayout.addWidget(self.start_checkBox)

        self.start_frame = QFrame(self)
        self.start_frame.setFrameShape(QFrame.StyledPanel)
        self.start_frame.setFrameShadow(QFrame.Raised)

        horizontalLayout_5 = QHBoxLayout(self.start_frame)

        self.start_time_qDataTimeEdit = QDateTimeEdit(self.start_frame)
        self.start_time_qDataTimeEdit.setDisplayFormat('H:mm')
        horizontalLayout_5.addWidget(self.start_time_qDataTimeEdit)
        
        start_verticalLayout.addWidget(self.start_frame)
        time_limit_horizontalLayout.addLayout(start_verticalLayout)

        # end time ->
        end_verticalLayout = QVBoxLayout()

        self.end_checkBox = QCheckBox(self)
        end_verticalLayout.addWidget(self.end_checkBox)

        self.end_frame = QFrame(self)
        self.end_frame.setFrameShape(QFrame.StyledPanel)
        self.end_frame.setFrameShadow(QFrame.Raised)

        horizontalLayout_6 = QHBoxLayout(self.end_frame)

        self.end_time_qDateTimeEdit = QDateTimeEdit(self.end_frame)
        self.end_time_qDateTimeEdit.setDisplayFormat('H:mm')
        horizontalLayout_6.addWidget(self.end_time_qDateTimeEdit)
 
        end_verticalLayout.addWidget(self.end_frame)
        time_limit_horizontalLayout.addLayout(end_verticalLayout)

        # limit Speed ->
        limit_verticalLayout = QVBoxLayout()

        self.limit_checkBox = QCheckBox(self)
        limit_verticalLayout.addWidget(self.limit_checkBox)

        self.limit_frame = QFrame(self)
        self.limit_frame.setFrameShape(QFrame.StyledPanel)
        self.limit_frame.setFrameShadow(QFrame.Raised)

        horizontalLayout_4 = QHBoxLayout(self.limit_frame)

        self.limit_spinBox = QDoubleSpinBox(self.limit_frame)
        self.limit_spinBox.setMinimum(1)
        self.limit_spinBox.setMaximum(1023)
        horizontalLayout_4.addWidget(self.limit_spinBox)

        self.limit_comboBox = QComboBox(self.limit_frame)
        self.limit_comboBox.addItem("")
        self.limit_comboBox.addItem("")
        horizontalLayout_4.addWidget(self.limit_comboBox)
        limit_verticalLayout.addWidget(self.limit_frame)
        time_limit_horizontalLayout.addLayout(limit_verticalLayout)
        window_verticalLayout.addLayout(time_limit_horizontalLayout)

        # number of connections ->
        connections_horizontalLayout = QHBoxLayout()
        connections_horizontalLayout.setContentsMargins(-1, 10, -1, -1)

        self.connections_frame = QFrame(self)
        self.connections_frame.setFrameShape(QFrame.StyledPanel)
        self.connections_frame.setFrameShadow(QFrame.Raised)

        horizontalLayout_3 = QHBoxLayout(self.connections_frame)
        self.connections_label = QLabel(self.connections_frame)
        horizontalLayout_3.addWidget(self.connections_label)

        self.connections_spinBox = QSpinBox(self.connections_frame)
        self.connections_spinBox.setMinimum(1)
        self.connections_spinBox.setMaximum(16)
        self.connections_spinBox.setProperty("value", 16)
        horizontalLayout_3.addWidget(self.connections_spinBox)
        connections_horizontalLayout.addWidget(self.connections_frame)
        connections_horizontalLayout.addStretch(1)

        window_verticalLayout.addLayout(connections_horizontalLayout)



        # ok cancel download_later buttons ->
        buttons_horizontalLayout = QHBoxLayout()
        buttons_horizontalLayout.addStretch(1)

        self.download_later_pushButton = QPushButton(self)
        self.download_later_pushButton.setIcon(QIcon(icons + 'stop'))

        self.cancel_pushButton = QPushButton(self)
        self.cancel_pushButton.setIcon(QIcon(icons + 'remove'))

        self.ok_pushButton = QPushButton(self)
        self.ok_pushButton.setIcon(QIcon(icons + 'ok'))

        buttons_horizontalLayout.addWidget(self.download_later_pushButton)
        buttons_horizontalLayout.addWidget(self.cancel_pushButton)
        buttons_horizontalLayout.addWidget(self.ok_pushButton)

        window_verticalLayout.addLayout(buttons_horizontalLayout)
        
        self.setLayout(window_verticalLayout)

        # labels ->
        self.setWindowTitle("Enter Your Link")

        self.link_label.setText("Download Link : ")

        self.add_queue_label.setText("Add to category : ")

        self.change_name_checkBox.setText("Change File Name : ")

        self.options_pushButton.setText("Show more options")

        self.detect_proxy_pushButton.setText("Detect system proxy setting")
        self.proxy_checkBox.setText("Proxy")
        self.proxy_pass_label.setText("Proxy PassWord : ")
        self.ip_label.setText("IP : ")
        self.proxy_user_label.setText("Proxy UserName : ")
        self.port_label.setText("Port:")

        self.download_checkBox.setText("Download UserName and PassWord")
        self.download_user_label.setText("Download UserName : ")
        self.download_pass_label.setText("Download PassWord : ")

        self.folder_pushButton.setText("Change Download Folder")
        self.folder_label.setText("Download Folder : ")

        self.start_checkBox.setText("Start Time")
        self.end_checkBox.setText("End Time")

        self.limit_checkBox.setText("Limit Speed")
        self.limit_comboBox.setItemText(0, "KB/S")
        self.limit_comboBox.setItemText(1, "MB/S")

        self.connections_label.setText("Number Of Connections :")

        self.cancel_pushButton.setText("Cancel")
        self.ok_pushButton.setText("OK")

        self.download_later_pushButton.setText("Download later")

    def changeIcon(self, icons):
        icons = ':/' + str(icons) + '/'

        self.folder_pushButton.setIcon(QIcon(icons + 'folder'))
        self.download_later_pushButton.setIcon(QIcon(icons + 'stop'))
        self.cancel_pushButton.setIcon(QIcon(icons + 'remove'))
        self.ok_pushButton.setIcon(QIcon(icons + 'ok'))
