from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QDesktopWidget, QFrame, QHBoxLayout, QWidget, QAction, QToolBar, QToolButton
from PyQt5.QtGui import QIcon, QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize

class TextEditor(QMainWindow):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 1000, 800)  # Adjust the size of the main window
        self.initUI(text)

        # Set the window icon
        self.setWindowIcon(QIcon('logo.ico'))

    def initUI(self, text):
        # Main layout for QMainWindow
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create a toolbar for file, edit, view, tools, and options
        toolbar = QToolBar("Main Toolbar")
        toolbar.setStyleSheet("background-color: white;")

        def create_tool_button(icon, text):
            button = QToolButton()
            button.setIcon(QIcon(icon))
            # button.setIconSize(icon_size)  # Remove this line
            button.setText(text)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Display text under the icon
            button.setStyleSheet("color: black;")
            return button

        file_button = create_tool_button('file.png', 'File')
        edit_button = create_tool_button('edit.png', 'Edit')
        view_button = create_tool_button('view.png', 'View')
        tools_button = create_tool_button('tools.png', 'Tools')
        options_button = create_tool_button('options.png', 'Options')

        toolbar.addWidget(file_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(view_button)
        toolbar.addWidget(tools_button)
        toolbar.addWidget(options_button)

        self.addToolBar(toolbar)

        # Create a frame to represent the paper
        paper_frame = QFrame()
        paper_frame.setStyleSheet("background-color: white; border: 1px solid lightgray; border-radius: 5px;")  # Subtle border added

        # Calculate the size of the frame to resemble 8.5 x 11 paper
        paper_width = int(self.width() * 0.5)  # 50% of the main window width
        paper_height = int(paper_width * 1.2941)  # 8.5 x 11 ratio
        paper_frame.setFixedSize(paper_width, paper_height)

        paper_frame_layout = QVBoxLayout(paper_frame)
        paper_frame_layout.setContentsMargins(20, 20, 20, 20)

        # Create the main text edit widget
        self.text_edit = QTextEdit()
        self.text_edit.setText(text)
        self.text_edit.setReadOnly(False)
        paper_frame_layout.addWidget(self.text_edit)

        # Add the paper frame to the main layout, centered
        main_layout.addStretch()
        main_layout.addWidget(paper_frame)
        main_layout.addStretch()

        # Set a dotted background
        self.setBackground()

        # Center the window on the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def setBackground(self):
        # Create a pixmap with a dotted pattern
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        pen = QPen(Qt.gray)  # Slightly darker shade for the dots
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        for x in range(0, 20, 10):  # Adjust dot spacing as needed
            for y in range(0, 20, 10):
                painter.drawPoint(x, y)
        painter.end()

        # Save the pixmap as an image file
        background_image_path = "background.png"
        pixmap.save(background_image_path)

        # Set the pixmap as the background
        self.setStyleSheet(f"QMainWindow {{ background-image: url({background_image_path}); }}")


# Example usage
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    editor = TextEditor("test")
    editor.show()
    sys.exit(app.exec_())
