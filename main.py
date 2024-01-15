# main.py

import sys
from PyQt5.QtWidgets import QApplication

from landing import LandingPage
from show import TextEditor
from mic_check import MicCheckWindow
from correct import correct_text, read_api_key

# Declare editor as a global variable
global editor

def main():
    app = QApplication(sys.argv)

    # Show the microphone check window
    mic_check = MicCheckWindow()
    mic_check.show()
    app.exec_()  # Run the application event loop

    if not mic_check.user_accepted:  # Check the flag
        return  # Exit the application if 'Cancel' was clicked

    # Show the landing page if 'OK' is clicked in the mic check window
    global landing
    landing = LandingPage()
    landing.proceedWithRecording.connect(lambda text: open_text_editor(text, landing))
    landing.show()
    app.exec_()

def open_text_editor(recognized_text, landing_page):
    global editor

    api_key = read_api_key()
    if api_key is None:
        print("API key not found. Unable to perform AI correction.")
        corrected_text = recognized_text  # Use the original text if API key is missing
    elif landing_page.autoCorrectionCheckBox.isChecked():
        corrected_text = correct_text(recognized_text, api_key)
    else:
        corrected_text = recognized_text

    editor = TextEditor(corrected_text)
    editor.show()
    landing_page.close()  # Close the LandingPage window

if __name__ == "__main__":
    main()
