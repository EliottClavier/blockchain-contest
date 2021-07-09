import os.path
from os import listdir


# FONCTIONS REUTILISEES PLUSIEURS FOIS DANS LE CODE


# Fonction de récupération des ids des wallets
def get_wallets_name():
    path = os.path.join(os.getcwd(), "content\\wallets\\")
    files = []
    for i, file in enumerate(listdir(path)):
        if not os.path.isdir(path + "\\" + file):
            files.append(os.path.splitext(file)[0])
    return files


# Fonction de récupération des hash des blocks sauf le premier block
def get_blocks_hash():
    path = os.path.join(os.getcwd(), "content\\blocs\\")
    files = []
    for i, file in enumerate(listdir(path)):
        if not os.path.isdir(path + "\\" + file) and file != "00.json":
            files.append(os.path.splitext(file)[0])
    return files


# Fonction d'affichage du détail d'un ou plusieurs wallets
def write_wallet_desc(wallets):
    for wallet in wallets:
        print('--------------------------------')
        print("ID -", wallet.unique_id)
        print("Solde -", wallet.balance, "tokens")
        print("Nombre de transactions -", len(wallet.history))
        print('--------------------------------')


# Fonction d'affichage du détail d'un ou plusieurs blocks
def write_blocks_desc(blocks):
    for block in blocks:
        print('--------------------------------')
        print('Hash -', block.hash)
        print('Base du hash -', block.base_hash)
        print('Cohérence Hash / Base du hash -', block.check_hash())
        print('Parent -', block.parent_hash)
        print("Nombre de transactions -", len(block.transactions))
        print('--------------------------------')


# Fonction d'affichage du détail d'une transaction, avec émetteur et récepteur
# ainsi que le montant
def write_transaction_desc(transaction, transmitter, receiver, amount):
    print("Transaction de {} tokens\n".upper().format(amount))
    print('--------------------------------')
    print("Avant transaction :")
    print("Émetteur ->", transmitter.unique_id, "->", transmitter.balance)
    print("Récepteur ->", receiver.unique_id, "->", receiver.balance)
    print('--------------------------------')

    print("\nTransaction :", transaction, "\n")

    print('--------------------------------')
    print("Après transaction :")
    print("Émetteur ->", transmitter.unique_id, "->", transmitter.balance,
          "(-{})".format(amount))
    print("Récepteur ->", receiver.unique_id, "->", receiver.balance,
          "(+{})".format(amount))
    print('--------------------------------')
