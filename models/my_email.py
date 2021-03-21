from dataclasses import dataclass

TRANSLATIONS = {
    '=20': '',
    '=D1': 'Ñ',
    '=F1': 'ñ',
    '=C1': 'Á',
    '=E1': 'á',
    '=C9': 'É',
    '=E9': 'é',
    '=CD': 'Í',
    '=ED': 'í',
    '=D3': 'Ó',
    '=F3': 'ó',
    '=DA': 'Ú',
    '=FA': 'ú',
    '=': ''
}


@dataclass
class MyEmail:
    _subject: str = None
    from_: str = None
    _text: str = None

    def __bool__(self):
        return self._subject is not None or self.from_ is not None or self._text is not None

    def __hash__(self):
        return hash((self._subject, self.from_, self._text))

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        try:
            if isinstance(subject, bytes):
                self._subject = subject.decode()
            else:
                self._subject = subject
        except:
            pass

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        for old, new in TRANSLATIONS.items():
            text = text.replace(old, new)
        self._text = text
