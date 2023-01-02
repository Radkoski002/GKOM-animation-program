from enum import Enum
from prodict import Prodict


class MOVE_MODE_TYPES(Enum):
    MODEL = 0
    CAMERA = 1
    LIGHT = 2


class GLOBAL_VALUES(Prodict):
    SPEED = 0.01
    FOV = 50
    NEAR = 0.1
    FAR = 100

