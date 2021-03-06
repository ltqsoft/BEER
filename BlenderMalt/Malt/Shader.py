# Copyright (c) 2020 BlenderNPR and contributors. MIT license.

from .GL import *

class Shader(object):

    def __init__(self, vertex_source, pixel_source):
        if vertex_source and pixel_source:
            self.program, self.error = compile_gl_program(vertex_source, pixel_source)
        else:
            self.program = None
            self.error = 'NO SOURCE'
        self.uniforms = {}
        self.textures = {}
        self.uniform_blocks = {}
        if self.error is None:
            self.uniforms = reflect_program_uniforms(self.program)
            texture_index = 0
            for name, uniform in self.uniforms.items():
                if uniform.is_sampler():
                    uniform.set_value(texture_index)
                    texture_index += 1 
                    self.textures[name] = None

            self.uniform_blocks = reflect_program_uniform_blocks(self.program)
        
    def bind(self):
        glUseProgram(self.program)
        for uniform in self.uniforms.values():
            uniform.bind()
        for name, texture in self.textures.items():
            glActiveTexture(GL_TEXTURE0 + self.uniforms[name].value[0])
            if texture:
                if hasattr(texture, 'bind'):
                    texture.bind()
                else: #Then it's just a externally generated bind code
                    glBindTexture(GL_TEXTURE_2D, texture)
            else:
                glBindTexture(GL_TEXTURE_2D, 0)
    
    def copy(self):
        new = Shader(None, None)
        new.program = self.program
        new.error = self.error
        for name, uniform in self.uniforms.items():
            new.uniforms[name] = uniform.copy()
        for name, texture in self.textures.items():
            new.textures[name] = texture
        for name, block in self.uniform_blocks.items():
            new.uniform_blocks[name] = block
        
        return new

