# utils/zoom.py

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

class ZoomControl:
    def __init__(self, parent):
        self.parent = parent
        self.zoomLevel = 100  # Initialize zoom level

    def create_controls(self):
        # Create a layout for the zoom buttons
        zoomLayout = QVBoxLayout()

        # Create zoom in and zoom out buttons
        zoomInButton = QPushButton("Zoom In (+)")
        zoomOutButton = QPushButton("Zoom Out (-)")

        # Connect buttons to their respective slots
        zoomInButton.clicked.connect(lambda: self.adjust_zoom(10))
        zoomOutButton.clicked.connect(lambda: self.adjust_zoom(-10))

        # Add buttons to the layout
        zoomLayout.addWidget(zoomInButton)
        zoomLayout.addWidget(zoomOutButton)

        # Create a container widget for zoom controls and set the layout
        zoomContainer = QWidget()
        zoomContainer.setLayout(zoomLayout)

        return zoomContainer

    def adjust_zoom(self, change):
        self.zoomLevel += change
        self.zoomLevel = max(10, min(self.zoomLevel, 200))  # Ensure zoom level stays within bounds
        font = self.parent.text_edit.font()
        font.setPointSize(int(self.zoomLevel / 10))
        self.parent.text_edit.setFont(font)
