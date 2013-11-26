import pyglet
from pyglet.window import key
from pyglet.gl import *
import random
from math import sin, cos, asin, acos, radians, degrees, sqrt, pi

window = pyglet.window.Window(800,600)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

class BaseObject(object):
    def __init__(self):
        self.x = random.randint(-500,500)
        self.y = random.randint(-500,500)
        self.z = random.randint(-500,500)

class Player(BaseObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0

class Asteroid(BaseObject):
    def __init__(self):
        super(Asteroid,self).__init__()

def create_asteroids(n):
    astlst = []
    for _ in range(n):
        astlst.append(Asteroid())
    return astlst

asteroids = create_asteroids(20)

@window.event
def on_draw():
    ast_coords = []
    for asteroid in asteroids:
        ast_coords += [asteroid.x, asteroid.y]
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    vertices_gl = (GLfloat * len(ast_coords))(*ast_coords)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
    glDrawArrays(GL_POINTS, 0, len(ast_coords) // 2)

def update(dt):
    pass

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()
