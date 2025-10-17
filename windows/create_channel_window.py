from .base_window import BaseWindow

class CreateChannelWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__('ui/create_channel_window.ui')
        self.create_channel.clicked.connect(self.button_click)
        self.parent = parent

    def button_click(self):
        self.parent.is_created_label.setText('создан')
        self.parent.is_created_label.setStyleSheet('color: green;')

        self.parent.curve_name_label.setText('secp386r1')
        self.parent.curve_name_label.setStyleSheet('')

        self.parent.encrypt_message.setEnabled(True)
        self.parent.decrypt_message.setEnabled(True)
        self.close()