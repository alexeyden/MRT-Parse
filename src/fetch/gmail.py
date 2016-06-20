import email
import imaplib
import config


class FetchGmail:

    def __init__(self):
        self.imap = imaplib.IMAP4_SSL(config.gmail_imap)
        self.imap.login(config.gmail_login, config.gmail_password)
        self.imap.select('Inbox')

    def fetch(self, mail):
        return self._fetch(mail, '(UNSEEN)', '(FROM "{0}")'.format(mail))

    def fetch_all(self, mail):
        return self._fetch(mail, '(FROM "{0}")'.format(mail))

    def _fetch(self, mail, *query):
        resp, items = self.imap.search(None, *query)

        messages = []
        for email_id in items[0].decode('utf-8').split():
            msg = self.imap.fetch(email_id, '(RFC822)')[1][0][1].decode('utf-8')
            messages.append(email.message_from_string(msg))

        return messages
