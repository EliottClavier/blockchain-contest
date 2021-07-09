import hashlib
import utils.utils as utils

from classes import Block


class Chain:

    def __init__(self):
        # Reconstruction de la chaîne
        self.blocks = self.get_chain()

        # Récupération du dernier numéro de transaction
        self.last_transaction_number = self.get_last_transaction_number()

        # Numéro d'incrémentation pour la génération du hash
        # On le sauvegarde pour éviter de repartir à zéro pour chaque nouveau block
        self.inc_hash = 0

        # On récupère tous les hash déjà utilisés pour les blocs dans un
        # attribut pour éviter de faire appel à la méthode
        # get_blocks_hash() x fois lors de la génération d'un hash
        self.blocks_hash = utils.get_blocks_hash()

    # Méthode de génération de hash unique
    def generate_hash(self):
        while self.verify_hash(
                hashlib.sha256(str(self.inc_hash).encode()).hexdigest()
        ):
            self.inc_hash += 1

        hash = hashlib.sha256(str(self.inc_hash).encode()).hexdigest()
        self.inc_hash += 1
        return hash

    # Méthode de vérification du hash généré (en lien avec generate_hash())
    def verify_hash(self, hash):
        return hash in self.blocks_hash or hash[:4] != "0000"

    # Méthode d'ajout d'un block à la suite de la chaine avec un hash unique
    def add_block(self):
        block = Block(
            self.generate_hash(),
            str(self.inc_hash - 1),
            self.blocks[-1].hash
        )
        self.blocks.append(block)

    # Méthode de récupération de block depuis la chaine
    def get_block(self, hash):
        return Block(hash)

    # Méthode d'ajout de transaction au block choisi entre deux wallets
    # La méthode vérifie la validité des wallets et le solde de l'émetteur
    # Elle fait appel à son homonyme présent dans la classe Block (voir desc)
    # puis réalise l'échange de tokens et la sauvegarde si la réponse du Block est positive
    def add_transaction(self, block, transmitter, receiver, amount):
        # Vérification de la validité des wallets passés en paramètre
        check_transmitter = self.verify_wallet(transmitter.unique_id)
        check_receiver = self.verify_wallet(receiver.unique_id)

        if not check_transmitter and not check_receiver:
            return "Transaction impossible: wallets renseignés inexistants"
        elif not check_transmitter:
            return "Transaction impossible: émetteur inexistant"
        elif not check_receiver:
            return "Transaction impossible: récepteur inexistant"

        # Vérification du solde du wallet émetteur
        if transmitter.balance >= amount:
            transaction = block.add_transaction(
                self.last_transaction_number + 1,
                transmitter, receiver, amount
            )
            # Si la transaction est acceptée sur le bloc (vérification du poids)
            if transaction:
                self.last_transaction_number += 1
                transmitter.send(receiver, amount)
                block.save(), transmitter.save(), receiver.save()
                return transaction
            return "Transaction impossible: " \
                   "place non disponible sur le bloc choisi."
        else:
            return "Transaction impossible: " \
                   "solde insuffisant pour l'utilisateur émetteur."

    # Méthode de vérification de l'existence du wallet renseigné
    def verify_wallet(self, id):
        return id in utils.get_wallets_name()

    # Méthode de recherche de block par numéro de transaction
    def find_transaction(self, num):
        for block in self.blocks:
            for transaction in block.transactions:
                if num == transaction['number']:
                    return block
        return "Aucune transaction pour le numéro {}".format(num)

    # Méthode de recherche du numéro de la dernière transaction effectuée
    def get_last_transaction_number(self):
        number = 0
        for block in self.blocks:
            for transaction in block.transactions:
                if int(transaction['number']) > number:
                    number = int(transaction['number'])
        return number

    # Méthode de reconstruction de la chaîne de blocks
    # Utilisée à l'initialisation de la châine
    def get_chain(self):
        blocks = []
        for block in utils.get_blocks_hash():
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
