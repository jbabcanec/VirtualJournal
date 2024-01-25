# show.py

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QDesktopWidget, QFrame, QHBoxLayout, QWidget, QAction, QToolBar, QToolButton, QDockWidget, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize

# Import utils functionalities
from utils.zoom import ZoomControl
from utils.re_record import RecordControl
from utils.reconcile import ReconcileControl
from utils.text_edit import TextEditTools

# Import ribbon functionalities
from ribbon.file import FileFunctions
from ribbon.edit import EditFunctions
from ribbon.options import OptionsFunctions
from ribbon.tools import ToolsFunctions
from ribbon.view import ViewFunctions


class TextEditor(QMainWindow):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('icons/logo.ico'))

        # Initialize UI components
        self.initUI(text)

        # Initialize ZoomControl and create dock widgets
        self.zoom_control = ZoomControl(self)
        self.record_control = RecordControl(self)
        self.reconcile_control = ReconcileControl(self)

        self.initDockWidgets()

    def initUI(self, text):
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
        self.file_functions = FileFunctions(toolbar, self.text_edit)
        self.edit_functions = EditFunctions(toolbar, self.text_edit)
        self.options_functions = OptionsFunctions(toolbar, self.text_edit)
        self.tools_functions = ToolsFunctions(toolbar, self.text_edit)
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
        rightDock = QDockWidget("Right Tools", self)
        rightDock.setAllowedAreas(Qt.RightDockWidgetArea)
        rightDock.setStyleSheet("QDockWidget { background: white; border: 1px solid black;}")

        # Layout for the right dock tools
        rightToolsLayout = QVBoxLayout()

        # Add a stretch factor at the top
        rightToolsLayout.addStretch()

        # Add zoom controls to the right tools layout
        zoomControls = self.zoom_control.create_controls()
        rightToolsLayout.addWidget(zoomControls)

        # Add record controls to the right tools layout
        recordControls = self.record_control.create_controls()
        rightToolsLayout.addWidget(recordControls)

        # Add reconcile controls to the right tools layout
        reconcileControls = self.reconcile_control.create_controls()
        rightToolsLayout.addWidget(reconcileControls)

        # Add a stretch factor at the bottom
        rightToolsLayout.addStretch()

        # Container widget for the right dock tools
        rightContainerWidget = QWidget()
        rightContainerWidget.setLayout(rightToolsLayout)
        rightContainerWidget.setStyleSheet("QWidget { background: white; }")

        rightDock.setWidget(rightContainerWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, rightDock)

        # --------------------------------------------------------
        # Left Dock Widget for Text Editing Tools
        # --------------------------------------------------------
        leftDock = QDockWidget("Text Editing Tools", self)
        leftDock.setAllowedAreas(Qt.LeftDockWidgetArea)
        leftDock.setStyleSheet("QDockWidget { background: white; border: 1px solid black;}")

        # Initialize TextEditTools with text_edit
        self.text_edit_tools = TextEditTools(self.text_edit)

        # Use the create_controls method to get the controls for the left dock
        textEditControls = self.text_edit_tools.create_controls()

        # Ensure the container widget has the same style as the right dock
        textEditControls.setStyleSheet("QWidget { background: white; }")

        # Set the controls to the left dock widget
        leftDock.setWidget(textEditControls)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)

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
        
# Example usage
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    editor = TextEditor("i really wish i had a penguin named jim")
    editor.show()
    sys.exit(app.exec_())
