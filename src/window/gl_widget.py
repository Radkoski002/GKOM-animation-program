import moderngl as mgl
import cv2
import numpy as np

from src.globals import MOVE_MODE_TYPES, GLOBAL_VALUES
from src.moderngl_functions.camera import Camera
from src.moderngl_functions.light import Light
from src.moderngl_functions.model import Model
from src.moderngl_functions.scene import Scene

from PIL import Image
from PyQt5 import QtOpenGL, QtGui


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

        self.current_frame = 0
        self.frame_numbers = [0]
        self.frames = [
            {
                "frame": 0,
                "position": (0, 0, 0),
                "scale": (1, 1, 1),
                "rotation": (0, 0, 0)
            }
        ]
        self.rednerType = 0

    def addObject(self, path):
        self.scene.add_objects(Model(self, path))

    def changeFrame(self, frame):
        self.current_frame = frame

    def addFrame(self):
        if self.current_frame not in self.frame_numbers:
            self.frame_numbers.append(self.current_frame)
            self.frames.append({
                "frame": self.current_frame,
                "position": self.scene.objects[0].position,
                "scale": self.scene.objects[0].scale,
                "rotation": self.scene.objects[0].rotation_angles,
            })
            self.frames = sorted(self.frames, key=lambda x: x["frame"])
            self.frame_numbers.sort()
        else:
            index = self.frame_numbers.index(self.current_frame)
            self.frames[index] = {
                "frame": self.current_frame,
                "position": self.scene.objects[0].position,
                "scale": self.scene.objects[0].scale,
                "rotation": self.scene.objects[0].rotation_angles,
            }

    def changeRenderType(self, render_type):
        self.rednerType = render_type

    def update_frame(self, src_frame, dst_frame, current_frame, frames_count):

        old_position = src_frame["position"]
        new_position = dst_frame["position"]
        old_rotation = src_frame["rotation"]
        new_rotation = dst_frame["rotation"]
        old_scale = src_frame["scale"]
        new_scale = dst_frame["scale"]

        if self.rednerType == 2:
            current_position = calculate_new_vector_linear(old_position, new_position, current_frame, frames_count)
            current_rotation = calculate_new_vector_linear(old_rotation, new_rotation, current_frame, frames_count)
            current_scale = calculate_new_vector_linear(old_scale, new_scale, current_frame, frames_count)
            self.scene.objects[0].update_model_matrix(current_position, current_rotation, current_scale)
        else:
            self.scene.objects[0].update_model_matrix(new_position, new_rotation, new_scale)

    def renderToFilm(self):
        resolution = (800, 450)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("test.mp4", fourcc, GLOBAL_VALUES.FRAME_RATE, resolution)

        fbo = self.ctx.simple_framebuffer(resolution)
        fbo.use()

        if self.rednerType == 0:
            self.frames.append(self.frames[-1])
            self.frames[-1]["frame"] += 1

        for index, frame in enumerate(self.frames[1:]):
            frames_count = ((frame["frame"] - self.frames[index]["frame"]) * GLOBAL_VALUES.FRAME_RATE) \
                           // GLOBAL_VALUES.KEY_FRAMES_PER_SECOND
            src_frame = self.frames[index]
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
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))

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
