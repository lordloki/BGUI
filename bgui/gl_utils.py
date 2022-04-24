# This file provides various utility functions for OpenGL
from bgl import *

# The following line is to make ReadTheDocs happy
from bgl import glGenTextures, glDeleteTextures, glGetIntegerv, GL_NEAREST, GL_LINEAR

_glGenTextures = glGenTextures
def glGenTextures(n, textures=None):
  id_buf = Buffer(GL_INT, n)
  _glGenTextures(n, id_buf)

  if textures:
    textures.extend(id_buf.to_list())

  return id_buf.to_list()[0] if n == 1 else id_buf.to_list()


_glDeleteTextures = glDeleteTextures
def glDeleteTextures(textures):
  n = len(textures)
  id_buf = Buffer(GL_INT, n, textures)
  _glDeleteTextures(n, id_buf)


_glGetIntegerv = glGetIntegerv
def glGetIntegerv(pname):
  # Only used for GL_VIEWPORT right now, so assume we want a size 4 Buffer
  buf = Buffer(GL_INT, 4)
  _glGetIntegerv(pname, buf)
  return buf.to_list()

