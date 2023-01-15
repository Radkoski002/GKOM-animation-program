import moderngl as mgl
import cv2
import numpy as np

from src.globals import MOVE_MODE_TYPES
from src.moderngl_functions.camera import Camera
from src.moderngl_functions.light import Light
from src.moderngl_functions.model import Model
from src.moderngl_functions.scene import Scene

from PIL import Image
from PyQt5 import QtOpenGL, QtGui

test_frames = [
    {
        "frame": 0,
        "position": (0, 0, 0),
        "scale": (1, 1, 1),
        "rotation": (0, 0, 0)
    },
    {
        "frame": 1,
        "position": (1, 0, 0),
        "scale": (1, 1, 1),
        "rotation": (0, 0, 0)
    },
    {
        "frame": 2,
        "position": (1, 0, 0),
        "scale": (2, 2, 2),
        "rotation": (0, 0, 0),
    },
    {
        "frame": 3,
        "position": (1, 0, 0),
        "scale": (2, 2, 2),
        "rotation": (45, 0, 0),
    },
]


def calculate_new_vector_linear(old_vector, new_vector, frame, frames):
    old_x, old_y, old_z = old_vector
    new_x, new_y, new_z = new_vector

    x = old_x + (new_x - old_x) * (frame / frames)
    y = old_y + (new_y - old_y) * (frame / frames)
    z = old_z + (new_z - old_z) * (frame / frames)

    return x, y, z


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

    def update_frame(self, src_frame, dst_frame, current_frame, frames_count):
        old_position = src_frame["position"] if "position" in src_frame else None
        new_position = dst_frame["position"] if "position" in dst_frame else None
        old_rotation = src_frame["rotation"] if "rotation" in src_frame else None
        new_rotation = dst_frame["rotation"] if "rotation" in dst_frame else None
        old_scale = src_frame["scale"] if "scale" in src_frame else None
        new_scale = dst_frame["scale"] if "scale" in dst_frame else None
        current_position = calculate_new_vector_linear(old_position, new_position, current_frame, frames_count) \
            if old_position and new_position else None
        current_rotation = calculate_new_vector_linear(old_rotation, new_rotation, current_frame, frames_count) \
            if old_rotation and new_rotation else None
        current_scale = calculate_new_vector_linear(old_scale, new_scale, current_frame, frames_count) \
            if old_scale and new_scale else None
        self.scene.objects[0].update_model_matrix(current_position, current_rotation, current_scale)
        pass

    def renderToImage(self):
        frame_rate = 24
        resolution = (800, 450)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("test.mp4", fourcc, frame_rate, resolution)

        fbo = self.ctx.simple_framebuffer(resolution)
        fbo.use()

        for index, frame in enumerate(test_frames[1:]):
            frames_count = (frame["frame"] - test_frames[index]["frame"]) * frame_rate
            src_frame = test_frames[index]
            dst_frame = frame
            for i in range(frames_count):
                fbo.clear(color=(0.08, 0.16, 0.18, 1))
                self.update_frame(src_frame, dst_frame, i, frames_count)
                self.scene.render()
                image = Image.frombytes("RGB", fbo.size, fbo.read(), "raw", "RGB", 0, -1)
                out.write(np.array(image))
        out.release()
        fbo.release()
        self.ctx.viewport = (0, 0, self.width(), self.height())

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.pointer_coords = (a0.x(), a0.y())

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        new_coords = ((a0.x() - self.pointer_coords[0]) / 10, (a0.y() - self.pointer_coords[1]) / 10)
        if abs(new_coords[0]) <= 1 and abs(new_coords[1]) <= 1:
            self.mouse_coords = (0, 0)
        else:
            self.mouse_coords = new_coords
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
