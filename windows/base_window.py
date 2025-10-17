import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic.load_ui import loadUi

class BaseWindow(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        loadUi(ui_file, self)