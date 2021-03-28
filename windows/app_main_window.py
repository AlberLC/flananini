import sys

from PySide2 import QtCore, QtGui, QtWidgets

from controllers import c_main
from ui_loader import load_ui


class MenuTextEdit(QtWidgets.QTextEdit):
    def contextMenuEvent(self, e: QtGui.QContextMenuEvent) -> None:
        menu = QtWidgets.QMenu()
        action = QtWidgets.QAction('Limpiar registro')
        menu.addAction(action)
        if menu.exec_(e.globalPos()) == action:
            self.clear()


class AppMainWindow(QtWidgets.QMainWindow):
    label_log: QtWidgets.QLabel

    button_config: QtWidgets.QPushButton
    button_alarm: QtWidgets.QPushButton

    check_alarm: QtWidgets.QCheckBox

    text_log: QtWidgets.QTextEdit

    def __init__(self):
        super().__init__()
        load_ui('uis/main.ui', self, [MenuTextEdit])
        self._setup_view()

    def _setup_view(self):
        self.icon = QtGui.QIcon('resources/logo.png')
        self.setWindowIcon(self.icon)

        self.button_config.setIcon(QtGui.QIcon('resources/config.svg'))
        self.button_config.setIconSize(QtCore.QSize(20, 20))

        self.show()

    def closeEvent(self, event):
        sys.exit(0)

    def connect_signals(self, controller: 'c_main.CMain'):
        self.button_config.clicked.connect(controller.clicked_config)
        self.button_alarm.clicked.connect(controller.clicked_stop_alarm)

        self.check_alarm.stateChanged.connect(controller.changed_check_alarm)
