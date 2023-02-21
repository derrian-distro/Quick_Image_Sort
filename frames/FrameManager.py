import os
import hashlib
from typing import Optional

from frames.ImageFrame import ImageFrame
from frames.FolderFrame import FolderFrame
from modules import MessageBoxes

from PyQt6.QtWidgets import QStackedWidget, QMessageBox, QApplication


class FrameManager:
    def __init__(self, app: QApplication) -> None:
        self.stack: QStackedWidget = QStackedWidget()
        self.folder_collection: FolderFrame = FolderFrame()
        self.image_display: Optional[ImageFrame, None] = None
        self.app: QApplication = app
        self.dst_folders = None
        self.hash_names = False

        self.folder_collection.set_button_click(self.process_images)
        self.stack.addWidget(self.folder_collection)
        self.stack.show()

    def process_images(self):
        src_folders = self.folder_collection.get_src_list()
        self.dst_folders = self.folder_collection.get_dst_list()
        self.hash_names = self.folder_collection.hash_names
        if len(src_folders) == 0 or len(self.dst_folders) == 0:
            MessageBoxes.missing_message()
            return
        self.image_display = ImageFrame(src_folders, self.dst_folders, self.delete_image)
        self.image_display.create_dst_pages(self.move_image)
        if not self.update_image():
            self.add_folders()
        self.stack.addWidget(self.image_display)
        self.stack.setCurrentIndex(1)

    def delete_image(self) -> None:
        if not self.image_display:
            return
        if not os.path.exists("delete_hold"):
            os.mkdir("delete_hold")
        output = MessageBoxes.display_delete_message()
        if output == QMessageBox.StandardButton.Yes:
            self.image_display.del_image()
            if not self.update_image():
                self.add_folders()

    def move_image(self) -> None:
        btn = self.image_display.sender()
        folder = btn.folder
        if self.image_display.file_loc == '':
            return
        old_path = self.image_display.file_loc
        path, file = os.path.split(old_path)
        if self.hash_names:
            new_file = open(old_path, "rb")
            buffer = new_file.read()
            output = hashlib.sha3_256(buffer).hexdigest()
            outputs = file.split(".")
            extension = '.' + outputs.pop()
            new_file.close()
            file = output + extension
        new_path = os.path.normpath(os.path.join(folder, file))
        print(new_path)
        if os.path.exists(new_path):
            ret = MessageBoxes.display_duplicate_message()
            if ret == QMessageBox.StandardButton.No:
                return
            elif ret == QMessageBox.StandardButton.Discard:
                self.image_display.del_image()
                if not self.update_image():
                    self.add_folders()
                return
        self.image_display.clear_image()
        os.replace(old_path, new_path)
        self.image_display.undo_list.append(new_path)
        if not self.update_image():
            self.add_folders()

    def update_image(self) -> bool:
        found = self.image_display.find_image()
        while not found:
            found = self.image_display.update_src()
            if not found:
                return False
            found = self.image_display.find_image()
        return True

    def add_folders(self) -> None:
        ret = MessageBoxes.return_message()
        if ret == QMessageBox.StandardButton.Yes:
            self.stack.removeWidget(self.folder_collection)
            self.stack.removeWidget(self.image_display)
            self.folder_collection = FolderFrame()
            self.folder_collection.set_button_click(self.process_images)
            self.image_display = None
            self.stack.addWidget(self.folder_collection)
            return
        self.app.quit()
