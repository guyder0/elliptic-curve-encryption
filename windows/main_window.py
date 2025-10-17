from .base_window import BaseWindow

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__('ui/main_window.ui')