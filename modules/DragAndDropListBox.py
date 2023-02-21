import os
from PyQt6 import QtGui
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt


class DragAndDropListBox(QListWidget):
    def __init__(self, allow_all=False, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.links = []
        self.include_sub_folders = allow_all

    def change_allow_all(self, new_val: bool):
        self.include_sub_folders = new_val

    # overloads QListWidget's dragEnterEvent function
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # overloads QListWidget's dragMoveEvent function
    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.acceptProposedAction()
        else:
            event.ignore()

    # overloads QListWidget's dropEvent function
    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.acceptProposedAction()
            to_display = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    temp = str(os.path.normpath(url.toLocalFile()))
                    if os.path.isdir(temp) and temp not in self.links:
                        self.links.append(temp)
                        to_display.append(temp)
                    if os.path.isdir(temp) and self.include_sub_folders:
                        for x in os.walk(temp):
                            if x[0] not in self.links:
                                self.links.append(os.path.normpath(x[0]))
                                to_display.append(os.path.normpath(x[0]))
            self.addItems(to_display)
        else:
            event.ignore()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            for sel in self.selectedItems():
                self.links.remove(sel.text())
                self.takeItem(self.row(sel))
