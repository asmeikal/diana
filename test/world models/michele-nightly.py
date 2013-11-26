
# il mio obiettivo e' un ambiente con una grande quantita' di stelle
# ossia, pixel bianchi. non mi importa della distanza, sono stelle.
# non mi devo poter muovere, a questo livello.
# non hanno nessun attributo, rotazione o simile: solo una posizione
# relativa rispetto al giocatore, centro del mondo


# importo le librerie, mi assicuro ci siano i keyhandlers
import pyglet, random, math
from pyglet.window import key

# utilities
def sgn(x):
    """Troviamo il segno :P"""
    if x == 0: return 1
    return (x) / (abs(x))

def gamma(a,b):
    """Find gamma angle, given orizontal
    and vertical angles alpha (a) and beta (b).
    Gamma angle is the third vertex angle in a pyramid"""
    if a == 0:
        return b
    elif b == 0:
        return a
    corda = math.sqrt(2 - 2 * math.cos(math.radians(a)) * math.cos(math.radians(b)))
    return math.degrees(2*math.asin(corda/2))

def move(d1,a,b,dt):
    v = 100
    c = gamma(a,b)
    d2 = math.sqrt(d1**2 + (v*dt)**2 - d1*dt*v*math.cos(math.radians(c)))
    c2 = math.degrees(math.acos((d1**2 - d2**2 - (dt*v)**2)/(d2*v*dt)))
    a2 = gamma(c2,b)
    return d2, a2

# fisso una resource path
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

# creo The Window
window = pyglet.window.Window(800, 600, caption='Pingu :3')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
ww = window.width
wh = window.height

# creo un batch dove mettere tutte le stelle
asteroidbatch = pyglet.graphics.Batch()

# carico lo sprite per la stella, un pixel bianco
asteroidimage = pyglet.resource.image('asteroid.png')

# definisco una classe per le stelle
# generate casualmente
class Asteroid(pyglet.sprite.Sprite):
    '''Una stella in un punto casuale attorno all'oggetto.
    Una stella e' un oggetto posto a distanza infinita, 
    identificato solo da due angoli'''
    def __init__(self, *args, **kwargs):
        super(Asteroid, self).__init__(*args, **kwargs)
        # self.posalpha, self.posbeta = random.randint(-180,180), random.randint(-90,90)
        self.posalpha, self.posbeta = 0, 0
        self.distance = random.randint(0,500)
        self.control()
        self.dt = 0
    def control(self, *args, **kwargs):
        '''Control svolge due lavori (pessima cosa, lo so):
        controlla che gli angoli che identificano la stella
        non vadano fuori range, di fatto rendendo il mondo 
        una grande sfera, e posiziona la stella nel cielo
        rispetto al giocatore.'''
        self.posalpha = int(self.posalpha)
        self.posbeta = int(self.posbeta)
        if abs(self.posalpha) > 180:
            self.posalpha = abs(abs(self.posalpha) - 360) * (-sgn(self.posalpha))
        if abs(self.posbeta) > 90:
            self.posbeta = abs(180 - abs(self.posbeta)) * sgn(self.posbeta)
            self.posalpha = abs(180 - abs(self.posalpha)) * (-sgn(self.posalpha))
        if self.distance < 0:
            self.distance = abs(self.distance)
            self.posalpha = abs(180 - abs(self.posalpha)) * (-sgn(self.posalpha))
            self.posbeta = abs(90 - abs(self.posbeta)) * (-sgn(self.posbeta))
        self.x = self.posalpha * ww/90 + ww/2
        self.y = self.posbeta * wh/90 + wh/2
        self.scale = (2 - (self.distance/500.0))

# definisco una funzione per creare le stelle in massa
def createasteroids(n,batch=None):
    '''Crea n asteroidi e, se presente, le mette in un batch'''
    asteroids = []
    for _ in range(n):
        ast = Asteroid(img=asteroidimage,batch=batch)
        asteroids.append(ast)
    return asteroids

# chiamo la funzione, e metto le stelle (una lista di stelle)
# in una variabile. mi servira' piu' avanti
asteroids = createasteroids(1,batch=asteroidbatch)

gl = 1

@window.event
def on_draw():
    window.clear()
    # disegno le stelle, in batch
    asteroidbatch.draw()

def update(dt):
    # le quattro frecce si occupano di ruotare l'universo
    # verso l'alto e verso il basso, verso destra e verso sinistra
    if keys[key.UP] or keys[key.W]:
        for s in asteroids:
            if abs(s.posalpha) < 90:
                s.posbeta += 1
            else:
                s.posbeta -= 1
    if keys[key.DOWN] or keys[key.S]:
        for s in asteroids:
            if abs(s.posalpha) < 90:
                s.posbeta -= 1
            else:
                s.posbeta += 1
    if keys[key.LEFT] or keys[key.A]:
        for s in asteroids:
            s.posalpha -= 1
    if keys[key.RIGHT] or keys[key.D]:
        for s in asteroids:
            s.posalpha += 1
    if keys[key.SPACE]:
        for s in asteroids:
            s.distance, s.posalpha = move(s.distance,s.posalpha,s.posbeta,dt)
    for s in asteroids:
        s.control()
        s.dt = int(dt*100)/100.0

# engage!
pyglet.clock.schedule(update)
pyglet.app.run()