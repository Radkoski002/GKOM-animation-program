from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMenu, QAction, QFileDialog, QHBoxLayout, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QTimer

from src.window.gl_widget import GLWidget
from src.window.main_widget import MainWidget


class PyQtWindow(QMainWindow):

    def __init__(self):
        super(PyQtWindow, self).__init__()
        self.resize(1600, 900)
        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)
        self._createActions()
        self._connectActions()
        self._createMenuBar()

    def newFile(self):
        print("new file")

    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", __file__, "*.obj")[0]
        # if file_name:
        #     self.gl_widget.addObject(file_name)

    def saveFile(self):
        pass
        # self.gl_widget.renderToImage()

    def _createActions(self):
        self.newFileAction = QAction("New", self)
        self.openFileAction = QAction("Open", self)
        self.saveFileAction = QAction("Save", self)

    def _connectActions(self):
        self.newFileAction.triggered.connect(self.newFile)
        self.openFileAction.triggered.connect(self.openFile)
        self.saveFileAction.triggered.connect(self.saveFile)

    def _createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.newFileAction)
        file_menu.addAction(self.openFileAction)
        file_menu.addAction(self.saveFileAction)
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

