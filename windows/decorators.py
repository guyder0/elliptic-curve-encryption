from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from PyQt6.QtGui import QFont
from pathlib import Path
import traceback


def choose_existing_files(parent, output_widget, path, field_name):
    def result():
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Выберите файл",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if not file_path: return
        file_path = Path(file_path)
        path[field_name] = file_path

        relative_path = file_path.name
        output_widget.setText(str(relative_path))

    return result


def choose_saving_path(parent, output_widget, path, field_name):
    def result():
        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Сохранить файл",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if not file_path: return
        file_path = Path(file_path)
        path[field_name] = file_path

        relative_path = file_path.name
        output_widget.setText(str(relative_path))

    return result


def check_passphrase(window, checker, handler):
    passphrase, ok = QInputDialog.getText(window, "Парольная фраза", "Введите парольную фразу")
    try:
        checker(passphrase)
        handler()
    except Exception as e:
        QMessageBox.warning(window, "Ошибка", e.args[0])


def warning_box(exception, parent=None):
    formatted = traceback.format_exception(type(exception), exception, exception.__traceback__)
    msg = QMessageBox(parent, )
    msg.setWindowTitle("Ошибка!")
    msg.setText(''.join(formatted[-1]))
    msg.setDetailedText(''.join(formatted))
    msg.exec()