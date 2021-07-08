import uuid
import json
import os.path
from os import listdir
from random import randrange


class Wallet:

    def __init__(self, unique_id=""):
        loaded = self.load(unique_id)

        if not loaded:
            self.unique_id = self.generate_unique_id()
            self.balance = 0
            self.history = []

    def generate_unique_id(self):

        wallets = self.get_wallets_name()
        id = str(uuid.uuid4())
        while id in wallets:
            id = str(uuid.uuid4())
        return id

    def get_wallets_name(self):
        path = os.path.join(os.getcwd(), "content\\wallets\\")
        files = []
        for i, file in enumerate(listdir(path)):
            if not os.path.isdir(path + "\\" + file):
                files.append(os.path.splitext(file)[0])
        return files

    def add_balance(self, balance):
        self.balance += balance

    def sub_balance(self, balance):
        self.balance -= balance

    def send(self):
        pass

    def save(self):
        content = json.dumps(self.__dict__)
        path = os.path.join(os.getcwd(), "content\\wallets\\", self.unique_id + ".json")
        with open(path, "w+") as f:
            f.write(content)
            f.close()

    def load(self, unique_id):
        path = os.path.join(os.getcwd(), "content\\wallets\\", unique_id + ".json")
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = json.loads(f.read())
                f.close()
                for k, v in content.items():
                    setattr(self, k, v)
            return True
        return False
