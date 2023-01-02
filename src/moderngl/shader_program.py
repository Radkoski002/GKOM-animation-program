from pathlib import Path


class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.program = self.get_program(
            (Path(__file__).parent.parent.parent / "resources/shaders/default/default.vert").resolve(),
            (Path(__file__).parent.parent.parent / "resources/shaders/default/default.frag").resolve()
        )

    def get_program(self, v_path: str | Path, f_path: str | Path):
        with open(v_path) as f:
            v_shader = f.read()

        with open(f_path) as f:
            f_shader = f.read()

        program = self.ctx.program(vertex_shader=v_shader, fragment_shader=f_shader)
        return program
