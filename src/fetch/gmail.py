import email
import imaplib
 
'''
class 
'''
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login('avia.tests@gmail.com ', 'kP5tuFzX7R2')
m.select("Inbox")
resp, items = m.search(None, '(FROM "buruki.mailer@buruki.com")')
msgs = [m.fetch(emailid, '(RFC822)')[1][0][1] for emailid in items[0].decode('utf-8').split()]
'''

# pickle.dump(msgs, open('dump.pickle', 'wb'))
'''