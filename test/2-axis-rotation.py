
# la prima parte, di definizione, me la copio para para tunz
# importo le librerie, mi assicuro ci siano i keyhandlers
# faccio le cose di pyglet
import pyglet
from pyglet.window import key

# fisso una resource path
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

# creo the window
window = pyglet.window.Window(800, 600, caption='2 axis rotation')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

ww = window.width
wh = window.height

# funzione per creare una label facile facile
def labeling(text,ver):
    l = pyglet.text.Label(text=text, x=10, y=ver)
    return l

# preso dall'internets, funzione per centrare un'immagine
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

# creo la barra graduata verticale, just 4 fun
# first step, carico la risorsa
bar = pyglet.resource.image('grad_bar.png')
factor = (6 * wh) / (bar.width)

center_image(bar)

ver_bar = pyglet.sprite.Sprite(img=bar,x=ww/2,y=wh/2)
ver_bar.scale = factor
ver_bar.rotation = 90

or_bar = pyglet.sprite.Sprite(img=bar,x=ww/2,y=wh/2)
or_bar.scale = factor
or_bar.rotation = 0

# definisco (male) questo strano oggetto rotante
# ha un "valore" per la rotazione sull'asse x e sull'asse y
# e ha hardcoded al suo interno una funzione di update
# per gestire il valore di questa rotazione:
# non supera mai 180 in valore assoluto
class rotating_object(object):
    # non so usare gli oggetti, per cui inizializzo brutalmente tutto a 0
    x = 0
    y = 0
    def checkbounds(self):
        if self.x > 180: self.x -= 360
        if self.x < -180: self.x += 360
        if self.y > 180: self.y -= 360
        if self.y < -180: self.y += 360

# We Are The Source
player = rotating_object()

# come conoscere rozzamente in quale degli otto quadranti siamo
# (ma se sono otto, allora sono ottanti? o sono semplicemente tanti?)
def quadrant(obj):
    q = 0
    if obj.rx >= 0 and obj.rx < 90:
        q = 1
    elif obj.rx >= 90:
        q = 2
    elif obj.rx <= -90:
        q = 3
    else:
        q = 4
    if obj.y >= 0:
        q += 4
    return str(q)

something_image = pyglet.resource.image('smiley.png')

class relative_object(pyglet.sprite.Sprite):
    rx = 160
    ry = 140
    dist = 400

something = relative_object(something_image)

# cosa devo fare ad ogni draw?
# sicuramente pulire la finestra
# poi ridisegnare dei text layer
@window.event
def on_draw():
    window.clear()
    # mi disegno due belle label per sapere quanto "vale"
    # la rotazione su ciascun asse
    labeling('x: ' + str(player.x),50).draw()
    labeling('y: ' + str(player.y),25).draw()
    # una per sapere in che quadrante sono
    labeling('quadrante: ' + quadrant(something),575).draw()
    # disegno le due aste quadrate, o come si chiamano
    ver_bar.draw()
    or_bar.draw()

def update(dt):
    # le quattro frecce si occupano di ruotare l'oggetto
    # verso l'alto e verso il basso, verso destra e verso sinistra
    if keys[key.UP]:
        player.x += 1
    if keys[key.DOWN]:
        player.x -= 1
    if keys[key.LEFT]:
        player.y += 1
    if keys[key.RIGHT]:
        player.y -= 1

    # il fatto che checkbounds sia scritta in questo modo
    # mi obbliga a chiamare esplicitamente la funzione
    # ad ogni update. si cercheranno more elegant ways
    player.checkbounds()
    ver_bar.y = factor*player.x + wh/2
    or_bar.x = factor*player.y + ww/2

    # we don't care about Euler!

# engage!
pyglet.clock.schedule(update)
pyglet.app.run()