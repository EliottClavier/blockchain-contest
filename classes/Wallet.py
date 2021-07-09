import uuid
import json
import os.path
import utils.utils as utils


class Wallet:

    def __init__(self, unique_id=""):
        # Recherche du wallet
        loaded = self.load(unique_id)

        # Si le wallet n'existe pas / qu'un nouveau wallet est instancié
        if not loaded and not unique_id:
            self.unique_id = self.generate_unique_id()
            self.balance = 100
            self.history = []
            self.save()
        # Dans le cas ou le chargement du wallet a échoué
        # (si unique_id a été renseigné), on construit un wallet invalide
        elif not loaded:
            self.unique_id = "INVALIDE"
            self.balance = 0
            self.history = []

    # Méthode de génération d'un ID unique
    def generate_unique_id(self):
        wallets = utils.get_wallets_name()
        id = str(uuid.uuid4())
        while id in wallets:
            id = str(uuid.uuid4())
        return id

    # Méthode d'ajout de tokens sur le solde du wallet
    def add_balance(self, balance):
        self.balance += balance
        self.save()

    # Méthode de soustraction de tokens sur le solde du wallet
    def sub_balance(self, balance):
        self.balance -= balance
        self.save()

    # Méthode d'envoi de tokens du wallet vers un autre wallet (liée à la transaction)
    def send(self, receiver, amount):
        self.sub_balance(amount)
        receiver.add_balance(amount)

    # Méthode de sauvegarde des données du wallet
    def save(self):
        content = json.dumps(self.__dict__)
        path = os.path.join(
            os.getcwd(), "content\\wallets\\", self.unique_id + ".json"
        )
        with open(path, "w+") as f:
            f.write(content)
            f.close()

    # Méthode de chargement des données du wallet s'il existe
    def load(self, unique_id):
        path = os.path.join(
            os.getcwd(), "content\\wallets\\", unique_id + ".json"
        )
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = json.loads(f.read())
                f.close()
                for k, v in content.items():
                    setattr(self, k, v)
        return os.path.isfile(path)
