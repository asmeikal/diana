import pyglet
from pyglet.window import key
import math
# sembra non esista una funzione segno all'interno di python
# o se ci sta, io non la trovo
def sgn(x):
    if x < 0:
        return -1
    else:
        return 1
window = pyglet.window.Window(800, 400, caption='Yet Another Space Ships Game')
# `keys` is an object that listens for keyboard events on the window
# and can be queried to find out which keys are currently pressed at any 
# time.
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
player_image = pyglet.resource.image('player-arrow.png')
# modifico l'anchor perche' sia al centro dell'immagine
player_image.anchor_x = player_image.width // 2
player_image.anchor_y = player_image.height // 2
w = window.width
h = window.height
# A `Sprite` can display an image or an animation at its own `x` and `y` 
# coordinates.
# estendo la classe di Sprite aggiungendo le due velocita'
class RotatingSprite(pyglet.sprite.Sprite):
    speed = 0
    angular_speed = 0
player = RotatingSprite(player_image)
player.x = w // 2
player.y = h // 2
@window.event
def on_draw():
    window.clear()
    player.draw()
# The `update` function will be called by pyglet every frame (due to the 
# `clock.schedule` call below). The `dt` parameter gives the number of 
# seconds passed since the last update, as a float.
def update(dt):
    # non influiamo direttamente sullo spostamento, ma
    # modifichiamo le velocita' dell'astronave
    if keys[key.W] or keys[key.UP]:
        player.speed += dt * 200
    if keys[key.S] or keys[key.DOWN]:
        player.speed -= dt * 200
    if keys[key.D] or keys[key.RIGHT]:
        player.angular_speed += dt * 20
    if keys[key.A] or keys[key.LEFT]:
        player.angular_speed -= dt * 20
    # non mi piace la parte che segue
    # abbastanza idiota e ridondante come modo per frenare l'astronave
    # sicuramente si riesce a pensare a qualcosa di piu' comodo
    if keys[key.SPACE]:
        if abs(player.speed) > 0:
            bs = sgn(player.speed)
            player.speed = bs * (abs(player.speed) - dt * 100)
            if bs != sgn(player.speed): player.speed = 0
        if abs(player.angular_speed) > 0:
            bs = sgn(player.angular_speed)
            player.angular_speed = bs * (abs(player.angular_speed) - dt * 20)
            if bs != sgn(player.angular_speed): player.angular_speed = 0
    if player.angular_speed:
        player.rotation += player.angular_speed * dt
        # conviene verificare in questo punto se la rotazione supera i limiti
        # perche' se la rotazione supera i limiti, sara' sempre dopo una variazione
        # a meno che sia possibile limitare direttamente rotation
        # all'interno della classe a cui appartiene l'astronave
        if player.rotation >= 360:
            player.rotation -= 360
        elif player.rotation < 0:
            player.rotation += 360
    if player.speed:
        # lo spostamento = velocita' * tempo viene diviso
        # nelle sue componenti x ed y
        player.x += player.speed * dt * math.cos(math.radians(player.rotation))
        player.y += player.speed * dt * math.sin(math.radians(-player.rotation))
    # se l'astronave va oltre i bordi, la riacciuffiamo
    if player.x > w:
        player.x = -20
    if player.x < -20:
        player.x = w
    if player.y > h:
        player.y = -20
    if player.y < -20:
        player.y = h
pyglet.clock.schedule(update)
pyglet.app.run()