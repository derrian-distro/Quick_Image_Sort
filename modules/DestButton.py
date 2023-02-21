from PyQt6.QtWidgets import QPushButton


class DestButton(QPushButton):
    def __init__(self, folder: str, text: str, parent=None) -> None:
        super().__init__(parent)
        self.setText(text)
        self.folder = folder
