import uuid


class Wallet:

    unique_id = ""
    balance = 0
    history = []

    def generate_unique_id(self):
        self.unique_id = uuid.uuid4()
