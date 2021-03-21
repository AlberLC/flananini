import application
from controllers.c_config import CConfig
from windows.app_main_window import AppMainWindow
from windows.config_window import ConfigWindow


class CMain:
    def __init__(self, app: 'application.App', gui: AppMainWindow):
        self.app = app
        self.gui = gui
        self.alarm_activated = False
        self.config_gui = None
        self.config_controller = None

    def changed_check_alarm(self):
        self.alarm_activated = not self.alarm_activated

    def clicked_config(self):
        self.config_gui = ConfigWindow()
        self.config_controller = CConfig(self.app, self.config_gui)
        self.config_gui.connect_signals(self.config_controller)

    def clicked_stop_alarm(self):
        self.app.player.stop()
