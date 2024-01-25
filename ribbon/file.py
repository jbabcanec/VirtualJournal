# ribbon/file.py

from PyQt5.QtWidgets import QMenu, QToolButton, QAction, QMessageBox, QTextEdit, QFileDialog

class FileFunctions:
    def __init__(self, main_toolbar, text_edit: QTextEdit, default_format='.txt'):
        self.text_edit = text_edit
        self.default_format = default_format  # Store the default format
        self.setupFileMenu(main_toolbar)

    def setupFileMenu(self, main_toolbar):
        # Create the File menu
        file_menu = QMenu()

        # 'New' action
        new_action = QAction('New', file_menu)
        new_action.triggered.connect(self.newFile)
        file_menu.addAction(new_action)

        # 'Open' action
        open_action = QAction('Open...', file_menu)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        # 'Save' action
        save_action = QAction('Save', file_menu)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        # 'Save As...' action
        save_as_action = QAction('Save As...', file_menu)
        save_as_action.triggered.connect(self.saveAsFile)
        file_menu.addAction(save_as_action)

        # 'Exit' action (optional)
        exit_action = QAction('Exit', file_menu)
        exit_action.triggered.connect(self.exitEditor)
        file_menu.addAction(exit_action)

        # Create the File button
        file_button = QToolButton()
        file_button.setText('File')
        file_button.setMenu(file_menu)
        file_button.setPopupMode(QToolButton.InstantPopup)
        main_toolbar.addWidget(file_button)

    def newFile(self):
        # Clear the text edit for a new file
        self.text_edit.clear()

    def openFile(self):
        # Open a file dialog to select and read a file
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'r') as file:
                self.text_edit.setText(file.read())

    def saveFile(self):
        print("Save File action triggered")  # Debug print
        filter = f"Text Files (*{self.default_format});;All Files (*)"
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", "", filter)
        print(f"Filename chosen: {filename}")  # Debug print
        if filename:
            if not filename.lower().endswith(self.default_format):
                filename += self.default_format
            with open(filename, 'w') as file:
                file.write(self.text_edit.toPlainText())
        else:
            print("Save operation cancelled")  # Debug print

    def saveAsFile(self):
        # Save the current text to a new file location
        self.saveFile()

    def exitEditor(self):
        # Exit the application (you might want to prompt for unsaved changes)
        QMessageBox.information(None, 'Exit', 'Exit functionality goes here.')
