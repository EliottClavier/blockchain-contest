import hashlib
import os
import json


class Block:

    def __init__(self, hash, base_hash=None, parent_hash=None):

        loaded = self.load(hash)

        if not loaded:
            self.base_hash = base_hash
            self.hash = hash
            self.parent_hash = parent_hash
            self.transactions = []

    def check_hash(self):
        return self.hash == hashlib.sha256(self.base_hash.encode()).hexdigest()

    def add_transaction(self, transmitter, receiver, amount):
        self.transactions.append({"transmitter": transmitter.unique_id, "receiver": receiver.unique_id, "amount": amount})

    def get_transaction(self, num):
        return self.transactions[num] if len(self.transactions) > num else print("Le numéro de transaction renseigné n'existe pas;")

    def get_weight(self):
        return os.path.getsize(os.path.join(os.getcwd(), "content\\blocs\\", self.hash + ".json"))

    def save(self):
        content = json.dumps(self.__dict__)
        path = os.path.join(os.getcwd(), "content\\blocs\\", self.hash + ".json")
        with open(path, "w+") as f:
            f.write(content)
            f.close()

    def load(self, hash):
        path = os.path.join(os.getcwd(), "content\\blocs\\", hash + ".json")
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = json.loads(f.read())
                f.close()
                for k, v in content.items():
                    setattr(self, k, v)
            return True
        return False