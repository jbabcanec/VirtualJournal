# utils/bottom_banner.py

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal

class BottomBanner(QWidget):
    textChanged = pyqtSignal(str)  # Signal to emit when text changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.wordCountLabel = QLabel("Words: 0")
        self.savedStateLabel = QLabel("Unsaved Changes")

        self.layout.addWidget(self.wordCountLabel)
        self.layout.addWidget(self.savedStateLabel)

    def updateWordCount(self, count):
        self.wordCountLabel.setText(f"Words: {count}")

    def updateSavedState(self, isSaved):
        state = "Saved" if isSaved else "Unsaved Changes"
        self.savedStateLabel.setText(state)
