import os.path
from os import listdir
from random import randrange
import utils.utils as utils

from classes import Chain, Wallet, Block

# Initialisation de la chaîne
chain = Chain()

# Initialisation de trois Wallets (méthode de génération d'un ID + save)
path = os.path.join(os.getcwd(), "content\\wallets\\")
if len(listdir(path)) < 3:
    wallet1 = Wallet()
    wallet2 = Wallet()
    wallet3 = Wallet()
# Ou récupération de trois wallets aléatoirement (méthode load)
else:
    wallets_name = utils.get_wallets_name()
    wallet1 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
    wallet2 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
    wallet3 = Wallet(wallets_name.pop(randrange(len(wallets_name))))

# Initialisation de blocks
path = os.path.join(os.getcwd(), "content\\blocs\\")
if len(listdir(path)) < 3:
    chain.add_block()
    chain.add_block()
    chain.add_block()

# Récupération du bloc principal
block1 = chain.get_block("00")

# Récupération de deux autres blocs aléatoirement
# (par la chaîne, et par le block directemment)
blocks_hash = utils.get_blocks_hash()
block2 = chain.get_block(blocks_hash.pop(randrange(len(blocks_hash))))
block3 = Block(blocks_hash.pop(randrange(len(blocks_hash))))

#
# 0. Récupération du dernier numéro de transaction
#
print("\n0.------ "
      "Récupération du dernier numéro de transaction "
      "------\n")
print(chain.last_transaction_number)

#
# 1. Transaction classique
#
print("\n1. "
      "------ Transaction n°1: "
      "------\n")

transaction_amount = 10
print("Transaction de {} tokens".upper().format(transaction_amount))
print("Avant transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance)
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance)

print(
    "\nTransaction :",
    chain.add_transaction(block2, wallet1, wallet2, transaction_amount),
    "\n"
)

print("Après transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance,
      "(-{})".format(transaction_amount))
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance,
      "(+{})".format(transaction_amount))

#
# 2. Transaction trop importante pour un utilisateur (solde insuffisant)
#
print("\n2. ------ "
      "Transaction n°2: solde insuffisant "
      "------\n")
print(chain.add_transaction(block2, wallet1, wallet2, 500))

#
# 3. Surcharge d'un bloc pour tester la limite de place en octets
#
print("\n3. ------ "
      "Transaction n°3: place insuffisante "
      "------\n")

result = None
expected_response = "Transaction impossible: " \
                    "place non disponible sur le bloc choisi."
while result != expected_response:
    result = chain.add_transaction(
        block1, wallet1, wallet2, 0)
print(expected_response)
print("Poids du block: {} octets".format(block1.get_weight()))


#
# 4. Transactions avec des wallets invalides
#
print("\n4. ------ "
      "Transaction n°4: wallet inexistant "
      "------\n")
print(chain.add_transaction(block2, Wallet("Test"), wallet2, 500))
print(chain.add_transaction(block2, wallet1, Wallet("Test"), 500))
print(chain.add_transaction(block2, Wallet("Test"), Wallet("Test"), 500))

#
# 5. Deuxième transaction classique
#
print("\n5. "
      "------ Transaction n°5: "
      "------\n")

print("Transaction de {} tokens".upper().format(transaction_amount))
print("Avant transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance)
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance)

print(
    "\nTransaction :",
    chain.add_transaction(block2, wallet1, wallet2, transaction_amount),
    "\n"
)

print("Après transaction :")
print("Émetteur ->", wallet1.unique_id, "->", wallet1.balance,
      "(-{})".format(transaction_amount))
print("Récepteur ->", wallet2.unique_id, "->", wallet2.balance,
      "(+{})".format(transaction_amount))


#
# 6. Reconstruction de la chaine lors de l'initialisation d'un objet Chain
#
print("\n6. ------ "
      "Reconstruction de la chaine à chaque initialisation de la chaine "
      "------\n")
del chain
chain = Chain()
print(" -> ".join([block.hash for block in chain.blocks]))


#
# 7. Récupération du dernier numéro de transaction
# après réinitilisation de la chaine
#
print("\n7. ------ "
      "Récupération du dernier numéro de transaction "
      "------\n")
print(chain.last_transaction_number)


#
# 8. Récupération d'une transaction par le numéro depuis la chaîne
#
print("\n8. ------ "
      "Récupération d'une transaction par le numéro depuis la chaîne"
      " ------\n")
print(chain.find_transaction(chain.last_transaction_number))
print(chain.find_transaction(-1))
print(chain.find_transaction(chain.last_transaction_number + 1))


#
# 9. Récupération d'une transaction par le numéro depuis le block
#
print("\n9. ------ "
      "Récupération d'une transaction par le numéro depuis le block"
      " ------\n")
print(block2.get_transaction(chain.last_transaction_number))
print(block2.get_transaction(-1))
print(block2.get_transaction(chain.last_transaction_number + 1))
