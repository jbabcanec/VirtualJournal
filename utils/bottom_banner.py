# utils/bottom_banner.py

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

class BottomBanner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.wordCountLabel = QLabel("Words: 0")
        self.paragraphCountLabel = QLabel("Paragraphs: 0")
        self.savedStateLabel = QLabel("Unsaved Changes")

        self.layout.addWidget(self.wordCountLabel)
        self.layout.addWidget(self.paragraphCountLabel)
        self.layout.addWidget(self.savedStateLabel)

    def updateWordCount(self, count):
        self.wordCountLabel.setText(f"Words: {count}")

    def updateParagraphCount(self, count):
        self.paragraphCountLabel.setText(f"Paragraphs: {count}")

    def updateSavedState(self, isSaved):
        state = "Saved" if isSaved else "Unsaved Changes"
        self.savedStateLabel.setText(state)
