import glm

from src.common import move_element
from src.globals import GLOBAL_VALUES

SENSITIVITY = 0.5


class Camera:
    def __init__(self, app, position=(-4, 5, -4), rot_x=45, rot_y=-45, rot_z=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]

        self.position = glm.vec3(position)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.rotate_x = rot_x
        self.rotate_y = rot_y
        self.rotate_z = rot_z

        self.m_view = self.get_view_matrix()

        self.m_proj = self.get_projection_matrix()

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        move_element(self, self.app)

    def rotate(self):
        self.rotate_x += self.app.mouse_coords[0] * SENSITIVITY
        self.rotate_y -= self.app.mouse_coords[1] * SENSITIVITY
        self.rotate_y = max(-89, min(89, self.rotate_y))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.rotate_x), glm.radians(self.rotate_y)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(GLOBAL_VALUES.FOV), self.aspect_ratio, GLOBAL_VALUES.NEAR, GLOBAL_VALUES.FAR)
