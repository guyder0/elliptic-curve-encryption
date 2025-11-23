from windows.decorators import *
from ec.encryption import *
from ec.named_curves import registered_curves


class KeyPairManager:
    def __init__(self, window):
        self.window = window
        self.paths = {}

        self.setup_ui()
        self.set_connections()


    def setup_ui(self):
        for curve_name in registered_curves():
            self.window.create_chosenCurve.addItem(curve_name)


    def set_connections(self):
        self.window.create_choosePublicKey.clicked.connect(self.choose_public_key)
        self.window.create_choosePrivateKey.clicked.connect(self.choose_private_key)
        self.window.create_createKeys.clicked.connect(self.create_keys)


    def choose_public_key(self):
        method = choose_saving_path(self.window,
                                    self.window.create_chosenPublicKey,
                                    self.paths,
                                    'public_key',
        )
        method()


    def choose_private_key(self):
        method = choose_saving_path(self.window,
                                    self.window.create_chosenPrivateKey,
                                    self.paths,
                                    'private_key',
        )
        method()


    def create_keys(self):
        try:
            cypher_interface = ECC_encryption(self.window.create_chosenCurve.currentText())
            passphrase = self.window.create_passphrase.text()
            cypher_interface.generate_key_pair(passphrase, self.paths['private_key'], self.paths['public_key'])

        except Exception as e:
            QMessageBox.warning(self.window, "Ошибка", e.args[0])


    def encrypt_file(self):
        try:
            cypher_interface = ECC_encryption(self.window.encrypt_chosenCurve.currentText)
            cypher_interface.select_public_key(self.paths['public_key'])
            cypher_interface.encrypt_message(self.paths['source_file'], self.paths['output_file'])

        except Exception as e:
            QMessageBox.warning(self.window, "Ошибка", e.args[0])
