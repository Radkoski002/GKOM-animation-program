from pathlib import Path

import glm

from src.moderngl_functions.shader_program import ShaderProgram
from src.moderngl_functions.vbo import ModelVBO


class Model:

    def __init__(
            self,
            app,
            path: str | Path,
            position: tuple[float, float, float] = (0, 0, 0),
            rotation: tuple[float, float, float] = (0, 0, 0),
            scale: tuple[float, float, float] = (1, 1, 1)
    ):
        self.app = app
        self.ctx = app.ctx

        self.position = position
        self.rotation = glm.vec3([glm.radians(angle) for angle in rotation])
        self.scale = scale

        self.program = ShaderProgram(self.ctx).program
        self.vbo = ModelVBO(
            self.ctx,
            path
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
        self.program['light.ambient_intensity'].write(self.app.light.ambient_color)
        self.program['light.diffuse_intensity'].write(self.app.light.diffuse_color)
        self.program['light.specular_intensity'].write(self.app.light.specular_color)

    def on_init(self):
        self.program['light.ambient_intensity'].write(self.app.light.ambient_color)
        self.program['light.diffuse_intensity'].write(self.app.light.diffuse_color)
        self.program['light.specular_intensity'].write(self.app.light.specular_color)

        self.program['mat.ambient_color'].write(self.vbo.ambient)
        self.program['mat.diffuse_color'].write(self.vbo.diffuse)
        self.program['mat.specular_color'].write(self.vbo.specular)

        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def get_vao(self):
        vao = self.ctx.vertex_array(self.program, [(self.vbo.vbo, self.vbo.format, *self.vbo.attribs)])
        return vao

    def render(self):
        self.update()
        self.vao.render()

    def update_model_matrix(self, new_position=None, new_rotation=None, new_scale=None):
        if new_position:
            self.position = new_position
        if new_rotation:
            self.rotation = glm.vec3([glm.radians(angle) for angle in new_rotation])
        if new_scale:
            self.scale = new_scale

        self.m_model = self.get_model_matrix()

    def destroy(self):
        self.program.release()
        self.vbo.vbo.release()
