import uuid
import json
import os.path


class Wallet:

    def __init__(self):
        self.unique_id = self.generate_unique_id()
        self.balance = 0
        self.history = []

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def add_balance(self, balance):
        self.balance += balance

    def sub_balance(self, balance):
        self.balance -= balance

    def send(self):
        pass

    def save(self):
        content = json.dumps(self.__dict__)
        path = os.path.join(os.getcwd(), "content\\wallets\\", self.unique_id)
        with open("{}.json".format(path), "w+") as f:
            f.write(content)
            f.close()
