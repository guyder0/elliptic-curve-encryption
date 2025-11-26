from .base_window import BaseWindow
from .main_window_logic import *
from .decorators import *
from PyQt6.QtWidgets import QMessageBox
from pathlib import Path

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__('ui/untitled.ui')
        self.encrypt_manager = EncryptManager(self)
        self.decrypt_managet = DecryptManager(self)
        self.key_pair_manager = KeyPairManager(self)
        self.set_connections()


    def set_connections(self):
        self.about_button.triggered.connect(self.about_dialog)


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