# show.py

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QDesktopWidget, QFrame, QHBoxLayout, QWidget, QAction, QToolBar, QToolButton, QDockWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QPen, QPixmap, QColor, QCloseEvent  # Corrected import
from PyQt5.QtCore import Qt, QSize

# Import utils functionalities
from utils.zoom import ZoomControl
from utils.re_record import RecordControl
from utils.reconcile import ReconcileControl
from utils.text_edit import TextEditTools
from utils.bottom_banner import BottomBanner

# Import ribbon functionalities
from ribbon.file import FileFunctions
from ribbon.edit import EditFunctions
from ribbon.options import OptionsFunctions
from ribbon.tools import ToolsFunctions
from ribbon.view import ViewFunctions


class TextEditor(QMainWindow):
    def __init__(self, text, file_format):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('icons/logo.ico'))

        # Initialize dock widgets at the very start
        self.rightDock = QDockWidget("Tools", self)
        self.leftDock = QDockWidget("Text Editing", self)

        # Initialize UI components
        self.initUI(text, file_format)

        # Initialize BottomBanner and add it to the status bar
        self.initBottomBanner()

        # Initialize ZoomControl, RecordControl, and ReconcileControl
        self.zoom_control = ZoomControl(self)
        self.record_control = RecordControl(self)
        self.reconcile_control = ReconcileControl(self)

        self.initDockWidgets()
        self.text_edit.textChanged.connect(self.updateWordCount)

    def initUI(self, text, file_format):
        # Main layout for QMainWindow
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create a frame to represent the paper
        paper_frame = QFrame()
        paper_frame.setStyleSheet("background-color: white; border: 1px solid lightgray; border-radius: 5px;")
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

        # Create a toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setStyleSheet("background-color: white;")
        self.addToolBar(toolbar)

        # Initialize FileFunctions with toolbar and text_edit
        self.file_functions = FileFunctions(toolbar, self.text_edit, file_format)
        self.edit_functions = EditFunctions(toolbar, self.text_edit)
        self.options_functions = OptionsFunctions(toolbar, self.text_edit)
        self.tools_functions = ToolsFunctions(toolbar, self.text_edit, self)
        self.view_functions = ViewFunctions(toolbar, self.text_edit)

        # Add the paper frame to the main layout, centered
        main_layout.addStretch()
        main_layout.addWidget(paper_frame)
        main_layout.addStretch()

        # Set a dotted background
        self.setBackground()

        # Additional UI settings (centering, etc.)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def initDockWidgets(self):
        # --------------------------------------------------------
        # Right Dock Widget for Zoom, Record, and Reconcile Controls
        # --------------------------------------------------------
        # Right Dock Widget for Zoom, Record, and Reconcile Controls
        self.rightDock = QDockWidget("Tools", self)
        self.rightDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.rightDock.setStyleSheet("QDockWidget { background: white; border: 1px solid black;}")

        # Layout for the right dock tools
        rightToolsLayout = QVBoxLayout()

        # Add zoom controls to the right tools layout
        zoomControls = self.zoom_control.create_controls()
        rightToolsLayout.addWidget(zoomControls)

        # Add record controls to the right tools layout
        recordControls = self.record_control.create_controls()
        rightToolsLayout.addWidget(recordControls)

        # Add reconcile controls to the right tools layout
        reconcileControls = self.reconcile_control.create_controls()
        rightToolsLayout.addWidget(reconcileControls)

        # Add a stretch factor at the bottom to push everything up
        rightToolsLayout.addStretch()

        # Container widget for the right dock tools
        rightContainerWidget = QWidget()
        rightContainerWidget.setLayout(rightToolsLayout)
        rightContainerWidget.setStyleSheet("QWidget { background: white; }")

        self.rightDock.setWidget(rightContainerWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightDock)

        # --------------------------------------------------------
        # Left Dock Widget for Text Editing Tools
        # --------------------------------------------------------
        # Left Dock Widget for Text Editing Tools
        self.leftDock = QDockWidget("Text Editing", self)
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.leftDock.setStyleSheet("QDockWidget { background: white; border: 1px solid black;}")

        # Initialize TextEditTools with text_edit
        self.text_edit_tools = TextEditTools(self.text_edit)

        # Use the create_controls method to get the controls for the left dock
        textEditControls = self.text_edit_tools.create_controls()

        # Ensure the container widget has the same style as the right dock
        textEditControls.setStyleSheet("QWidget { background: white; }")

        # Set the controls to the left dock widget
        self.leftDock.setWidget(textEditControls)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)

    def initBottomBanner(self):
        self.bottomBanner = BottomBanner(self)
        self.statusBar().addPermanentWidget(self.bottomBanner)  # Add BottomBanner to the status bar

        # Optionally, make the status bar opaque
        self.statusBar().setStyleSheet("QStatusBar { background-color: rgba(255, 255, 255, 0.8); }")  # Adjust opacity as needed

    def toggleRightDock(self):
        self.rightDock.setVisible(not self.rightDock.isVisible())

    def toggleLeftDock(self):
        self.leftDock.setVisible(not self.leftDock.isVisible())

    def adjustZoom(self, change):
        self.zoomLevel += change
        self.zoomLevel = max(10, min(self.zoomLevel, 200))  # Ensure zoom level stays within bounds
        font = self.text_edit.font()
        font.setPointSize(int(self.zoomLevel / 10))
        self.text_edit.setFont(font)

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

        # Save the pixmap as an image file in the 'icons' directory
        background_image_path = "icons/background.png"
        pixmap.save(background_image_path)

        # Set the pixmap as the background
        self.setStyleSheet(f"QMainWindow {{ background-image: url({background_image_path}); }}")

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, 'Save Document', 
                                     "Do you want to save your changes?", 
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            self.file_functions.saveFile()
            event.accept()  # Proceed with the closing
        elif reply == QMessageBox.No:
            event.accept()  # Proceed with the closing without saving
        else:
            event.ignore()  # Ignore the close event

    def updateWordCount(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        self.bottomBanner.updateWordCount(word_count)

# Example usage
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # Specify a default file format, e.g., '.txt'
    editor = TextEditor("i really wish i had a penguin named jim", '.txt')
    editor.show()
    sys.exit(app.exec_())