import json
from dataclasses import dataclass


@dataclass
class ConfigData:
    api_id = None
    api_hash = None
    phone = None
    email_name = None
    email_pass = None
    period = None
    n_emails = None
    send_to = None
    emails_to_check = []

    def __init__(self):
        with open('config.json', 'a+') as file:
            file.seek(0)
            text = file.read()
            if not text:
                text = '{}'
                file.write(text)
            config = json.loads(text)

        self.api_id = config.get('api_id')
        self.api_hash = config.get('api_hash')
        self.phone = config.get('phone')
        self.email_name = config.get('email_name')
        self.email_pass = config.get('email_pass')
        self.period = config.get('period', 5)
        self.n_emails = config.get('n_emails', 5)
        self.send_to = config.get('send_to', 'me')
        self.emails_to_check = config.get('emails_to_check', [])

    def __bool__(self):
        return bool(self.api_id and
                    self.api_hash and
                    self.phone and
                    self.email_name and
                    self.email_pass and
                    self.period and
                    self.n_emails and
                    self.send_to and
                    self.emails_to_check)

    def save_config(self, api_id, api_hash, phone, email_name, email_pass, period, n_emails, send_to, emails_to_check):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.email_name = email_name
        self.email_pass = email_pass
        self.period = period
        self.n_emails = n_emails
        self.send_to = send_to
        self.emails_to_check = emails_to_check

        with open('config.json', 'w') as file:
            json.dump(self.__dict__, file)
