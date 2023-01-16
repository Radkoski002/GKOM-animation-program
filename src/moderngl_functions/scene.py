from src.moderngl_functions.model import *

PATH = (Path(
    __file__
).parent.parent.parent / "resources/models/monkey.obj").resolve()


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_objects(self, obj):
        self.objects = [obj]

    def load(self):
        self.add_objects(Model(self.app, PATH))

    def render(self):
        for obj in self.objects:
            obj.render()

    def destroy(self):
        for obj in self.objects:
            obj.destroy()
