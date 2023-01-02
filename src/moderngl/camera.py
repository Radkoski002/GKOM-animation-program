import glm

from src.common import move_element
from src.globals import MOVE_MODE_TYPES, GLOBAL_VALUES


class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]

        self.position = glm.vec3(0, 0, 5)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_view = self.get_view_matrix()

        self.m_proj = self.get_projection_matrix()

    def update(self):
        self.move()
        self.m_view = self.get_view_matrix()

    def move(self):
        if self.app.move_mode == MOVE_MODE_TYPES.CAMERA:
            move_element(self.position, self.app)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(GLOBAL_VALUES.FOV), self.aspect_ratio, GLOBAL_VALUES.NEAR, GLOBAL_VALUES.FAR)
