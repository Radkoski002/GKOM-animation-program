from pathlib import Path

import glm
import numpy as np
import pywavefront


class ModelVBO:
    def __init__(self, ctx, path: str | Path):
        self.ctx = ctx
        self.path = path
        self.name = ""
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.vbo = self.get_vbo()

    def get_vertex_data(self):
        model = pywavefront.Wavefront(self.path)
        for name, material in model.materials.items():
            self.name = name
            self.ambient = glm.vec3(material.ambient)
            self.diffuse = glm.vec3(material.diffuse)
            self.specular = glm.vec3(material.specular)
            return np.array(material.vertices, dtype='f4')

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
