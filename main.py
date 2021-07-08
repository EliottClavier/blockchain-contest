import os.path
from os import listdir
from random import randrange
import utils.utils as utils

from classes import Chain, Wallet, Block

# Initialisation de la chaîne
chain = Chain()

# Initialisation de trois Wallets
path = os.path.join(os.getcwd(), "content\\wallets\\")
if len(listdir(path)) < 4:
    wallet1 = Wallet()
    wallet2 = Wallet()
    wallet3 = Wallet()
# Ou récupération de trois wallets
else:
    wallets_name = utils.get_wallets_name()
    wallet1 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
    wallet2 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
    wallet3 = Wallet(wallets_name.pop(randrange(len(wallets_name))))

# Initialisation de blocks
path = os.path.join(os.getcwd(), "content\\blocs\\")
if len(listdir(path)) < 4:
    chain.add_block()
    chain.add_block()
    chain.add_block()

# Récupération du bloc principal
block1 = chain.get_block("00")

# Récupération de deux autres blocs
blocks_hash = utils.get_blocks_hash()
block2 = chain.get_block(blocks_hash.pop(randrange(len(blocks_hash))))

# Récupération du dernier numéro de transaction
print("\n0.------------------------- Récupération du dernier numéro de transaction -------------------------\n")
print(chain.last_transaction_number)

# Transaction classique
print("\n1. ------------------------- Transaction n°1: -------------------------\n")
transaction_amount = 10
print("Avant transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance)
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance)
print("\nTransaction :", chain.add_transaction(block2, wallet1, wallet2, transaction_amount), "\n")
print("Après transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance, "(-{})".format(transaction_amount))
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance, "(+{})".format(transaction_amount))

# Transaction trop importante pour un utilisateur (solde insuffisant)
print("\n2. ------------------------- Transaction n°2: solde insuffisant -------------------------\n")
print(chain.add_transaction(block2, wallet1, wallet2, 500))

# Surcharge d'un bloc pour tester la limite de place en octets
print("\n3. ------------------------- Transaction n°3: place insuffisante -------------------------\n")
result = None
while result != "Transaction impossible: place non disponible sur le bloc choisi.":
    result = chain.add_transaction(block1, wallet1, wallet2, transaction_amount)
    result = chain.add_transaction(block1, wallet2, wallet1, transaction_amount)
print(result)

# Reconstruction de la chaine lors de l'initialisation d'un objet Chain
print("\n4. ------------------------- Reconstruction de la chaine à chaque initialisation de la chaine -------------------------\n")
del chain
chain = Chain()
print(" -> ".join([block.hash for block in chain.blocks]))

# Récupération du dernier numéro de transaction après réinitilisation de la chaine
print("\n5. ------------------------- Récupération du dernier numéro de transaction -------------------------\n")
print(chain.last_transaction_number)

# Récupération d'une transaction par le numéro
print("\n6. ------------------------- Récupération d'une transaction par le numéro -------------------------\n")
print(chain.find_transaction(100))
print(chain.find_transaction(-1))
print(chain.find_transaction(chain.last_transaction_number + 1))

