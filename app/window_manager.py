from windows import MainWindow, CreateChannelWindow, EncryptWindow, DecryptWindow, PassphraseWindow

class WindowManager:
    def __init__(self):
        pass

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.create_channel.clicked.connect(
            self.open_create_channel_window)
        self.main_window.encrypt_message.clicked.connect(
            self.open_encrypt_window)
        self.main_window.decrypt_message.clicked.connect(
            self.open_passphrase_window)
        self.main_window.show()

    def open_create_channel_window(self):
        self.create_channel_window = CreateChannelWindow(self.main_window)
        self.create_channel_window.show()

    def open_passphrase_window(self):
        self.passphrase_window = PassphraseWindow()
        self.passphrase_window.show()

    def open_encrypt_window(self):
        self.encrypt_window = EncryptWindow()
        self.encrypt_window.show()

    def open_decrypt_window(self):
        self.decrypt_window = DecryptWindow()
        self.decrypt_window.show()