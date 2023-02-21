import os
import shutil
import sys

from frames.FrameManager import FrameManager

from PyQt6.QtWidgets import QApplication


def remove_held_images() -> None:
    if os.path.exists('delete_hold'):
        shutil.rmtree("delete_hold")
        os.mkdir("delete_hold")


def main() -> None:
    app = QApplication(sys.argv)
    required = FrameManager(app)
    app.exec()
    remove_held_images()
    sys.exit()


if __name__ == "__main__":
    main()
