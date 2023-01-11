from time import sleep

from PyQt5 import QtOpenGL, QtGui
import moderngl as mgl

from src.globals import MOVE_MODE_TYPES
from src.moderngl_functions.camera import Camera
from src.moderngl_functions.light import Light
from src.moderngl_functions.model import Model
from src.moderngl_functions.scene import Scene

from PIL import Image


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.ctx = None
        self.scene = None
        self.camera = None
        self.light = None
        self.pressed_key = None
        self.parent = parent

        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)
        super(GLWidget, self).__init__(fmt, None)
        self.WIN_SIZE = (1600, 900)

        self.time = 0
        self.delta_time = 20
        self.pointer_coords = (0, 0)
        self.mouse_coords = (0, 0)

        self.move_mode = MOVE_MODE_TYPES.CAMERA

    def addObject(self, path):
        self.scene.add_objects(Model(self, path))

    def renderToImage(self):
        print(self.ctx)
        fbo = self.ctx.fbo
        fbo.use()
        fbo.clear(color=(0.08, 0.16, 0.18, 1))
        self.scene.render()
        Image.frombytes("RGB", fbo.size, fbo.read(), "raw", "RGB", 0, -1).show()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.pointer_coords = (a0.x(), a0.y())

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        new_coords = ((a0.x() - self.pointer_coords[0]) / 10, (a0.y() - self.pointer_coords[1]) / 10)
        if abs(new_coords[0]) <= 1 and abs(new_coords[1]) <= 1:
            self.mouse_coords = (0, 0)
        else:
            self.mouse_coords = new_coords
            print(self.mouse_coords)
            self.pointer_coords = (a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_coords = (0, 0)
        self.pointer_coords = (0, 0)

    def scroll(self, dx: int, dy: int) -> None:
        print(dx, dy)

    def initializeGL(self) -> None:
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # Camera
        self.camera = Camera(self)
        # Light
        self.light = Light(self)
        # Scene
        self.scene = Scene(self)

    def resizeGL(self, w: int, h: int) -> None:
        self.ctx.viewport = (0, 0, self.width(), self.height())

    def paintGL(self) -> None:
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.light.move()
        self.camera.update()
        self.scene.render()
        self.ctx.finish()
