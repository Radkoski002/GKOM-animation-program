from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_objects(self, obj):
        self.objects.append(obj)

    def load(self):
        self.add_objects(Model(self.app))
        self.add_objects(Model(self.app, position=(-5, 0, 0), rotation=(45, 0, 0), scale=(1.5, 1, 1.5)))
        self.add_objects(Model(self.app, position=(5, 0, 0), rotation=(0, 45, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()

    def destroy(self):
        for obj in self.objects:
            obj.destroy()
