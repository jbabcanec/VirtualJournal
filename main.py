# main.py

import sys
from PyQt5.QtWidgets import QApplication
from landing import LandingPage
from show import TextEditor  # Assuming TextEditor is a class in show.py that handles text display
from mic_check import MicCheckWindow  # Import the MicCheckWindow class

def main():
    app = QApplication(sys.argv)

    # Show the microphone check window
    mic_check = MicCheckWindow()
    mic_check.show()
    app.exec_()  # Run the application event loop

    if not mic_check.user_accepted:  # Check the flag
        return  # Exit the application if 'Cancel' was clicked

    # Show the landing page if 'OK' is clicked in the mic check window
    landing = LandingPage()
    landing.transcriptionCompleted.connect(open_text_editor)
    landing.show()
    sys.exit(app.exec_())

def open_text_editor(recognized_text):
    editor = TextEditor(recognized_text)
    editor.show()

if __name__ == "__main__":
    main()

