# mic_check.py

from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import pyaudio

class MicCheckWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_accepted = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Microphone Check")
        self.resize(350, 200)  # Set window size

        # Set the window icon
        self.setWindowIcon(QIcon('logo.ico'))

        # Create layout and widgets
        layout = QVBoxLayout()

        # Create and add a label above the list
        self.label = QLabel("Please select audio input device")
        layout.addWidget(self.label)

        self.micList = QListWidget()
        self.populate_mics()
        layout.addWidget(self.micList)

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        layout.addWidget(self.okButton)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.cancelButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Center the window on the screen
        self.centerOnScreen()

    def centerOnScreen(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def populate_mics(self):
        p = pyaudio.PyAudio()
        default_index = p.get_default_input_device_info()['index']
        device_names = set()  # Set to track unique device names

        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            device_name = device_info.get('name')

            # Check if the device is an input device and not already added
            if device_info.get('maxInputChannels') > 0 and device_name not in device_names:
                self.micList.addItem(device_name)
                device_names.add(device_name)
                if i == default_index:
                    # Select the default device
                    self.micList.setCurrentRow(len(device_names) - 1)

        if not device_names:
            self.micList.addItem("No input devices found")

        p.terminate()

    def accept(self):
        self.user_accepted = True
        self.close()

    def reject(self):
        QApplication.instance().quit()
