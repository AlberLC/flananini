from PySide2 import QtCore, QtGui, QtWidgets

import controllers
from ui_loader import load_ui


class ConfigWindow(QtWidgets.QMainWindow):
    label_api_id: QtWidgets.QLabel
    label_api_hash: QtWidgets.QLabel
    label_phone: QtWidgets.QLabel
    label_email_name: QtWidgets.QLabel
    label_email_pass: QtWidgets.QLabel
    label_emails: QtWidgets.QLabel
    label_period: QtWidgets.QLabel
    label_n_emails: QtWidgets.QLabel
    label_send_to: QtWidgets.QLabel

    line_api_id: QtWidgets.QLineEdit
    line_api_hash: QtWidgets.QLineEdit
    line_phone: QtWidgets.QLineEdit
    line_email_name: QtWidgets.QLineEdit
    line_email_pass: QtWidgets.QLineEdit
    line_send_to: QtWidgets.QLineEdit

    button_add: QtWidgets.QPushButton
    button_delete: QtWidgets.QPushButton
    button_save: QtWidgets.QPushButton
    button_cancel: QtWidgets.QPushButton

    spin_period: QtWidgets.QSpinBox
    spin_n_emails: QtWidgets.QSpinBox

    list_emails: QtWidgets.QListWidget

    def __init__(self):
        super().__init__()
        load_ui('uis/config.ui', self)
        self._setup_view()

    def _setup_view(self):
        self.icon = QtGui.QIcon('resources/logo.png')
        self.setWindowIcon(self.icon)

        self.button_add.setIcon(QtGui.QIcon('resources/plus.png'))
        self.button_add.setIconSize(QtCore.QSize(15, 15))

        self.button_delete.setIcon(QtGui.QIcon('resources/minus.png'))
        self.button_delete.setIconSize(QtCore.QSize(15, 15))

        self.show()

    def connect_signals(self, controller: 'controllers.c_config.CConfig'):
        self.button_add.clicked.connect(lambda: controller.add_item())
        self.button_delete.clicked.connect(lambda: controller.clicked_delete(self.list_emails.currentItem()))
        self.button_save.clicked.connect(controller.clicked_save)
        self.button_cancel.clicked.connect(self.close)
