from .base_window import BaseWindow
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from pathlib import Path

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__('ui/untitled.ui')
        self.set_connections()
        self.chosen_paths = {}

    def set_connections(self):
        # MENU
        self.about_button.triggered.connect(self.about_dialog)

        # DECRYPT FILE ZONE
        self.decrypt_decryptFile.clicked.connect(self.check_passphrase)
        self.decrypt_choosePrivateKey.clicked.connect(self.choose_existing_files(
            self.decrypt_chosenPrivateKey,
            'decrypt_private_key'
        ))
        self.decrypt_chooseSourceFile.clicked.connect(self.choose_existing_files(
            self.decrypt_chosenSourceFile,
            'decrypt_source_file'
        ))

        # CREATE KEYS ZONE
        self.create_choosePublicKey.clicked.connect(self.choose_saving_path(
            self.create_chosenPublicKey,
            'create_public_key'
        ))

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

    def check_passphrase(self):
        passphrase, ok = QInputDialog.getText(
            None,
            "Проверка парольной фразы",
            "Введите парольную фразу:"
        )

    def choose_existing_files(self, output_widget, metainfo):
        def result():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл",
                "",
                "Текстовые файлы (*.txt);;Все файлы (*)"
            )
            file_path = Path(file_path)
            file_path = file_path.relative_to(Path.cwd())
            output_widget.setText(str(file_path))
            self.chosen_paths[metainfo] = file_path
        return result

    def choose_saving_path(self, output_widget, metainfo):
        def result():
            file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
                "Сохранить файл",
                "",
                "Текстовые файлы (*.txt);;Все файлы (*)"
            )
            file_path = Path(file_path)
            file_path = file_path.relative_to(Path.cwd())
            output_widget.setText(str(file_path))
            self.chosen_paths[metainfo] = file_path
        return result