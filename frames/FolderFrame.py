import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QCheckBox, QMessageBox

from modules.DragAndDropListBox import DragAndDropListBox
from modules.MessageBoxes import display_hash_warning


class FolderFrame(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # define layout and set minimum size for column, as well as misc variables
        self.layout: QGridLayout = QGridLayout()
        self.layout.setColumnMinimumWidth(0, 300)
        self.layout.setColumnMinimumWidth(1, 300)
        self.allow_all = False
        self.hash_names = False

        # define labels
        self.src_label: QLabel = QLabel('Drag the folders you want to use as sources into the list below')
        self.out_label: QLabel = QLabel('Drag the folders you want to use as destinations into the list below')
        self.setup_labels()
        self.layout.addWidget(self.src_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.out_label, 0, 1, Qt.AlignmentFlag.AlignCenter)

        # define listBoxes and set size
        self.src_list_box: DragAndDropListBox = DragAndDropListBox(allow_all=self.allow_all)
        self.out_list_box: DragAndDropListBox = DragAndDropListBox()
        self.layout.addWidget(self.src_list_box, 1, 0)
        self.layout.addWidget(self.out_list_box, 1, 1)

        # define the checkboxes
        self.decide_allow_all: QCheckBox = QCheckBox("Also Add Sub Folders")
        self.decide_allow_all.clicked.connect(self.swap_allow_all)
        self.hash_file_names: QCheckBox = QCheckBox("Hash File Names")
        self.hash_file_names.clicked.connect(self.swap_hash_names)
        self.layout.addWidget(self.decide_allow_all, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.hash_file_names, 2, 0, Qt.AlignmentFlag.AlignRight)

        # define the buttons
        self.cont_button: QPushButton = QPushButton("continue")
        exit_button = QPushButton("exit")
        exit_button.clicked.connect(sys.exit)
        self.layout.addWidget(self.cont_button, 2, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(exit_button, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)

    def setup_labels(self) -> None:
        self.src_label.setWordWrap(True)
        self.src_label.setMinimumHeight(40)
        self.src_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.out_label.setWordWrap(True)
        self.out_label.setMinimumHeight(40)
        self.out_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_button_click(self, function) -> None:
        self.cont_button.clicked.connect(function)

    def get_src_list(self):
        return self.src_list_box.links

    def get_dst_list(self):
        return self.out_list_box.links

    def swap_allow_all(self):
        self.allow_all = not self.allow_all
        self.src_list_box.change_allow_all(self.allow_all)

    def swap_hash_names(self):
        if not self.hash_names:
            ret = display_hash_warning()
            if ret == QMessageBox.StandardButton.Yes:
                self.hash_names = True
            else:
                self.hash_file_names.setChecked(False)
        else:
            self.hash_names = False
