import email
import imaplib
import threading

from PySide2 import QtCore, QtWidgets, QtMultimedia
from telethon.sync import TelegramClient

from controllers.c_main import CMain
from models.config_data import ConfigData
from models.my_email import MyEmail
from windows.app_main_window import AppMainWindow


class App(QtWidgets.QApplication):
    signal_new_emails_obtained = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_data = ConfigData()
        self.gui = AppMainWindow()
        self.c_main = CMain(self, self.gui)
        self.client = None
        self.telegram_client_connected = False
        self.email_count = 0
        self.old_emails = set()
        self.new_emails = set()
        self.get_emails_error = None
        self.conected_with_email = False
        self.timer_get_new_emails = QtCore.QTimer()
        self.timer_get_new_emails.setSingleShot(False)
        self.timer_get_new_emails.timeout.connect(self._get_emails)
        self.signal_new_emails_obtained.connect(self._check_new_emails)
        self.player = QtMultimedia.QMediaPlayer(self.gui, QtMultimedia.QMediaPlayer.LowLatency)
        self.player.setMedia(QtCore.QUrl('resources/alarm.mp3'))
        self.player.mediaStatusChanged.connect(self._repeat_alarm)

        self.gui.connect_signals(self.c_main)
        self._setup_app()
        self.run_flananini()

    def _check_new_emails(self):
        if self.get_emails_error:
            self.conected_with_email = False
            self.gui.text_log.append(self.get_emails_error)
        elif not self.conected_with_email:
            self.conected_with_email = True
            self.gui.text_log.append('Conectado con éxito con la cuenta de email.')

        my_emails = {email for email in self.new_emails if email.from_.lower() in self.config_data.emails_to_check}

        if not self.old_emails:
            self.old_emails = my_emails
            return

        new_emails = my_emails - self.old_emails
        self.old_emails = my_emails

        for new_email in new_emails:
            self.email_count += 1
            if self.telegram_client_connected:
                self.client.send_message(self.config_data.send_to, f'''
    NUEVO CORREO
    Despiertame cuando sea necesario, si es que es necesario.
    =================================================
    
    Asunto:
    {new_email._subject}
    
    Contenido:
    {new_email._text or 'Correo vacío'}''', silent=False)
                self.gui.text_log.append(f'Correo enviado a {self.config_data.send_to} ({self.email_count}).')
            else:
                self.gui.text_log.append(f'Correo nuevo ({self.email_count}).')

        if new_emails and self.c_main.alarm_activated and self.player.state() != QtMultimedia.QMediaPlayer.PlayingState:
            self.player.play()

    def _get_emails(self):
        def get_emails():
            self.get_emails_error = None
            imap = imaplib.IMAP4_SSL('imap.outlook.com')
            try:
                imap.login(self.config_data.email_name, self.config_data.email_pass)
            except (AttributeError, imaplib.IMAP4.error) as e:
                self.get_emails_error = 'Error: no se pudo conectar con la cuenta de email.'
                self.signal_new_emails_obtained.emit()
                return

            status, n_messages = imap.select('INBOX')

            n_messages = int(n_messages[0])
            my_emails: set[MyEmail] = set()
            for id_ in range(n_messages, n_messages - self.config_data.n_emails, -1):
                res, msg = imap.fetch(str(id_), '(RFC822)')
                for response in msg:
                    if not isinstance(response, tuple):
                        continue

                    my_email = MyEmail()
                    msg = email.message_from_bytes(response[1])
                    my_email.subject = email.header.decode_header(msg['Subject'])[0][0]
                    try:
                        my_email.from_ = msg['From'].split('<')[1].split('>')[0]
                    except:
                        self.get_emails_error = 'Error: "from" no tiene el formato "<direccion>"'

                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            try:
                                my_email.text = part.get_payload(decode=True).decode()
                            except:
                                my_email.text = part.get_payload()

                    if my_email:
                        my_emails.add(my_email)

            imap.close()
            imap.logout()

            self.new_emails = my_emails
            self.signal_new_emails_obtained.emit()

        thread = threading.Thread(target=get_emails)
        thread.start()

    def _repeat_alarm(self, media_status):
        if media_status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.player.play()

    def _setup_app(self):
        self.setStyle('fusion')

    def run_flananini(self):
        def get_code_from_user():
            dialog = QtWidgets.QInputDialog(self.gui)
            dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
            dialog.setWindowTitle('FlanaNini')
            dialog.setLabelText('Introduce el código recibido en telegram')
            dialog.setOkButtonText('Aceptar')
            dialog.setCancelButtonText('Cancelar')
            dialog.exec_()
            return dialog.textValue()

        try:
            self._get_emails()
            self.timer_get_new_emails.start(self.config_data.period * 1000 * 60)

            if self.client:
                self.client.disconnect()

            self.client = TelegramClient('session', self.config_data.api_id, self.config_data.api_hash)
            self.client.start(self.config_data.phone, code_callback=get_code_from_user)
            self.telegram_client_connected = True
            self.gui.text_log.append('Conectado con éxito con telegram.')
            self.email_count = 0

        except (RuntimeError, ValueError):
            self.telegram_client_connected = False
            self.gui.text_log.append('Sin conectar con telegram. Modo solo alarma.')
        except Exception as e:
            self.gui.text_log.append(f'Error de configuración: {str(e)}')
