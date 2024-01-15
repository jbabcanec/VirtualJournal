# landing.py

from PyQt5.QtWidgets import QMainWindow, QPushButton, QComboBox, QCheckBox, QLabel, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import QSize, QTimer, QTime, pyqtSignal
from record import ChunkedSpeechRecorder
import threading

class LandingPage(QMainWindow):
    proceedWithRecording = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.speech_recorder = ChunkedSpeechRecorder()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timeElapsed = QTime(0, 0, 0)

    def initUI(self):
        self.setWindowTitle("Voice to Text Journal")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height

        # Set the window icon
        self.setWindowIcon(QIcon('logo.ico'))

        # # Set the background color of the window to white
        # self.setStyleSheet("background-color: white;")

        # Center the window on the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Connect signals to slots
        self.speech_recorder.recording_successful.connect(self.on_recording_successful)
        self.speech_recorder.recording_error.connect(self.on_recording_error)

        # Start Recording Button
        self.startButton = QPushButton("Start Recording", self)
        self.startButton.setGeometry(100, 100, 200, 50)  # x, y, width, height
        self.startButton.clicked.connect(self.toggleRecording)

        # Timer Label (Initially hidden)
        self.timerLabel = QLabel(self)
        self.timerLabel.setGeometry(170, 30, 100, 20)  # Adjust position and size as needed
        self.timerLabel.hide()

        # Sound Wave Animation (Initially hidden, adjusted position and size)
        self.soundWaveAnimation = QLabel(self)
        self.soundWaveAnimation.setGeometry(150, 50, 100, 40)  # x, y, width, height
        self.soundWaveMovie = QMovie("waves.gif")  # Placeholder animation
        self.soundWaveMovie.setScaledSize(QSize(100, 40))  # Scaling the movie to fit label size
        self.soundWaveAnimation.setMovie(self.soundWaveMovie)
        self.soundWaveAnimation.hide()

        # Dropdown for output file format selection
        self.fileFormatLabel = QLabel("Output File Format:", self)
        self.fileFormatLabel.setGeometry(50, 200, 150, 30)  # x, y, width, height
        self.fileFormatDropdown = QComboBox(self)
        self.fileFormatDropdown.setGeometry(210, 200, 150, 30)  # x, y, width, height
        self.fileFormatDropdown.addItems([".txt", ".docx", ".pdf"])  # Example formats

        # Checkbox for automatic AI correction
        self.autoCorrectionCheckBox = QCheckBox("Enable AI Correction", self)
        self.autoCorrectionCheckBox.setGeometry(50, 250, 150, 30)  # x, y, width, height

        # Set the checkbox to be checked by default
        self.autoCorrectionCheckBox.setChecked(True)

    def updateTimer(self):
        self.timeElapsed = self.timeElapsed.addMSecs(1)
        self.timerLabel.setText(self.timeElapsed.toString("hh:mm:ss.zzz"))

    def toggleRecording(self):
        if not self.soundWaveAnimation.isVisible():
            # Start recording UI updates
            self.startButton.setText("Stop Recording")  # Change button text to 'Stop Recording'
            self.soundWaveAnimation.show()
            self.soundWaveMovie.start()
            self.timerLabel.show()
            self.timeElapsed = QTime(0, 0, 0)
            self.timer.start(1)  # Update every millisecond

            # Start the speech recorder
            self.speech_recorder.start_recording()
            # Start a thread to process the audio chunks and set it as daemon
            audio_processing_thread = threading.Thread(target=self.process_audio_chunks)
            audio_processing_thread.daemon = True
            audio_processing_thread.start()
        else:
            # Stop recording and processing
            self.startButton.setText("Start Recording")  # Change button text back to 'Start Recording'
            self.speech_recorder.stop_recording()

            # Retrieve the recognized text
            recognized_text = self.speech_recorder.get_recognized_text()
            print("Recording stopped...")
            
    def process_audio_chunks(self):
        # Process each audio chunk
        self.speech_recorder.process_audio_chunk()

    def on_recording_successful(self, recognized_text):
        # Stop recording UI updates (moved from toggleRecording)
        self.soundWaveAnimation.hide()
        self.soundWaveMovie.stop()
        self.timer.stop()
        self.timerLabel.hide()

        reply = QMessageBox.question(self, 'Recording', 'Continue with recording?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.proceedWithRecording.emit(recognized_text)  # Emit the signal with the recorded text
        else:
            self.resetUI()  # Reset the UI if the user chooses not to continue

    def on_recording_error(self):
        # Reset UI without showing any dialog and ensure no further action is taken
        self.resetUI()

    def resetUI(self):
        # Implement the method to reset UI components if needed
        # For example, resetting the startButton text, hiding animations, etc.
        self.startButton.setText("Start Recording")
        self.soundWaveAnimation.hide()
        self.soundWaveMovie.stop()
        self.timer.stop()
        self.timerLabel.hide()
        # Reset any other UI components as needed