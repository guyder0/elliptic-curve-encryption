from .base_window import BaseWindow

class PassphraseWindow(BaseWindow):
    def __init__(self):
        super().__init__('ui/passphrase_window.ui')