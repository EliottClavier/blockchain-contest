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