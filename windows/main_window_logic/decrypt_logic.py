from windows.decorators import *
from ec.encryption import *
from ec.named_curves import registered_curves

from PyQt6.QtWidgets import QInputDialog, QLineEdit


class DecryptManager:
    def __init__(self, window):
        self.window = window
        self.paths = {}

        self.setup_ui()
        self.set_connections()


    def setup_ui(self):
        for curve_name in registered_curves():
            self.window.decrypt_chosenCurve.addItem(curve_name)


    def set_connections(self):
        self.window.decrypt_choosePrivateKey.clicked.connect(self.choose_private_key)
        self.window.decrypt_chooseSourceFile.clicked.connect(self.choose_source_file)
        self.window.decrypt_chooseOutputFile.clicked.connect(self.choose_output_file)
        self.window.decrypt_decryptFile.clicked.connect(self.decrypt_file)


    def choose_private_key(self):
        method = choose_existing_files(self.window,
                                       self.window.decrypt_chosenPrivateKey,
                                       self.paths,
                                       'private_key',
        )
        method()


    def choose_source_file(self):
        method = choose_existing_files(self.window,
                                       self.window.decrypt_chosenSourceFile,
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
                                    self.window.decrypt_chosenOutputFile,
                                    self.paths,
                                    'output_file',
        )
        method()


    def decrypt_file(self):
        try:
            passphrase, ok = QInputDialog.getText(self.window, 'Проверка парольной фразы', 'Введите парольную фразу', QLineEdit.EchoMode.Password)
            if not passphrase or not ok:
                raise Exception('Введите парольную фразу!')

            cypher_interface = ECC_encryption(self.window.decrypt_chosenCurve.currentText())
            cypher_interface.select_private_key(passphrase, self.paths['private_key'])
            cypher_interface.decrypt_message(self.paths['source_file'], self.paths['output_file'])

        except Exception as e:
            QMessageBox.warning(self.window, "Ошибка", str(e.args))
