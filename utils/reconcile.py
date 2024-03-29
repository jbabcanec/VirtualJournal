# utils/reconcile.py

import os
from PyQt5.QtWidgets import QWidget, QToolButton, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton  # Added QPushButton here
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
import openai
from correct import read_api_key, correct_text


class CorrectionDialog(QDialog):
    def __init__(self, original_text, corrected_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Suggested Correction")
        self.setGeometry(300, 300, 800, 400)  # Adjust size as needed
        self.original_text = original_text
        self.corrected_text = corrected_text

        main_layout = QVBoxLayout()
        comparison_layout = QHBoxLayout()

        self.original_text_edit = QTextEdit()
        self.original_text_edit.setText(self.original_text)
        self.original_text_edit.setReadOnly(True)  # Make original text read-only
        comparison_layout.addWidget(self.original_text_edit)

        self.corrected_text_edit = QTextEdit()
        self.corrected_text_edit.setText(self.corrected_text)
        comparison_layout.addWidget(self.corrected_text_edit)

        main_layout.addLayout(comparison_layout)

        accept_button = QPushButton("Accept Correction")
        accept_button.clicked.connect(self.accept_correction)
        main_layout.addWidget(accept_button)

        reject_button = QPushButton("Reject Correction")
        reject_button.clicked.connect(self.reject_correction)
        main_layout.addWidget(reject_button)

        self.setLayout(main_layout)

    def accept_correction(self):
        cursor = self.parent().text_edit.textCursor()
        cursor.insertText(self.corrected_text_edit.toPlainText())  # Replace selected text with correction
        self.accept()

    def reject_correction(self):
        self.reject()

class ReconcileControl:
    def __init__(self, parent):
        self.parent = parent
        self.api_key = read_api_key()

    def create_controls(self):
        # Create a correct button with icon and text
        correctButton = QToolButton()
        correctButton.setText("Correct")
        correctButton.setIcon(QIcon(self.get_icon_path("Correct.png")))  # Adjust the icon filename as necessary
        correctButton.setIconSize(QSize(22, 22))  # Adjust icon size as needed
        correctButton.setToolTip("Correct Text")  # Tooltip for the button
        correctButton.clicked.connect(self.correct_text)
        correctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # Set the button to display text beside the icon
        return correctButton

    def correct_text(self):
        selected_text = self.parent.text_edit.textCursor().selectedText()
        if selected_text:
            corrected_text = correct_text(selected_text, self.api_key)
            self.show_correction_dialog(selected_text, corrected_text)
        else:
            QMessageBox.warning(self.parent, "No Text Selected", "Please highlight text to correct.")

    def show_correction_dialog(self, original_text, corrected_text):
        correction_dialog = CorrectionDialog(original_text, corrected_text, self.parent)
        correction_dialog.exec_()

    def get_icon_path(self, icon_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
        return os.path.join(dir_path, "..", "icons", icon_name)  # Construct the full path to the icon