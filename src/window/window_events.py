import sys
import pygame as pg

from src.globals import MOVE_MODE_TYPES


def change_move_mode_to_camera(app):
    app.move_mode = MOVE_MODE_TYPES.CAMERA


def change_move_mode_to_light(app):
    app.move_mode = MOVE_MODE_TYPES.LIGHT


def app_exit(app):
    app.scene.destroy()
    pg.quit()
    sys.exit()
