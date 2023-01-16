import glm

from src.common import move_element
from src.globals import MOVE_MODE_TYPES


class Light:

    def __init__(self, app, position=(3, 3, -3), color=(1, 1, 1)):
        self.ambient_color = None
        self.diffuse_color = None
        self.specular_color = None

        self.app = app

        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        self.ambient_intensity = 0.3
        self.diffuse_intensity = 0.8
        self.specular_intensity = 1.0

        self.update()

    def move(self):
        if self.app.move_mode == MOVE_MODE_TYPES.LIGHT:
            move_element(self.position, self.app)

    def updateLight(self, new_position=None, new_color=None):
        if new_position:
            self.position = glm.vec3(new_position)
        if new_color:
            self.color = glm.vec3(new_color)

        self.update()

    def changeColor(self, color):
        self.color = glm.vec3(color)
        self.update()

    def changeAmbientValue(self, value: float):
        self.ambient_intensity = value
        self.update()

    def changeDiffuseValue(self, value: float):
        self.diffuse_intensity = value
        self.update()

    def changeSpecularValue(self, value: float):
        self.specular_intensity = value
        self.update()

    def update(self):
        self.ambient_color = self.ambient_intensity * self.color
        self.diffuse_color = self.diffuse_intensity * self.color
        self.specular_color = self.specular_intensity * self.color
