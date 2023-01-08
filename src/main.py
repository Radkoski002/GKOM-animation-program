from PyQt5 import QtWidgets
import sys
from src.window.pyqt_window import PyQtWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = PyQtWindow()
    win.show()

    sys.exit(app.exec())

    # new_window = Pygame_Window()
    # new_window.run()
