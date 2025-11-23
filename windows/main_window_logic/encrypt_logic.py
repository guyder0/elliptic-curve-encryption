from windows.decorators import *
from ec.encryption import *
from ec.named_curves import registered_curves


class EncryptManager:
    def __init__(self, window):
        self.window = window
        self.paths = {}

        self.setup_ui()
        self.set_connections()


    def setup_ui(self):
        for curve_name in registered_curves():
            self.window.encrypt_chosenCurve.addItem(curve_name)


    def set_connections(self):
        self.window.encrypt_choosePublicKey.clicked.connect(self.choose_public_key)
        self.window.encrypt_chooseSourceFile.clicked.connect(self.choose_source_file)
        self.window.encrypt_chooseOutputFile.clicked.connect(self.choose_output_file)
        self.window.encrypt_encryptFile.clicked.connect(self.encrypt_file)


    def choose_public_key(self):
        method = choose_existing_files(self.window,
                                       self.window.encrypt_chosenPublicKey,
                                       self.paths,
                                       'public_key',
        )
        method()


    def choose_source_file(self):
        method = choose_existing_files(self.window,
                                       self.window.encrypt_chosenSourceFile,
                                       self.paths,
                                       'source_file',
        )
        method()
        try:
            with open(self.paths['source_file'], 'r') as f:
                msg = f.read()
                self.window.encrypt_fileContent.setPlainText(msg)
        except Exception as e:
            QMessageBox.warning(self.window, "Ошибка", e.args[0])


    def choose_output_file(self):
        method = choose_saving_path(self.window,
                                    self.window.encrypt_chosenOutputFile,
                                    self.paths,
                                    'output_file',
        )
        method()


    def encrypt_file(self):
        try:
            cypher_interface = ECC_encryption(self.window.encrypt_chosenCurve.currentText())
            cypher_interface.select_public_key(self.paths['public_key'])
            cypher_interface.encrypt_message(self.paths['source_file'], self.paths['output_file'])

        except Exception as e:
            QMessageBox.warning(self.window, "Ошибка", e.args[0])
