# ribbon/options.py

from PyQt5.QtWidgets import QMenu, QToolButton, QAction, QTextEdit, QFontDialog, QColorDialog, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
import os

class CustomFontDialog(QFontDialog):
    def __init__(self, *args, **kwargs):
        super(CustomFontDialog, self).__init__(*args, **kwargs)
        icon_path = os.path.join(os.path.dirname(__file__), '../logo.ico')
        self.setWindowIcon(QIcon(icon_path))

class CustomColorDialog(QColorDialog):
    def __init__(self, *args, **kwargs):
        super(CustomColorDialog, self).__init__(*args, **kwargs)
        icon_path = os.path.join(os.path.dirname(__file__), '../logo.ico')
        self.setWindowIcon(QIcon(icon_path))

class OptionsFunctions:
    def __init__(self, main_toolbar, text_edit: QTextEdit):
        self.text_edit = text_edit
        self.setupOptionsMenu(main_toolbar)

    def setupOptionsMenu(self, main_toolbar):
        # Create the Options menu
        options_menu = QMenu()

        # 'Change Font' action
        change_font_action = QAction('Change Font', options_menu)
        change_font_action.triggered.connect(self.changeFont)
        options_menu.addAction(change_font_action)

        # 'Change Color' action
        change_color_action = QAction('Change Color', options_menu)
        change_color_action.triggered.connect(self.changeColor)
        options_menu.addAction(change_color_action)

        # 'Other Options...' action (placeholder for more options)
        other_options_action = QAction('Other Options...', options_menu)
        other_options_action.triggered.connect(self.showOptionsDialog)
        options_menu.addAction(other_options_action)

        # Create the Options button
        options_button = QToolButton()
        options_button.setText('Options')
        options_button.setMenu(options_menu)
        options_button.setPopupMode(QToolButton.InstantPopup)
        main_toolbar.addWidget(options_button)

    def changeFont(self):
        # Use the custom font dialog
        fontDialog = CustomFontDialog()
        if fontDialog.exec_():
            font = fontDialog.currentFont()
            self.text_edit.setFont(font)

    def changeColor(self):
        # Use the custom color dialog
        colorDialog = CustomColorDialog()
        if colorDialog.exec_():
            color = colorDialog.currentColor()
            if color.isValid():
                self.text_edit.setTextColor(color)

    def showOptionsDialog(self):
        # Placeholder for more complex options
        QMessageBox.information(None, 'Options', 'More options functionality goes here.')
