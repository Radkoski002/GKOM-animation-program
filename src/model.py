from pathlib import Path

import glm

from src.shader_program import ShaderProgram
from src.vbo import ModelVBO


class Model:

    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.ctx = app.ctx
        self.model = None
        self.program = ShaderProgram(self.ctx).program
        self.position = position
        self.rotation = glm.vec3([glm.radians(angle) for angle in rotation])
        self.scale = scale
        self.vbo = ModelVBO(
            self.ctx,
            (Path(__file__).parent.parent / "resources/models/cube.obj").resolve()
        )
        self.vao = self.get_vao()
        self.camera = self.app.camera
        self.m_model = self.get_model_matrix()
        self.on_init()

    def get_model_matrix(self):
        m_model = glm.mat4()

        m_model = glm.translate(m_model, self.position)

        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))

        m_model = glm.scale(m_model, self.scale)
        return m_model

    def update(self):
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)
        self.program['light.position'].write(self.app.light.position)

    def on_init(self):
        self.program['light.ambient_intensity'].write(self.app.light.ambient_intensity)
        self.program['light.diffuse_intensity'].write(self.app.light.diffuse_intensity)
        self.program['light.specular_intensity'].write(self.app.light.specular_intensity)

        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def get_vao(self):
        vao = self.ctx.vertex_array(self.program, [(self.vbo.vbo, self.vbo.format, *self.vbo.attribs)])
        return vao

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.program.release()
        self.vbo.vbo.release()
