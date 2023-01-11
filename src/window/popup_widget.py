from PyQt5.QtWidgets import QWidget, QVBoxLayout


class PopupWidget(QWidget):
    def __init__(self, widget: QWidget):
        super().__init__()
        layout = QVBoxLayout()
        self.widget = widget
        layout.addWidget(self.widget)
        self.setLayout(layout)
