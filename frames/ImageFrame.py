import os
import subprocess
from math import ceil
from typing import Optional

from PIL import Image, UnidentifiedImageError
from PIL.ImageQt import ImageQt
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QMovie, QPixmap, QResizeEvent, QKeyEvent
from PyQt6.QtWidgets import QWidget, QLabel, QTabWidget, QPushButton, QGridLayout

from frames.PILHelper import pil_2_pixmap
from modules.DestButton import DestButton


class ImageFrame(QWidget):
    def __init__(self, src: list, dst: list, delete_button_func=None, parent=None) -> None:
        super().__init__(parent)
        # variables that won't change
        self.src_folders: list = src
        self.dst_folders: list = dst
        self.image: QLabel = QLabel()
        self.source_image_location: QLabel = QLabel()
        self.source_image_location.setWordWrap(True)
        self.file_number: QLabel = QLabel("files left in folder: 0")
        self.image.mousePressEvent = self.open_file_in_folder
        self.dst_display: QTabWidget = QTabWidget()
        self.delete_button: QPushButton = QPushButton("Delete Current Image")
        layout = QGridLayout()
        self.pages: int = ceil(len(dst) / 16)
        self.delete_func = delete_button_func

        # variables that will change
        self.current_folder_index: int = 0
        self.current_file_list: Optional[list, None] = None
        self.file_loc: str = ''
        self.current_image: Optional[QMovie, QPixmap, None] = None
        self.max_image_size: QSize = QSize(0, 0)
        self.is_gif: bool = False
        self.undo_list: list = []
        self.files_left: int = 0

        # optional setup
        if self.delete_func:
            self.delete_button.clicked.connect(delete_button_func)

        # create layout of items
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumSize(200, 200)
        layout.addWidget(self.image, 0, 0, 1, 2)
        layout.addWidget(self.dst_display, 0, 2, Qt.AlignmentFlag.AlignJustify)
        layout.addWidget(self.delete_button, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.source_image_location, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_number, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def set_image(self, img: str) -> None:
        self.file_loc = img
        self.source_image_location.setText(self.file_loc)
        with Image.open(self.file_loc) as im:
            if im.mode == 'RGBA':
                qim = ImageQt(im)
                self.current_image = QPixmap.fromImage(qim)
            else:
                self.current_image = pil_2_pixmap(im)
        self.max_image_size = self.current_image.size()
        im = self.current_image.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio)
        if im.size().width() > self.max_image_size.width() and im.size().height() > self.max_image_size.height():
            im = self.current_image
        self.image.setPixmap(im)
        self.is_gif = False

    def resize_image(self):
        im = self.current_image.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio)
        if im.size().width() > self.max_image_size.width() and im.size().height() > self.max_image_size.height():
            im = self.current_image
        self.image.setPixmap(im)

    def set_gif(self, gif: str) -> None:
        self.file_loc = gif
        self.source_image_location.setText(self.file_loc)
        self.current_image = QMovie(self.file_loc)
        self.current_image.jumpToFrame(1)
        self.current_image.start()
        self.max_image_size = self.current_image.currentPixmap().size()
        self.image.setMovie(self.current_image)
        self.is_gif = True
        self.resize_gif()

    def resize_gif(self):
        width_ratio = self.image.size().width() / self.max_image_size.width()
        height_ratio = self.image.size().height() / self.max_image_size.height()
        if width_ratio >= height_ratio:
            new_size = QSize(self.max_image_size.width() * height_ratio, self.image.size().height())
        else:
            new_size = QSize(self.image.size().width(), self.max_image_size.height() * width_ratio)
        self.current_image.setScaledSize(new_size)

    def create_dst_pages(self, func_to_run):
        self.dst_display.clear()

        def create_page(folder_list: [str], page_number: int) -> Optional[QtWidgets.QWidget]:
            start_point = 16 * page_number
            page_layout = QGridLayout()
            widget = QtWidgets.QWidget()
            row, col = 0, 0
            for j in range(start_point, len(folder_list)):
                throw, label = os.path.split(folder_list[j])
                button = DestButton(folder_list[j], label)
                button.clicked.connect(func_to_run)
                page_layout.addWidget(button, row, col, Qt.AlignmentFlag.AlignCenter)
                col += 1
                if col == 4:
                    row += 1
                    col = 0
                    if row == 4:
                        widget.setLayout(page_layout)
                        return widget
            if page_layout.count() > 0:
                widget.setLayout(page_layout)
                return widget
            else:
                return None

        for i in range(self.pages):
            wid = create_page(self.dst_folders, i)
            if wid:
                self.dst_display.addTab(wid, str(i + 1))

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.current_image is None:
            return
        if not self.is_gif:
            self.resize_image()
        else:
            self.resize_gif()

    def update_src(self):
        if self.current_folder_index >= len(self.src_folders):
            return False
        self.current_file_list = os.listdir(self.src_folders[self.current_folder_index])
        self.files_left = len(self.current_file_list) + 1
        self.file_number.setText("files left in folder: " + str(self.files_left))
        self.current_folder_index += 1
        return True

    def find_image(self):
        while self.current_file_list and len(self.current_file_list) != 0:
            file = self.current_file_list.pop()
            file = os.path.normpath(self.src_folders[self.current_folder_index - 1] + '/' + file)
            if os.path.isdir(file):
                self.files_left -= 1
                continue
            try:
                with Image.open(file) as img:
                    img_type = img.format
                    if img_type == 'WEBP':
                        if getattr(img, "is_animated", False):
                            img_type = 'GIF'
            except UnidentifiedImageError:
                self.files_left -= 1
                continue
            if img_type == 'GIF':
                self.files_left -= 1
                self.file_number.setText("files left in folder: " + str(self.files_left))
                self.set_gif(file)
                return True
            elif img_type:
                self.files_left -= 1
                self.file_number.setText("files left in folder: " + str(self.files_left))
                self.set_image(file)
                return True
        return False

    def set_del_button(self, func):
        self.delete_button.clicked.connect(func)

    def del_image(self):
        old_path = self.file_loc
        path, file = os.path.split(old_path)
        new_path = os.path.join("delete_hold", file)
        self.clear_image()
        os.replace(old_path, new_path)
        self.undo_list.append(new_path)

    def clear_image(self):
        self.file_loc = ''
        self.current_image = None
        self.max_image_size = QSize(0, 0)
        self.is_gif = False
        self.image.clear()
        self.image.setMovie(None)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.delete_func:
                self.delete_func()
        if event.key() == Qt.Key.Key_Z.value and \
                event.keyCombination().keyboardModifiers().value == Qt.KeyboardModifier.ControlModifier.value:
            if len(self.undo_list) != 0:
                path, file = os.path.split(self.file_loc)
                self.current_file_list.append(file)
                back_file = self.undo_list.pop()
                while not os.path.exists(back_file):
                    back_file = self.undo_list.pop()
                new_path, file_2 = os.path.split(back_file)
                path = os.path.normpath(os.path.join(path, file_2))
                os.replace(back_file, path)
                self.current_file_list.append(file_2)
                self.files_left += 2
                self.file_number.setText("files left in folder:" + str(self.files_left))
                self.clear_image()
                self.find_image()

    def open_file_in_folder(self, event):
        subprocess.Popen("explorer /select," + self.file_loc)
