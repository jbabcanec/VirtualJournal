# utils/zoom.py

import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class ZoomControl:
    def __init__(self, parent):
        self.parent = parent
        self.zoomLevel = 100  # Initialize zoom level

    def create_controls(self):
        # Create a layout for the zoom buttons
        zoomLayout = QVBoxLayout()

        # Create zoom in and zoom out buttons with icons and text
        zoomInButton = self.create_icon_button("ZoomIn.png", "Zoom In", lambda: self.adjust_zoom(10))
        zoomOutButton = self.create_icon_button("ZoomOut.png", "Zoom Out", lambda: self.adjust_zoom(-10))

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

    def create_icon_button(self, icon_name, tooltip, callback):
        dir_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
        icon_path = os.path.join(dir_path, "..", "icons", icon_name)  # Construct the full path to the icon
        button = QToolButton()
        button.setText(tooltip)  # Set the button text
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(22, 22))  # Adjust icon size as needed
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # Set the button to display text beside the icon
        return button
