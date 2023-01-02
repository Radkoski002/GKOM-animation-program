from src.moderngl.model import *

PATH = (Path(
    __file__
).parent.parent.parent / "resources/models/cube.obj").resolve()


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_objects(self, obj):
        self.objects.append(obj)

    def load(self):
        self.add_objects(Model(self.app, PATH))
        self.add_objects(Model(self.app, PATH, position=(-5, 0, 0), rotation=(45, 0, 0), scale=(1.5, 1, 1.5)))
        self.add_objects(Model(self.app, PATH, position=(5, 0, 0), rotation=(0, 45, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()

    def destroy(self):
        for obj in self.objects:
            obj.destroy()
