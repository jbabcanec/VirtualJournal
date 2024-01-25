# main.py

import sys
from PyQt5.QtWidgets import QApplication

from landing import LandingPage
from show import TextEditor
from mic_check import MicCheckWindow
from correct import correct_text, read_api_key

def open_text_editor(recognized_text, file_format, landing_page):
    api_key = read_api_key()
    corrected_text = recognized_text

    if api_key is not None and landing_page.autoCorrectionCheckBox.isChecked():
        corrected_text = correct_text(recognized_text, api_key)

    editor = TextEditor(corrected_text, file_format)
    editor.show()
    landing_page.close()

def main():
    app = QApplication(sys.argv)

    mic_check = MicCheckWindow()
    mic_check.show()
    if app.exec_() == 0 and not mic_check.user_accepted:
        return  # Exit if the mic check was not accepted

    landing = LandingPage()
    landing.proceedWithRecording.connect(lambda text, fmt: open_text_editor(text, fmt, landing))
    landing.show()
    app.exec_()

if __name__ == "__main__":
    main()
