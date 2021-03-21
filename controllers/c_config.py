from PySide2 import QtWidgets, QtCore

import application
from windows.config_window import ConfigWindow


class CConfig:
    def __init__(self, app: 'application.App', gui: ConfigWindow):
        self.app = app
        self.gui = gui

        self._load_config_data()

    def _load_config_data(self):
        self.gui.line_api_id.setText(self.app.config_data.api_id)
        self.gui.line_api_hash.setText(self.app.config_data.api_hash)
        self.gui.line_phone.setText(self.app.config_data.phone)
        self.gui.line_email_name.setText(self.app.config_data.email_name)
        self.gui.line_email_pass.setText(self.app.config_data.email_pass)
        self.gui.spin_period.setValue(self.app.config_data.period)
        self.gui.spin_n_emails.setValue(self.app.config_data.n_emails)
        self.gui.line_send_to.setText(self.app.config_data.send_to)
        for email_to_check in self.app.config_data.emails_to_check:
            self.add_item(email_to_check)

    def add_item(self, text='-'):
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.gui.list_emails.addItem(item)

    def clicked_delete(self, current_item):
        if current_item is None:
            row = self.gui.list_emails.count() - 1
        else:
            row = self.gui.list_emails.row(current_item)
        self.gui.list_emails.takeItem(row)

    def clicked_save(self):
        self.app.config_data.save_config(
            self.gui.line_api_id.text(),
            self.gui.line_api_hash.text(),
            self.gui.line_phone.text(),
            self.gui.line_email_name.text(),
            self.gui.line_email_pass.text(),
            self.gui.spin_period.value(),
            self.gui.spin_n_emails.value(),
            self.gui.line_send_to.text(),
            [self.gui.list_emails.item(i).text() for i in range(self.gui.list_emails.count())]
        )

        self.gui.close()
        self.app.run_flananini()
