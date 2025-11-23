from .base_window import BaseWindow
from .main_window_logic import *
from .decorators import *
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from pathlib import Path

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__('ui/untitled.ui')
        self.encrypt_manager = EncryptManager(self)
        self.key_pair_manager = KeyPairManager(self)
        self.set_connections()

    def set_connections(self):
        self.about_button.triggered.connect(self.about_dialog)

        # # decrypt file
        # self.decrypt_decryptFile.clicked.connect(self.check_passphrase)
        # self.decrypt_choosePrivateKey.clicked.connect(self.choose_existing_files(
        #     self.decrypt_chosenPrivateKey,
        #     'decrypt_private_key'
        # ))
        # self.decrypt_chooseSourceFile.clicked.connect(self.choose_existing_files(
        #     self.decrypt_chosenSourceFile,
        #     'decrypt_source_file'
        # ))

        # # create keys
        # self.create_choosePublicKey.clicked.connect(self.choose_saving_path(
        #     self.create_chosenPublicKey,
        #     'create_public_key'
        # ))

    def about_dialog(self):
        text = """
            <h2>Реализация криптоалгоритма на основе эллиптических кривых</h2>
            <p><b>Выполнил:</b> Володченков Н.Д.</p>
            <p><b>Группа:</b> А-05-22</p>
        """
        QMessageBox.about(
            self,
            "О программе",
            text
        )