# utils/translate.py

import os
from PyQt5.QtWidgets import QWidget, QToolButton, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from googletrans import Translator, LANGUAGES

class TranslationDialog(QDialog):
    def __init__(self, original_text, parent=None):
        super().__init__(parent)
        self.parent = parent  # Keep a reference to the parent to modify the main text edit
        self.setWindowTitle("Translation")
        self.setGeometry(300, 300, 800, 400)

        main_layout = QVBoxLayout()
        comparison_layout = QHBoxLayout()

        self.original_text_edit = QTextEdit()
        self.original_text_edit.setText(original_text)
        self.original_text_edit.setReadOnly(True)
        comparison_layout.addWidget(self.original_text_edit)

        self.translated_text_edit = QTextEdit()
        self.translated_text_edit.setReadOnly(True)
        comparison_layout.addWidget(self.translated_text_edit)

        main_layout.addLayout(comparison_layout)

        language_layout = QHBoxLayout()
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Spanish", "French", "German", "Chinese", "Japanese"])
        language_layout.addWidget(self.language_selector)

        translate_button = QPushButton("Translate")
        translate_button.clicked.connect(self.translate_text)
        language_layout.addWidget(translate_button)

        replace_button = QPushButton("Replace Text")
        replace_button.clicked.connect(self.replace_text)
        language_layout.addWidget(replace_button)

        main_layout.addLayout(language_layout)
        self.setLayout(main_layout)

    def translate_text(self):
        translator = Translator()
        selected_language = self.language_selector.currentText().lower()
        
        # Convert language selection to ISO 639-1 language codes used by googletrans
        lang_code = ''
        for code, lang in LANGUAGES.items():
            if lang == selected_language.lower():
                lang_code = code
                break

        # If the language is not supported, show a message box and return
        if not lang_code:
            QMessageBox.warning(self, "Translation Error", "Selected language is not supported for translation.")
            return

        try:
            translated = translator.translate(self.original_text_edit.toPlainText(), dest=lang_code)
            self.translated_text_edit.setText(translated.text)
        except Exception as e:
            QMessageBox.warning(self, "Translation Error", f"An error occurred during translation: {e}")


    def replace_text(self):
        cursor = self.parent.text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(self.translated_text_edit.toPlainText())
        cursor.endEditBlock()
        self.close()

class TranslateControl:
    def __init__(self, parent):
        self.parent = parent

    def create_controls(self):
        translateButton = QToolButton()
        translateButton.setText("Translate")
        translateButton.setIcon(QIcon(self.get_icon_path("Translate.png")))
        translateButton.setIconSize(QSize(22, 22))
        translateButton.setToolTip("Translate Text")
        translateButton.clicked.connect(self.show_translation_dialog)
        translateButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        return translateButton

    def show_translation_dialog(self):
        selected_text = self.parent.text_edit.textCursor().selectedText()
        if selected_text:
            translation_dialog = TranslationDialog(selected_text, self.parent)
            translation_dialog.exec_()
        else:
            QMessageBox.warning(self.parent, "No Text Selected", "Please highlight text to translate.")

    def get_icon_path(self, icon_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "..", "icons", icon_name)
