import glm

from src.common import move_element
from src.globals import MOVE_MODE_TYPES


class Light:

    def __init__(self, app, position=(3, 3, -3), color=(1, 1, 1)):
        self.app = app

        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.ambient_intensity = 0.3 * self.color
        self.diffuse_intensity = 0.8 * self.color
        self.specular_intensity = 1.0 * self.color

    def move(self):
        if self.app.move_mode == MOVE_MODE_TYPES.LIGHT:
            move_element(self.position, self.app)
