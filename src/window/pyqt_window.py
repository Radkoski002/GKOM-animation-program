from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMenu, QAction, QFileDialog

from src.window.gl_widget import GLWidget


class PyQtWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(PyQtWindow, self).__init__()
        self.resize(1600, 900)

        self.gl_widget = GLWidget(self)
        self.setCentralWidget(self.gl_widget)
        self._createActions()
        self._connectActions()
        self._createMenuBar()

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.gl_widget.updateGL)
        timer.start()

    def newFile(self):
        print("new file")

    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", __file__, "*.obj")[0]
        print(file_name)
        self.gl_widget.addObject(file_name)

    def _createActions(self):
        self.newFileAction = QAction("New", self)
        self.openFileAction = QAction("Open", self)

    def _connectActions(self):
        self.newFileAction.triggered.connect(self.newFile)
        self.openFileAction.triggered.connect(self.openFile)

    def _createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.newFileAction)
        file_menu.addAction(self.openFileAction)
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.gl_widget.pressed_key = a0.key()

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.gl_widget.pressed_key = None

