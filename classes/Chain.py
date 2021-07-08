import hashlib
import os.path
from os import listdir
from classes.Block import Block
from classes.Wallet import Wallet


class Chain:

    def __init__(self):
        self.blocks = self.get_chain()
        self.last_transaction_number = self.get_last_transaction_number()
        self.inc_transaction = self.last_transaction_number + 1
        self.inc_hash = 0

        # On récupère tous les hash déjà utilisés pour les blocs dans una ttribut pour éviter de faire appel à la méthode
        # get_blocks_hash() x fois lors de la génération d'un hash
        self.blocks_hash = self.get_blocks_hash()

    def generate_hash(self):
        while self.verify_hash(hashlib.sha256(str(self.inc_hash).encode()).hexdigest()):
            self.inc_hash += 1

        hash = hashlib.sha256(str(self.inc_hash).encode()).hexdigest()
        self.inc_hash += 1
        return hash

    def verify_hash(self, hash):
        return hash in self.blocks_hash or hash[:4] != "0000"

    def add_block(self):
        block = Block(self.generate_hash(), str(self.inc_hash), self.blocks[-1].hash)
        self.blocks.append(block)

    def get_block(self, hash):
        return Block(hash)

    def add_transaction(self, block, transmitter, receiver, amount):
        if self.verify_wallet(transmitter) and self.verify_wallet(receiver) and block.check_weight():
            transmitter, receiver = Wallet(transmitter), Wallet(receiver)
            if transmitter.balance >= amount:
                block.add_transaction(self.inc_transaction, transmitter, receiver, amount)
                transmitter.send(receiver, amount)
                block.save(), transmitter.save(), receiver.save()
                self.last_transaction_number, self.inc_transaction = self.inc_transaction, self.inc_transaction + 1

    def verify_wallet(self, id):
        return id in self.get_wallets_name()

    def find_transaction(self, num):
        for block in self.blocks:
            for transaction in block:
                if num == transaction.number:
                    return transaction
        return None

    def get_last_transaction_number(self):
        number = 0
        for block in self.blocks:
            for transaction in block.transactions:
                if int(transaction.number) > number:
                    number = int(transaction.number)
        return number

    def get_chain(self):
        blocks = []
        for block in self.get_blocks_hash():
            if block != "00":
                blocks.append(self.get_block(block))

        ordered_blocks = [self.get_block("00")]
        while blocks:
            index = 0
            for i, block in enumerate(blocks):
                if block.parent_hash == ordered_blocks[-1].hash:
                    index = i
                    break

            if index is not None:
                ordered_blocks.append(blocks.pop(index))
        return ordered_blocks

    def get_blocks_hash(self):
        path = os.path.join(os.getcwd(), "content\\blocs\\")
        files = []
        for i, file in enumerate(listdir(path)):
            if not os.path.isdir(path + "\\" + file):
                files.append(os.path.splitext(file)[0])
        return files

    def get_wallets_name(self):
        path = os.path.join(os.getcwd(), "content\\wallets\\")
        files = []
        for i, file in enumerate(listdir(path)):
            if not os.path.isdir(path + "\\" + file):
                files.append(os.path.splitext(file)[0])
        return files
