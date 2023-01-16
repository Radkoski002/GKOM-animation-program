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
        model = pywavefront.Wavefront(self.path, create_materials=True, collect_faces=True)
        for name, material in model.materials.items():
            self.name = name
            self.ambient = glm.vec3(material.ambient)
            self.diffuse = glm.vec3(material.diffuse)
            self.specular = glm.vec3(material.specular)
            self.setVertexFormat(material.vertex_format)
            return np.array(material.vertices, dtype='f4')

    def setVertexFormat(self, format):
        if format == 'T2F_N3F_V3F':
            self.format = '2f 3f 3f'
            self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        elif format == 'N3F_V3F':
            self.format = '3f 3f'
            self.attribs = ['in_normal', 'in_position']
        elif format == 'V3F':
            self.format = '3f'
            self.attribs = ['in_position']
        else:
            raise ValueError("Unsupported vertex format")

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
