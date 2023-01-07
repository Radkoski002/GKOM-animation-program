import moderngl as mgl

from src.moderngl.camera import Camera
from src.moderngl.light import Light
from src.moderngl.scene import Scene
from src.window.window_events import *


class Pygame_Window:
    def __init__(self, window_size=(1600, 900)):
        # Pygame init
        pg.init()
        self.WIN_SIZE = window_size

        # Pygame opengl config
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Create opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Create time variables
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Create option variables
        self.move_mode = MOVE_MODE_TYPES.CAMERA

        # Camera
        self.camera = Camera(self)
        # Light
        self.light = Light(self)
        # Scene
        self.scene = Scene(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_c:
                change_move_mode_to_camera(self)

            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                change_move_mode_to_light(self)

            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                app_exit(self)

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.scene.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.light.move()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)
