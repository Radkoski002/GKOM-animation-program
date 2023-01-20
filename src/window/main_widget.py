from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSlider, QSpinBox, QLabel, QColorDialog, \
    QFrame, QDoubleSpinBox, QCheckBox

from src.window.gl_widget import GLWidget
from src.window.popup_widget import PopupWidget



class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_color = (1, 1, 1)
        self.gl_widget = GLWidget(self)

        self.actions = {
            "position_x": self.positionXChanged,
            "position_y": self.positionYChanged,
            "position_z": self.positionZChanged,
            "rotation_x": self.rotationXChanged,
            "rotation_y": self.rotationYChanged,
            "rotation_z": self.rotationZChanged,
            "scale_x": self.scaleXChanged,
            "scale_y": self.scaleYChanged,
            "scale_z": self.scaleZChanged,
            "ambient": self.ambientValueChanged,
            "diffuse": self.diffuseValueChanged,
            "specular": self.specularValueChanged,
            "light_pos_x": self.lightPosXChanged,
            "light_pos_y": self.lightPosYChanged,
            "light_pos_z": self.lightPosZChanged,
        }

        self.spin_boxes = {}

        # init layout
        layout = QVBoxLayout()

        # init element position layout

        element_position_layout = QHBoxLayout()

        for key, label in [
            ("position_x", "Position X:"),
            ("position_y", "Position Y:"),
            ("position_z", "Position Z:"),
        ]:
            self.createSpinBoxWithLabel(
                key,
                label,
                element_position_layout,
                decimals=1,
                value_range=(-100, 100),
                step=0.1,
                initial_value=0,
            )

        layout.addLayout(element_position_layout)

        # init element rotation layout

        element_rotation_layout = QHBoxLayout()

        for key, label in [
            ("rotation_x", "Rotation X:"),
            ("rotation_y", "Rotation Y:"),
            ("rotation_z", "Rotation Z:"),
        ]:
            self.createSpinBoxWithLabel(
                key,
                label,
                element_rotation_layout,
                decimals=1,
                value_range=(-720, 720),
                step=1,
                initial_value=0,
            )

        layout.addLayout(element_rotation_layout)

        # init element scale layout

        element_scale_layout = QHBoxLayout()

        for key, label in [
            ("scale_x", "Scale X:"),
            ("scale_y", "Scale Y:"),
            ("scale_z", "Scale Z:"),
        ]:
            self.createSpinBoxWithLabel(
                key,
                label,
                element_scale_layout,
                decimals=2,
                value_range=(0.01, 100),
                step=1,
                initial_value=1,
            )

        layout.addLayout(element_scale_layout)

        # init light position layout

        light_position_layout = QHBoxLayout()

        for key, label, init_value in [
            ("light_pos_x", "Light X:", 3),
            ("light_pos_y", "Light Y:", 3),
            ("light_pos_z", "Light Z:", -3),
        ]:
            self.createSpinBoxWithLabel(
                key,
                label,
                light_position_layout,
                decimals=1,
                value_range=(-100, 100),
                step=0.1,
                initial_value=init_value,
            )
        layout.addLayout(light_position_layout)

        # init light values layout

        light_values_layout = QHBoxLayout()

        for key, label, init_value in [
            ("ambient", "Ambient value:", 0.3),
            ("diffuse", "Diffuse value:", 0.8),
            ("specular", "Specular value:", 1.0),
        ]:
            self.createSpinBoxWithLabel(
                key,
                label,
                light_values_layout,
                decimals=2,
                value_range=(0, 1),
                step=0.1,
                initial_value=init_value,
            )
        layout.addLayout(light_values_layout)

        # init color window
        color_window = QColorDialog()
        color_window.currentColorChanged.connect(self.colorChanged)
        layout.addWidget(color_window)

        # init camera move button
        camera_move_button = QPushButton("Move camera")
        layout.addWidget(camera_move_button)

        # init frame change widgets
        frames_layout = QHBoxLayout()

        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setRange(0, 60)
        self.frame_slider.setSingleStep(1)
        self.frame_slider.valueChanged.connect(self.frameSliderChanged)
        frames_layout.addWidget(self.frame_slider)

        self.frame_spin_box = QSpinBox()
        self.frame_spin_box.setRange(0, 60)
        self.frame_spin_box.setSingleStep(1)
        self.frame_spin_box.valueChanged.connect(self.frameSpinBoxChanged)
        frames_layout.addWidget(self.frame_spin_box)

        layout.addLayout(frames_layout)

        frame_button = QPushButton()
        frame_button.setText("Add Frame")
        frame_button.clicked.connect(self.gl_widget.addFrame)
        layout.addWidget(frame_button)

        render_type_checkbox = QCheckBox()
        render_type_checkbox.setText("Linear animation")
        render_type_checkbox.stateChanged.connect(self.gl_widget.changeRenderType)
        layout.addWidget(render_type_checkbox)

        render_button = QPushButton()
        render_button.setText("Render")
        render_button.clicked.connect(self.gl_widget.renderToFilm)
        layout.addWidget(render_button)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layout, 1)
        mainLayout.addWidget(self.gl_widget, 4)

        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.gl_widget.updateGL)
        timer.start()

        self.setLayout(mainLayout)

    def createSpinBoxWithLabel(self, key, label, layout, decimals=1, value_range=(0, 1), step=1, initial_value=0):
        new_label = QLabel()
        new_label.setText(label)
        layout.addWidget(new_label)

        new_spin_box = QDoubleSpinBox()
        new_spin_box.setDecimals(decimals)
        new_spin_box.setRange(value_range[0], value_range[1])
        new_spin_box.setSingleStep(step)
        new_spin_box.setValue(initial_value)
        new_spin_box.valueChanged.connect(self.actions[key])
        layout.addWidget(new_spin_box)
        self.spin_boxes[key] = new_spin_box

    def ambientValueChanged(self, value: float):
        self.gl_widget.light.changeAmbientValue(value)

    def diffuseValueChanged(self, value: float):
        self.gl_widget.light.changeDiffuseValue(value)

    def specularValueChanged(self, value: float):
        self.gl_widget.light.changeSpecularValue(value)

    def colorChanged(self, color: QColor):
        current_color = tuple([tmp_color / 255 for tmp_color in color.getRgb()[:3]])
        self.gl_widget.light.changeColor(current_color)

    def setActiveFrame(self, value):
        self.gl_widget.current_frame = value
        new_value = 0
        for frame in self.gl_widget.frame_numbers:
            if frame <= value:
                new_value = frame
            else:
                break
        index = self.gl_widget.frame_numbers.index(new_value)
        current_frame = self.gl_widget.frames[index]
        current_position = current_frame["position"]
        current_rotation = current_frame["rotation"]
        current_scale = current_frame["scale"]
        self.gl_widget.scene.objects[0].update_model_matrix(
            new_position=current_position,
            new_rotation=current_rotation,
            new_scale=current_scale,
        )
        posX, posY, posZ = current_position
        rotX, rotY, rotZ = current_rotation
        scaleX, scaleY, scaleZ = current_scale
        self.spin_boxes["position_x"].setValue(posX)
        self.spin_boxes["position_y"].setValue(posY)
        self.spin_boxes["position_z"].setValue(posZ)
        self.spin_boxes["rotation_x"].setValue(rotX)
        self.spin_boxes["rotation_y"].setValue(rotY)
        self.spin_boxes["rotation_z"].setValue(rotZ)
        self.spin_boxes["scale_x"].setValue(scaleX)
        self.spin_boxes["scale_y"].setValue(scaleY)
        self.spin_boxes["scale_z"].setValue(scaleZ)

    def frameSliderChanged(self, value):
        self.frame_spin_box.setValue(value)
        self.setActiveFrame(value)

    def frameSpinBoxChanged(self, value):
        self.frame_slider.setValue(value)
        self.setActiveFrame(value)

    def positionXChanged(self, value):
        curX, curY, curZ = self.gl_widget.scene.objects[0].position
        self.gl_widget.scene.objects[0].update_model_matrix(new_position=(value, curY, curZ))

    def positionYChanged(self, value):
        curX, curY, curZ = self.gl_widget.scene.objects[0].position
        self.gl_widget.scene.objects[0].update_model_matrix(new_position=(curX, value, curZ))

    def positionZChanged(self, value):
        curX, curY, curZ = self.gl_widget.scene.objects[0].position
        self.gl_widget.scene.objects[0].update_model_matrix(new_position=(curX, curY, value))

    def rotationXChanged(self, value):
        rotX, rotY, rotZ = self.gl_widget.scene.objects[0].rotation_angles
        self.gl_widget.scene.objects[0].update_model_matrix(new_rotation=(value, rotY, rotZ))

    def rotationYChanged(self, value):
        rotX, rotY, rotZ = self.gl_widget.scene.objects[0].rotation_angles
        self.gl_widget.scene.objects[0].update_model_matrix(new_rotation=(rotX, value, rotZ))

    def rotationZChanged(self, value):
        rotX, rotY, rotZ = self.gl_widget.scene.objects[0].rotation_angles
        self.gl_widget.scene.objects[0].update_model_matrix(new_rotation=(rotX, rotY, value))

    def scaleXChanged(self, value):
        scaleX, scaleY, scaleZ = self.gl_widget.scene.objects[0].scale
        self.gl_widget.scene.objects[0].update_model_matrix(new_scale=(value, scaleY, scaleZ))

    def scaleYChanged(self, value):
        scaleX, scaleY, scaleZ = self.gl_widget.scene.objects[0].scale
        self.gl_widget.scene.objects[0].update_model_matrix(new_scale=(scaleX, value, scaleZ))

    def scaleZChanged(self, value):
        scaleX, scaleY, scaleZ = self.gl_widget.scene.objects[0].scale
        self.gl_widget.scene.objects[0].update_model_matrix(new_scale=(scaleX, scaleY, value))

    def lightPosXChanged(self, value):
        curX, curY, curZ = self.gl_widget.light.position
        self.gl_widget.light.updateLight(new_position=(value, curY, curZ))

    def lightPosYChanged(self, value):
        curX, curY, curZ = self.gl_widget.light.position
        self.gl_widget.light.updateLight(new_position=(curX, value, curZ))

    def lightPosZChanged(self, value):
        curX, curY, curZ = self.gl_widget.light.position
        self.gl_widget.light.updateLight(new_position=(curX, curY, value))

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.gl_widget.pressed_key = a0.key()

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        self.gl_widget.pressed_key = None
