from classes.Wallet import Wallet

wallet = Wallet("d98510b0-92e5-452c-a38d-8bdefaf6ee8f")
print(wallet.__dict__)

wallet = Wallet("d985108d-8bdefaf6ee8f")
print(wallet.__dict__)

wallet = Wallet()
print(wallet.__dict__)