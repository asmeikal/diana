import pyglet

window = pyglet.window.Window(fullscreen=True)

from modules import base_object
from pyglet.window import key
from pyglet.gl import *
import math

class Settings(object):
    def __init__(self,fov_a,rate,acc):
        self.fov = (math.radians(fov_a),math.radians(fov_a*wh/ww))
        self.turnrate = math.radians(rate)
        self.acc = acc
        self.speed = 0

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
ww = window.width
wh = window.height
current_settings = Settings(85,1,20)

objects = base_object.create_objects(500)

@window.event
def on_draw():
    global objects
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    _object_coords = []
    for _obj in objects:
        if _obj.coords(current_settings.fov):
            _x, _y = _obj.coords(current_settings.fov)
            _x *= ww
            _y *= wh
            _object_coords += [_x,_y]
    vertices_gl = (GLfloat * len(_object_coords))(*_object_coords)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
    glDrawArrays(GL_POINTS, 0, len(_object_coords) // 2)

def update(dt):
    global current_settings
    global objects
    t_rate = current_settings.turnrate
    if keys[key.SPACE]:
        current_settings.speed += current_settings.acc * dt
    if keys[key.C]:
        current_settings.speed -= current_settings.acc * dt
    if keys[key.X]:
        current_settings.speed = 0
    for _obj in objects:
        if keys[key.UP] or keys[key.W]:
            _obj.rotate('up',t_rate)
        if keys[key.DOWN] or keys[key.S]:
            _obj.rotate('down',t_rate)
        if keys[key.LEFT] or keys[key.A]:
            _obj.rotate('left',t_rate)
        if keys[key.RIGHT] or keys[key.D]:
            _obj.rotate('right',t_rate)
        if keys[key.Q]:
            _obj.rotate('tilt_left',t_rate)
        if keys[key.E]:
            _obj.rotate('tilt_right',t_rate)
        if current_settings.speed:
            _obj.move(current_settings.speed,dt)

pyglet.clock.schedule_interval(update,1/120.0)
pyglet.app.run()
