# utils/reconcile.py

from PyQt5.QtWidgets import QPushButton, QMessageBox, QDialog, QVBoxLayout, QTextEdit
import openai
from correct import read_api_key, correct_text

class CorrectionDialog(QDialog):
    def __init__(self, original_text, corrected_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Suggested Correction")
        self.setGeometry(300, 300, 600, 400)
        self.original_text = original_text
        self.corrected_text = corrected_text

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setText(self.corrected_text)
        layout.addWidget(self.text_edit)

        accept_button = QPushButton("Accept Correction")
        accept_button.clicked.connect(self.accept_correction)
        layout.addWidget(accept_button)

        reject_button = QPushButton("Reject Correction")
        reject_button.clicked.connect(self.reject_correction)
        layout.addWidget(reject_button)

        self.setLayout(layout)

    def accept_correction(self):
        cursor = self.parent().text_edit.textCursor()
        cursor.insertText(self.corrected_text)  # Replace selected text with correction
        self.accept()

    def reject_correction(self):
        self.reject()

class ReconcileControl:
    def __init__(self, parent):
        self.parent = parent
        self.api_key = read_api_key()

    def create_controls(self):
        correctButton = QPushButton("Correct")
        correctButton.clicked.connect(self.correct_text)
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