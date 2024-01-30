# utils/re_record.py

import os
from PyQt5.QtWidgets import QToolButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon
from record import ChunkedSpeechRecorder

class RecordingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recording")
        self.setGeometry(200, 200, 200, 100)

        layout = QVBoxLayout()
        self.label = QLabel("Recording...")
        layout.addWidget(self.label)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.accept)
        layout.addWidget(self.stopButton)

        self.setLayout(layout)

class AudioProcessingThread(QThread):
    finished_processing = pyqtSignal()  # Signal when processing is done

    def __init__(self, recorder, parent=None):
        super().__init__(parent)
        self.recorder = recorder

    def run(self):
        self.recorder.process_audio_chunk()
        self.finished_processing.emit()  # Emit signal when done

class RecordControl:
    def __init__(self, parent):
        self.parent = parent
        self.recorder = ChunkedSpeechRecorder()
        self.recorder.recording_successful.connect(self.on_recording_successful)
        self.recording_dialog = None
        self.recording_thread = None

    def create_controls(self):
        # Create a record button with icon and text
        recordButton = QToolButton()
        recordButton.setText("Record")
        recordButton.setIcon(QIcon(self.get_icon_path("Record.png")))  # Adjust the icon filename as necessary
        recordButton.setIconSize(QSize(22, 22))  # Adjust icon size as needed
        recordButton.setToolTip("Start Recording")  # Tooltip for the button
        recordButton.clicked.connect(self.toggle_recording)
        recordButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # Set the button to display text beside the icon
        return recordButton

    def toggle_recording(self):
        if not self.recorder.is_recording:
            self.recorder.start_recording()
            self.recording_thread = AudioProcessingThread(self.recorder)
            self.recording_thread.finished_processing.connect(self.on_finished_processing)
            self.recording_thread.start()  # Start processing in a separate thread
            self.recording_dialog = RecordingDialog(self.parent)
            result = self.recording_dialog.exec_()  # Show the recording dialog

            if result:  # If the dialog was accepted (Stop button clicked)
                self.recorder.stop_recording()
        else:
            self.recorder.stop_recording()
            if self.recording_dialog:
                self.recording_dialog.accept()

    def on_finished_processing(self):
        if self.recording_thread.isRunning():
            self.recording_thread.quit()
            self.recording_thread.wait()

    def on_recording_successful(self, text):
        print("Recorded Text:", text)  # Print the recorded text to the console
        self.parent.text_edit.insertPlainText(text)

    def get_icon_path(self, icon_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
        return os.path.join(dir_path, "..", "icons", icon_name)  # Construct the full path to the icon