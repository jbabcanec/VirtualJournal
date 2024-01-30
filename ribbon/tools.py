# ribbon/tools.py

import os
from PyQt5.QtWidgets import QMenu, QToolButton, QAction, QTextEdit, QMessageBox
from PyQt5.QtGui import QIcon

class ToolsFunctions:
    def __init__(self, main_toolbar, text_edit: QTextEdit, editor: 'TextEditor'):
        self.text_edit = text_edit
        self.editor = editor  # Reference to the main TextEditor window
        self.tools_button = QToolButton()  # Initialize the tools_button
        self.tools_button.setText('Tools')
        self.tools_button.setPopupMode(QToolButton.InstantPopup)
        main_toolbar.addWidget(self.tools_button)  # Add the tools_button to the main toolbar
        self.setupToolsMenu()  # Call setupToolsMenu without passing main_toolbar


    def setupToolsMenu(self):
        # Create the Tools menu
        tools_menu = QMenu("Tools")

        # 'Word Count' action
        word_count_action = QAction('Word Count', tools_menu)
        word_count_action.triggered.connect(self.wordCount)
        tools_menu.addAction(word_count_action)

        # 'Search Text' action
        search_text_action = QAction('Search Text', tools_menu)
        search_text_action.triggered.connect(self.searchText)
        tools_menu.addAction(search_text_action)

        # Create the Docks submenu
        docks_menu = QMenu('Docks', tools_menu)

        # 'Text Editing' dock action
        text_editing_dock_action = QAction('Text Editing', docks_menu, checkable=True)
        text_editing_dock_action.setChecked(self.editor.leftDock.isVisible())
        text_editing_dock_action.triggered.connect(self.editor.toggleLeftDock)
        docks_menu.addAction(text_editing_dock_action)

        # 'Tools' dock action
        tools_dock_action = QAction('Tools', docks_menu, checkable=True)
        tools_dock_action.setChecked(self.editor.rightDock.isVisible())
        tools_dock_action.triggered.connect(self.editor.toggleRightDock)
        docks_menu.addAction(tools_dock_action)

        # Add the Docks submenu to the Tools menu
        tools_menu.addMenu(docks_menu)

        # Update the checks dynamically whenever the menu is about to show
        tools_menu.aboutToShow.connect(lambda: text_editing_dock_action.setChecked(self.editor.leftDock.isVisible()))
        tools_menu.aboutToShow.connect(lambda: tools_dock_action.setChecked(self.editor.rightDock.isVisible()))

        # 'Other Tools...' action (placeholder for more tools)
        other_tools_action = QAction('Other Tools...', tools_menu)
        other_tools_action.triggered.connect(self.showToolsDialog)
        tools_menu.addAction(other_tools_action)

        # Assign the complete Tools menu to the tools_button
        self.tools_button.setMenu(tools_menu)

    def wordCount(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        icon_path = self.get_icon_path("logo.ico")  # Use the helper method to get the icon path
        self.showMessage('Word Count', f'Total words: {word_count}', icon_path)

    def searchText(self):
        icon_path = self.get_icon_path("logo.ico")  # Use the helper method to get the icon path
        self.showMessage('Search Text', 'Search text functionality goes here.', icon_path)

    def showToolsDialog(self):
        icon_path = self.get_icon_path("logo.ico")  # Use the helper method to get the icon path
        self.showMessage('Tools', 'More tools functionality goes here.', icon_path)

    def showMessage(self, title, text, icon_path):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setWindowIcon(QIcon(icon_path))  # Set the window icon
        msgBox.exec_()
        
    def get_icon_path(self, icon_name):
        # Assuming this script is located in the 'ribbon' directory, adjust the path as needed
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "..", "icons", icon_name)