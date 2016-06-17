import pickle
import email


class FetchPickle:
    def __init__(self, dump_file, fetch_size = 3):
        self.dump_file = dump_file
        self.fetch_size = fetch_size

    def fetch(self):
        return self.fetch_all()[-self.fetch_size:]

    def fetch_all(self):
        messages = []

        with open(self.dump_file, 'rb') as f:
            raw_messages = pickle.load(f)

            for msg in raw_messages:
                messages.append(email.message_from_string(msg.decode('utf-8')))

        return messages
