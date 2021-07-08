from classes.Wallet import Wallet
from classes.Block import Block

wallet = Wallet()
wallet2 = Wallet()

block = Block("00")
print(block.hash)
block.add_transaction(wallet, wallet2, 10)
print(block.transactions, block.get_transaction(0))
print(block.get_weight())
block.save()
