from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSlider, QSpinBox, QLabel, QColorDialog, \
    QFrame, QDoubleSpinBox

from src.window.gl_widget import GLWidget
from src.window.popup_widget import PopupWidget


def showColorWindow():
    window = PopupWidget(QColorDialog())
    window.show()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_color = (1, 1, 1)
        self.gl_widget = GLWidget(self)

        layout = QVBoxLayout()

        ambient_label = QLabel()
        ambient_label.setText("Ambient intensity:")
        layout.addWidget(ambient_label)

        ambient_spin_box = QDoubleSpinBox()
        ambient_spin_box.setDecimals(2)
        ambient_spin_box.setRange(0, 1)
        ambient_spin_box.setSingleStep(0.1)
        ambient_spin_box.setValue(0.3)
        ambient_spin_box.valueChanged.connect(self.ambientValueChanged)
        layout.addWidget(ambient_spin_box)

        diffuse_label = QLabel()
        diffuse_label.setText("Diffuse intensity:")
        layout.addWidget(diffuse_label)

        diffuse_spin_box = QDoubleSpinBox()
        diffuse_spin_box.setDecimals(2)
        diffuse_spin_box.setRange(0, 1)
        diffuse_spin_box.setSingleStep(0.1)
        diffuse_spin_box.setValue(0.8)
        diffuse_spin_box.valueChanged.connect(self.diffuseValueChanged)
        layout.addWidget(diffuse_spin_box)

        specular_label = QLabel()
        specular_label.setText("Specular intensity:")
        layout.addWidget(specular_label)

        specular_spin_box = QDoubleSpinBox()
        specular_spin_box.setDecimals(2)
        specular_spin_box.setRange(0, 1)
        specular_spin_box.setSingleStep(0.1)
        specular_spin_box.setValue(1.0)
        specular_spin_box.valueChanged.connect(self.specularValueChanged)
        layout.addWidget(specular_spin_box)

        color_window = QColorDialog()
        color_window.currentColorChanged.connect(self.colorChanged)
        layout.addWidget(color_window)

        self.dupa = QPushButton()
        self.dupa.clicked.connect(showColorWindow)
        layout.addWidget(self.dupa)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layout, 1)
        mainLayout.addWidget(self.gl_widget, 4)

        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.gl_widget.updateGL)
        timer.start()

        self.setLayout(mainLayout)

    def ambientValueChanged(self, value: float):
        self.gl_widget.light.changeAmbientValue(value)

    def diffuseValueChanged(self, value: float):
        self.gl_widget.light.changeDiffuseValue(value)

    def specularValueChanged(self, value: float):
        self.gl_widget.light.changeSpecularValue(value)

    def colorChanged(self, color: QColor):
        self.dupa.setStyleSheet(f"background-color: {color.name()}")
        current_color = tuple([tmp_color / 255 for tmp_color in color.getRgb()[:3]])
        self.gl_widget.light.changeColor(current_color)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.gl_widget.pressed_key = a0.key()

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        self.gl_widget.pressed_key = None
