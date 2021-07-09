import os.path
from os import listdir
from random import randrange
import utils.utils as utils

from classes import Chain, Wallet, Block


# Simulation de transactions et comportements transverses
def main():

    print('\n*** Simulation de transactions '
          'et comportements transverses ***\n')

    # Initialisation de la chaîne
    print('\n* Initialisation de la chaîne *\n')
    chain = Chain()
    print('--------------------------------')
    print('Dernière transaction :', chain.last_transaction_number)
    print('Liste des blocks :', " -> "
          .join([block.hash for block in chain.blocks]))
    print('--------------------------------')
    input("\nAppuyer sur entrée pour continuer ...")

    # Initialisation de trois Wallets (méthode de génération d'un ID + save)
    path = os.path.join(os.getcwd(), "content\\wallets\\")
    if len(listdir(path)) < 3:
        print('\n* Initialisation de trois Wallets *\n')
        wallet1 = Wallet()
        wallet2 = Wallet()
        wallet3 = Wallet()
        utils.write_wallet_desc([wallet1, wallet2, wallet3])
        input("\nAppuyer sur entrée pour continuer ...")
    # Ou récupération de trois wallets aléatoirement (méthode load)
    else:
        print('\n* Récupération de trois wallets aléatoirement *\n')
        wallets_name = utils.get_wallets_name()
        wallet1 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
        wallet2 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
        wallet3 = Wallet(wallets_name.pop(randrange(len(wallets_name))))
        utils.write_wallet_desc([wallet1, wallet2, wallet3])
        input("\nAppuyer sur entrée pour continuer ...")

    # Initialisation de blocks
    print('\n* Initialisation de blocks *\n')
    path = os.path.join(os.getcwd(), "content\\blocs\\")
    if len(listdir(path)) < 3:
        chain.add_block()
        chain.add_block()
        chain.add_block()

    # Récupération du bloc principal
    print('\n* Récupération du bloc principal *\n')
    block1 = chain.get_block("00")
    utils.write_blocks_desc([block1])
    input("\nAppuyer sur entrée pour continuer ...")

    # Récupération de deux autres blocs aléatoirement
    # (par la chaîne, et par le block directemment)
    print('\n* Récupération de deux autres blocs aléatoirement *\n')
    blocks_hash = utils.get_blocks_hash()
    block2 = chain.get_block(blocks_hash.pop(randrange(len(blocks_hash))))
    block3 = Block(blocks_hash.pop(randrange(len(blocks_hash))))
    utils.write_blocks_desc([block2, block3])
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 0. Récupération du dernier numéro de transaction
    #
    print("\n0.------ "
          "Récupération du dernier numéro de transaction "
          "------\n")
    print("N°", chain.last_transaction_number)
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 1. Transaction classique
    #
    print("\n1. "
          "------ Transaction n°1: "
          "------\n")

    transaction_amount = 10
    transaction = chain.add_transaction(
        block2, wallet1, wallet2, transaction_amount
    )
    utils.write_transaction_desc(
        transaction, wallet1, wallet2, transaction_amount
    )
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 2. Transaction trop importante pour un utilisateur (solde insuffisant)
    #
    print("\n2. ------ "
          "Transaction n°2: solde insuffisant "
          "------\n")
    print("Transaction de 500 tokens".upper())
    print(chain.add_transaction(block2, wallet1, wallet2, 500))
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 3. Surcharge d'un bloc pour tester la limite de place en octets
    #
    print("\n3. ------ "
          "Transaction n°3: place insuffisante "
          "------\n")

    result = None
    expected_response = "Transaction impossible: " \
                        "place non disponible sur le bloc choisi."
    print("// Génération d'un grand nombre de transactions sur le block {} "
          "\\\\\n".format(block1.hash))
    while result != expected_response:
        result = chain.add_transaction(
            block1, wallet1, wallet2, 0)
    print(expected_response)
    print("Poids du block: {} octets".format(block1.get_weight()))
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 4. Transactions avec des wallets invalides
    #
    print("\n4. ------ "
          "Transaction n°4: wallets inexistants "
          "------\n")
    random_wallet = Wallet("Test")
    utils.write_wallet_desc([random_wallet])
    print(chain.add_transaction(block2, random_wallet, wallet2, 500))
    print(chain.add_transaction(block2, wallet1, random_wallet, 500))
    print(chain.add_transaction(block2, random_wallet, random_wallet, 500))
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 5. Deuxième transaction classique avec autre block et wallet
    #
    print("\n5. "
          "------ Transaction n°5: "
          "------\n")
    transaction = chain.add_transaction(
        block3, wallet3, wallet2, transaction_amount
    )
    utils.write_transaction_desc(
        transaction, wallet1, wallet2, transaction_amount
    )
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 6. Reconstruction de la chaine lors de l'initialisation d'un objet Chain
    #
    print("\n6. ------ "
          "Reconstruction de la chaine à chaque initialisation de la chaine "
          "------\n")
    del chain
    chain = Chain()
    print(" -> ".join([block.hash for block in chain.blocks]))
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 7. Récupération du dernier numéro de transaction
    # après réinitilisation de la chaine
    #
    print("\n7. ------ "
          "Récupération du dernier numéro de transaction "
          "------\n")
    print("N°", chain.last_transaction_number)
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 8. Récupération d'un block par le numéro de transaction
    #
    print("\n8. ------ "
          "Récupération d'un block par le numéro de transaction"
          " ------\n")
    print(chain.find_transaction(chain.last_transaction_number))
    print(chain.find_transaction(-1))
    print(chain.find_transaction(chain.last_transaction_number + 1))
    input("\nAppuyer sur entrée pour continuer ...")

    #
    # 9. Récupération d'une transaction par le numéro depuis le block
    #
    print("\n9. ------ "
          "Récupération d'une transaction par le numéro depuis le block"
          " ------\n")
    print(block3.get_transaction(chain.last_transaction_number))
    print(block3.get_transaction(-1))
    print(block3.get_transaction(chain.last_transaction_number + 1))
    input("\nAppuyer sur entrée pour continuer ...")


if __name__ == '__main__':
    main()
