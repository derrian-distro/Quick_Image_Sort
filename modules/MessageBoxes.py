from PyQt6.QtWidgets import QMessageBox


def missing_message() -> None:
    x = QMessageBox()
    x.setModal(True)
    x.setWindowTitle("Missing Entry")
    x.setText("You must have at least one entry in both lists")
    x.setIcon(QMessageBox.Icon.Critical)
    x.exec()


def display_delete_message() -> int:
    x = QMessageBox()
    x.setModal(True)
    x.setWindowTitle("Delete Image")
    x.setText("     Are you sure you want to delete this image?\n"
              "It cannot be recovered once this operation is completed")
    x.setIcon(QMessageBox.Icon.Question)
    x.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    x.setDefaultButton(QMessageBox.StandardButton.Yes)
    return x.exec()


def display_duplicate_message() -> int:
    x = QMessageBox()
    x.setModal(True)
    x.setWindowTitle("File already exists")
    x.setText("File already exists in folder, do you want to replace")
    x.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                         | QMessageBox.StandardButton.Discard)
    x.setDefaultButton(QMessageBox.StandardButton.No)
    return x.exec()


def return_message() -> int:
    x = QMessageBox()
    x.setModal(True)
    x.setWindowTitle("Return to folder entry?")
    x.setText("There are no more images within the sources you have provided, do you want to set new folders?")
    x.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    x.setDefaultButton(QMessageBox.StandardButton.Yes)
    return x.exec()


def display_hash_warning() -> int:
    x = QMessageBox()
    x.setModal(True)
    x.setWindowTitle("Are You Sure?")
    x.setText("Activating this option will automatically rename all files it moves to reduce file name collisions," +
              " are you sure you want to do this?")
    x.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    x.setDefaultButton(QMessageBox.StandardButton.No)
    x.setIcon(QMessageBox.Icon.Warning)
    return x.exec()

