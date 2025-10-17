from PyQt6.QtWidgets import QApplication
from .window_manager import WindowManager

class Application:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.window_manager = WindowManager()
        self.setup_connections()

    def setup_connections(self):
        pass

    def run(self):
        self.window_manager.open_main_window()
        return self.app.exec()