# utils/text_edit.py

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QMessageBox, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class TextEditTools:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def create_controls(self):
        # Main layout for all text editing tools
        main_layout = QVBoxLayout()

        # Group for text styling tools
        styling_group = QGroupBox("Text Styling")
        styling_layout = QHBoxLayout()
        styling_group.setLayout(styling_layout)
        styling_layout.addWidget(self.create_icon_button("../icons/Bold.png", "Bold", self.toggleTextBold))
        styling_layout.addWidget(self.create_icon_button("../icons/Italics.png", "Italics", self.toggleTextItalic))
        styling_layout.addWidget(self.create_icon_button("../icons/Underline.png", "Underline", self.toggleTextUnderline))
        main_layout.addWidget(styling_group)

        # Group for text alignment tools
        alignment_group = QGroupBox("Text Alignment")
        alignment_layout = QHBoxLayout()
        alignment_group.setLayout(alignment_layout)
        alignment_layout.addWidget(self.create_icon_button("../icons/Align_Left.png", "Align Left", lambda: self.text_edit.setAlignment(Qt.AlignLeft)))
        alignment_layout.addWidget(self.create_icon_button("../icons/Align_Right.png", "Align Right", lambda: self.text_edit.setAlignment(Qt.AlignRight)))
        alignment_layout.addWidget(self.create_icon_button("../icons/Align_Center.png", "Align Center", lambda: self.text_edit.setAlignment(Qt.AlignCenter)))
        alignment_layout.addWidget(self.create_icon_button("../icons/Align_Justify.png", "Align Justify", lambda: self.text_edit.setAlignment(Qt.AlignJustify)))
        main_layout.addWidget(alignment_group)

        # Group for list tools
        list_group = QGroupBox("Lists")
        list_layout = QHBoxLayout()
        list_group.setLayout(list_layout)
        list_layout.addWidget(self.create_icon_button("../icons/Bullets.png", "Bullets", lambda: self.insertList(QTextListFormat.ListDisc)))
        list_layout.addWidget(self.create_icon_button("../icons/Numbered_List.png", "Numbered List", lambda: self.insertList(QTextListFormat.ListDecimal)))
        main_layout.addWidget(list_group)

        # Create a container widget and set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        return container

    def create_icon_button(self, icon_name, tooltip, callback):
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Construct an absolute path to the icon
        icon_path = os.path.join(dir_path, "..", "icons", icon_name)

        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(18, 18))  # Set a smaller icon size if needed
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.setMaximumSize(QSize(22, 22))  # Limit the size of the button
        return button

    def toggleTextBold(self):
        self.text_edit.setFontWeight(QFont.Bold if not self.text_edit.fontWeight() == QFont.Bold else QFont.Normal)

    def toggleTextItalic(self):
        self.text_edit.setFontItalic(not self.text_edit.fontItalic())

    def toggleTextUnderline(self):
        self.text_edit.setFontUnderline(not self.text_edit.fontUnderline())

    def insertList(self, listStyle):
        cursor = self.text_edit.textCursor()
        cursor.insertList(listStyle)
