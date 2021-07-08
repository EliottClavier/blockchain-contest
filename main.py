from classes.Wallet import Wallet

wallet = Wallet()
wallet.generate_unique_id()
print(wallet.unique_id)