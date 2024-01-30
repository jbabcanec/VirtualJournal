# utils/text_edit.py

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QGroupBox, QHBoxLayout, QColorDialog
from PyQt5.QtGui import QIcon, QFont, QTextListFormat, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import QSize, Qt


class TextEditTools:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def create_controls(self):
        # Main layout for all text editing tools
        main_layout = QVBoxLayout()

        # Add groups to the main layout
        main_layout.addWidget(self.create_styling_group())
        main_layout.addWidget(self.create_text_formatting_group())
        main_layout.addWidget(self.create_alignment_group())
        main_layout.addWidget(self.create_list_group())

        # Push all groups to the top
        main_layout.addStretch(1)

        # Create a container widget and set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        return container

    def create_styling_group(self):
        styling_group = QGroupBox("Text Styling")
        styling_layout = QHBoxLayout()
        styling_layout.setSpacing(4)  # Reduced spacing between buttons
        styling_layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        styling_group.setLayout(styling_layout)
        for icon_name, tooltip, callback in [
            ("../icons/Bold.png", "Bold", self.toggleTextBold),
            ("../icons/Italics.png", "Italics", self.toggleTextItalic),
            ("../icons/Underline.png", "Underline", self.toggleTextUnderline)
        ]:
            styling_layout.addWidget(self.create_icon_button(icon_name, tooltip, callback))
        return styling_group

    def create_text_formatting_group(self):
        formatting_group = QGroupBox("Text Formatting")
        formatting_layout = QHBoxLayout()
        formatting_layout.setSpacing(4)
        formatting_layout.setContentsMargins(5, 5, 5, 5)
        formatting_group.setLayout(formatting_layout)

        # Add buttons for new functionalities
        for icon_name, tooltip, callback in [
            ("../icons/Highlight.png", "Highlight Text", self.highlightText),
            ("../icons/IncreaseFontSize.png", "Increase Font Size", self.increaseFontSize),
            ("../icons/DecreaseFontSize.png", "Decrease Font Size", self.decreaseFontSize),
            ("../icons/TextColor.png", "Text Color", self.changeTextColor)
        ]:
            formatting_layout.addWidget(self.create_icon_button(icon_name, tooltip, callback))

        return formatting_group

    def create_alignment_group(self):
        alignment_group = QGroupBox("Text Alignment")
        alignment_layout = QHBoxLayout()
        alignment_layout.setSpacing(4)  # Reduced spacing between buttons
        alignment_layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        alignment_group.setLayout(alignment_layout)
        for icon_name, tooltip, callback in [
            ("../icons/Align_Left.png", "Align Left", lambda: self.text_edit.setAlignment(Qt.AlignLeft)),
            ("../icons/Align_Right.png", "Align Right", lambda: self.text_edit.setAlignment(Qt.AlignRight)),
            ("../icons/Align_Center.png", "Align Center", lambda: self.text_edit.setAlignment(Qt.AlignCenter)),
            ("../icons/Align_Justify.png", "Align Justify", lambda: self.text_edit.setAlignment(Qt.AlignJustify))
        ]:
            alignment_layout.addWidget(self.create_icon_button(icon_name, tooltip, callback))
        return alignment_group

    def create_list_group(self):
        list_group = QGroupBox("Lists")
        list_layout = QHBoxLayout()
        list_layout.setSpacing(4)  # Reduced spacing between buttons
        list_layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        list_group.setLayout(list_layout)
        for icon_name, tooltip, callback in [
            ("../icons/Bullets.png", "Bullets", lambda: self.insertList(QTextListFormat.ListDisc)),
            ("../icons/Numbered_List.png", "Numbered List", lambda: self.insertList(QTextListFormat.ListDecimal))
        ]:
            list_layout.addWidget(self.create_icon_button(icon_name, tooltip, callback))
        return list_group

    def create_icon_button(self, icon_name, tooltip, callback):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(dir_path, "..", "icons", icon_name)
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(18, 18))
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.setMaximumSize(QSize(22, 22))
        return button

    def toggleTextBold(self):
        self.text_edit.setFontWeight(QFont.Bold if not self.text_edit.fontWeight() == QFont.Bold else QFont.Normal)

    def toggleTextItalic(self):
        self.text_edit.setFontItalic(not self.text_edit.fontItalic())

    def toggleTextUnderline(self):
        self.text_edit.setFontUnderline(not self.text_edit.fontUnderline())

    def highlightText(self):
        color = QColorDialog.getColor()  # Open a color dialog to pick the color
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.mergeFormatOnWordOrSelection(fmt)

    def increaseFontSize(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            currentSize = fmt.fontPointSize()
            if currentSize <= 0:  # If for some reason the size is not valid, set a default size before increasing
                currentSize = 12
            fmt.setFontPointSize(currentSize + 1)
            cursor.mergeCharFormat(fmt)
        else:
            fmt = self.text_edit.currentCharFormat()
            currentSize = fmt.fontPointSize()
            if currentSize <= 0:  # If for some reason the size is not valid, set a default size before increasing
                currentSize = 12
            fmt.setFontPointSize(currentSize + 1)
            self.text_edit.setCurrentCharFormat(fmt)

    def decreaseFontSize(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            currentSize = fmt.fontPointSize()
            if currentSize > 1:  # Ensure the font size does not go below 1
                fmt.setFontPointSize(currentSize - 1)
                cursor.mergeCharFormat(fmt)
        else:
            fmt = self.text_edit.currentCharFormat()
            currentSize = fmt.fontPointSize()
            if currentSize > 1:  # Ensure the font size does not go below 1
                fmt.setFontPointSize(currentSize - 1)
                self.text_edit.setCurrentCharFormat(fmt)


    def changeTextColor(self):
        color = QColorDialog.getColor(self.text_edit.textColor())  # Open a color dialog with the current text color
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.mergeFormatOnWordOrSelection(fmt)

    def insertList(self, listStyle):
        cursor = self.text_edit.textCursor()
        cursor.insertList(listStyle)

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.text_edit.mergeCurrentCharFormat(format)
