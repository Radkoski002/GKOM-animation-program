import glm
from PyQt5 import QtCore

from src.globals import GLOBAL_VALUES


def move_element(position, app):
    up = glm.vec3(0, 1, 0)
    right = glm.vec3(1, 0, 0)
    forward = glm.vec3(0, 0, -1)
    velocity = GLOBAL_VALUES.SPEED * app.delta_time
    pressed_key = app.pressed_key
    if pressed_key == QtCore.Qt.Key_W:
        position += forward * velocity
        print(position)
    if pressed_key == QtCore.Qt.Key_S:
        position -= forward * velocity
    if pressed_key == QtCore.Qt.Key_D:
        position += right * velocity
    if pressed_key == QtCore.Qt.Key_A:
        position -= right * velocity
    if pressed_key == QtCore.Qt.Key_E:
        position += up * velocity
    if pressed_key == QtCore.Qt.Key_Q:
        position -= up * velocity
