import glm
import pygame as pg
from src.globals import GLOBAL_VALUES


def move_element(position, app):
    up = glm.vec3(0, 1, 0)
    right = glm.vec3(1, 0, 0)
    forward = glm.vec3(0, 0, -1)
    velocity = GLOBAL_VALUES.SPEED * app.delta_time
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        position += forward * velocity
    if keys[pg.K_s]:
        position -= forward * velocity
    if keys[pg.K_d]:
        position += right * velocity
    if keys[pg.K_a]:
        position -= right * velocity
    if keys[pg.K_q]:
        position += up * velocity
    if keys[pg.K_e]:
        position -= up * velocity
