# show.py

from PyQt5.QtWidgets import QMainWindow, QTextEdit
# ... other imports ...

class TextEditor(QMainWindow):
    def __init__(self, text):
        super().__init__()
        self.initUI(text)

    def initUI(self, text):
        self.text_edit = QTextEdit(self)
        self.text_edit.setText(text)
        self.text_edit.setReadOnly(False)  # Set to True if you want it to be read-only
        # ... set geometry, window title, etc. ...

# ... any additional methods or classes ...
