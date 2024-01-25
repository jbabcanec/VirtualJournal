# ribbon/edit.py

from PyQt5.QtWidgets import QMenu, QToolButton, QAction, QTextEdit

class EditFunctions:
    def __init__(self, main_toolbar, text_edit: QTextEdit):
        self.text_edit = text_edit
        self.setupEditMenu(main_toolbar)

    def setupEditMenu(self, main_toolbar):
        # Create the Edit menu
        edit_menu = QMenu()

        # 'Undo' action
        undo_action = QAction('Undo', edit_menu)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        # 'Redo' action
        redo_action = QAction('Redo', edit_menu)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        # 'Cut' action
        cut_action = QAction('Cut', edit_menu)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        # 'Copy' action
        copy_action = QAction('Copy', edit_menu)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        # 'Paste' action
        paste_action = QAction('Paste', edit_menu)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        # Create the Edit button
        edit_button = QToolButton()
        edit_button.setText('Edit')
        edit_button.setMenu(edit_menu)
        edit_button.setPopupMode(QToolButton.InstantPopup)
        main_toolbar.addWidget(edit_button)

