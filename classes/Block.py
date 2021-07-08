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
            self.save()

    def check_hash(self):
        return self.hash == hashlib.sha256(self.base_hash.encode()).hexdigest()

    def add_transaction(self, number, transmitter, receiver, amount):
        transaction = {"number": number, "transmitter": transmitter.unique_id, "receiver": receiver.unique_id, "amount": amount}
        self.transactions.append(transaction)
        transmitter.history.append(transaction)
        receiver.history.append(transaction)
        return transaction

    def get_transaction(self, num):
        for transaction in self.transactions:
            if str(num) == transaction.number:
                return transaction
        print("Le numéro de transaction renseigné n'existe pas sur ce bloc")
        return False

    def get_weight(self):
        return os.path.getsize(os.path.join(os.getcwd(), "content\\blocs\\", self.hash + ".json"))

    def check_weight(self):
        return self.get_weight() < 256000

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
        return os.path.isfile(path)
