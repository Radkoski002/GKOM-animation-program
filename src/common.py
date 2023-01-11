from PyQt5 import QtCore

from src.globals import GLOBAL_VALUES


def move_element(element, app):
    velocity = GLOBAL_VALUES.SPEED * app.delta_time
    pressed_key = app.pressed_key
    if pressed_key == QtCore.Qt.Key_W:
        element.position += element.forward * velocity
    if pressed_key == QtCore.Qt.Key_S:
        element.position -= element.forward * velocity
    if pressed_key == QtCore.Qt.Key_D:
        element.position += element.right * velocity
    if pressed_key == QtCore.Qt.Key_A:
        element.position -= element.right * velocity
    if pressed_key == QtCore.Qt.Key_E:
        element.position += element.up * velocity
    if pressed_key == QtCore.Qt.Key_Q:
        element.position -= element.up * velocity
