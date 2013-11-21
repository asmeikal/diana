

# ordine delle sezioni

# 1) import
# 2) settings
# 3) window
# 4) utilities
# 5) asteroid class
# 6) resources
# 7) asteroids creation
# 8) draw
# 9) update
# 10) inizializzazione di pyglet

###



# import

import pyglet, random
from pyglet.window import key

from math import sin, cos, asin, acos, radians, degrees, sqrt, pi

# importo pyglet, random e varie funzioni della libreria matematica
###



# settings

fov = (radians(60),radians(40))                # field of view (or,ver)
# per capire quale sara' il campo visivo, raddoppio i valori:
# ad esempio, (60,40) mi indica 120 gradi di visuale orizzontale
# e 80 gradi di visuale verticale
turnrate = radians(1)                          # velocita' di rotazione
acc = 30                                       # accelerazione
speed = 0                                      # velocita' della nave

# per semplificare le modifiche agli attributi della nave,
# imposto qui all'inizio il mio FOV, l'accelerazione della
# nave, la velocita' di rotazione, ed inizializzo la velocita' a 0
###



# window

window = pyglet.window.Window(800, 600, caption='Asteroids')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
ww = window.width
wh = window.height

# creo una finestra 800x600
# inizializzo la parte di pyglet che tiene traccia dell'input
# da tastiera, e metto da parte larghezza e altezza della finestra
###



# utilities

def sgn(x):
    """Funzione segno di x"""
    if x < 0: return -1
    return 1

def sgn_dir(drc):
    """Restituisce 1 per movimenti verso destra o l'alto,
    -1 altrimenti"""
    if drc in ('down','left'):
        return 1
    return -1

def crd(a):
    """Funzione (goniometrica) corda"""
    return 2*sin(a/2)

def acrd(a):
    """Inverso della funzione corda"""
    return 2*asin(a/2)

def drawlabel(text,ver):
    '''Disegna un testo (text) nella finestra,
    ad altezza (ver), utile per debugging'''
    l = pyglet.text.Label(text=text, x=10, y=ver).draw()

def carnot(x,y,a):
    """Dati due lati (x ed y) di un triangolo
    qualsiasi e l'ampiezza dell'angolo (a)
    compreso fra loro, ritorna la lunghezza del terzo lato"""
    return sqrt(x**2 + y**2 - 2*x*y*cos(a))

def center_image(image):
    """Posiziona l'anchor point
    di un'immagine nel suo centro"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

def createasteroids(n):
    '''Crea n asteroidi. Ritorna una
    lista di asteroidi'''
    asteroids = []
    for _ in range(n):
        ast = Asteroid(img=asteroidimage)
        asteroids.append(ast)
    return asteroids

###



# asteroid class

class Asteroid(pyglet.sprite.Sprite):

    def __init__(self, **kwargs):
        super(Asteroid, self).__init__(**kwargs)
        # eredito attributi e metodi da pyglet.sprite.Sprite
        ###
        # da qui definisco i miei attributi per l'asteroide
        self.alpha = radians(random.randint(-180,180))      # alpha compreso fra -pi e pi
        self.beta = radians(random.randint(-90,90))         # beta compreso fra -pi/2 e pi/2
        # alpha e beta indicano la posizione relativa dell'asteroide rispetto a me
        # i valori di alpha e beta sono convertiti da subito in radianti
        # per comodita' (thanks Matteo) lavoro unicamente con i radianti
        self.distance = random.randint(10,100)
        # decoro il metodo draw() degli sprite usando "powerdrawer", definita subito dopo
        self.draw = self.powerdrawer(self.draw)

    def powerdrawer(self,func):
        """Un decoratore per impostare gli attributi
        x, y e scale dello sprite e dare l'impressione
        che questo sia effettivamente nello spazio intorno a me"""
        def inner(*args,**kwargs):
            # ad ogni draw voglio controllare che l'asteroide sia nella posizione giusta
            self.control()
            # dopodiche, modifico le coordinate x ed y dell'asteroide in base
            # ai suoi angoli alpha e beta
            self.x = self.alpha * ww/(fov[0]*2) + ww/2
            self.y = self.beta * wh/(fov[1]*2) + wh/2
            # e ne modifico le dimensioni in base alla distanza
            self.scale = 30.0/self.distance
            # le regole di prospettiva utilizzate qui sono molto banali!
            # dopo queste piccole modifiche, posso disegnare l'asteroide
            # definisco una condizione: l'asteroide deve essere nel mio campo visivo
            # risparmio molto molto lavoro, in questo modo
            if abs(self.alpha) <= fov[0] and abs(self.beta) <= fov[1]:
                _ = func(*args,**kwargs)
                return _
        return inner

    def gamma(self):
        """Determina l'angolo gamma"""
        if self.alpha == 0:
            return self.beta
        elif self.beta == 0:
            return self.alpha
        # la matematika entra in gioco solo se alpha e beta
        # sono diversi da zero
        _ = sqrt( 2 - 2 * cos(self.alpha) * cos(self.beta) )
        return 2 * asin( _ / 2 )

    def control(self):
        """Control rende ciclici i valori di alpha e beta
        e termina la 'partita' se il giocatore passa troppo
        vicino ad un asteroide"""
        # alpha ha un periodo di 2 pi greco
        # arrivato a pi o -pi, cambio segno
        if abs(self.alpha) > pi:
            self.alpha = abs(2*pi - abs(self.alpha)) * (-sgn(self.alpha))
        # beta ha un periodo di pi greco
        # arrivato a pi/2 o -pi/2, il valore di beta inverte direzione:
        # se stava aumentando, inizia a scendere, o viceversa,
        # ed eseguo una rotazione di 180 gradi dell'angolo alpha
        if abs(self.beta) > pi/2:
            self.alpha = abs(pi - abs(self.alpha)) * (-sgn(self.alpha))
            self.beta = abs(pi - abs(self.beta)) * (sgn(self.beta))
        # se sono troppo vicino ad un asteroide,
        # onde evitare divisions by zero,
        # chiudo la finestra e lascio un messaggio minaccioso
        if self.distance < 1:
            print 'Sei morto!'
            window.close()

    def rotate(self,drc):
        """Data una direzione (drc) ruoto l'astronave 
        alla velocita' di rotazione impostata
        all'inizio del file"""

        # la velocita' di rotazione e' una variabile globale
        # conviene ricordarlo a python, che e' un po' smemorato
        global turnrate

        # se sto ruotando in verticale, su beta
        # aumento o diminuisco beta a seconda se l'asteroide
        # si trova di fronte al giocatore o alle sue spalle
        if drc in ('up','down'):
            if abs(self.alpha) < pi/2:
               self.beta += turnrate * sgn_dir(drc)
            else:
               self.beta += turnrate * -sgn_dir(drc)

        # se sto ruotando in orizzontale, il lavoro e' piu' semplice
        # aumenta o diminuisce il valore di alpha
        elif drc in ('right','left'):
            self.alpha += turnrate * sgn_dir(drc)

    def move(self,dt):
        """Muovo il mondo relativamente rispetto al giocatore
        alla velocita' (speed) regolata all'inizio del file
        in avanti se la velocita' e' positiva, indietro altrimenti"""

        # ricordo a python che speed e' una variabile globale
        global speed

        # la direzione dipende dal segno di speed
        drc = sgn(speed)

        # segno la posizione dell'asteroide prima del movimento
        _distance = self.distance
        _alpha = self.alpha
        _beta = self.beta

        # spostamento = velocita' per delta-t
        ds = speed * dt

        # hic est mathematika
        # credo convenga scrivere una guida a parte
        # per spiegare le funzioni usate

        # ricalcolo la distanza
        self.distance = sqrt((self.distance)**2 + ds**2 - 2 * (self.distance) * ds * cos(self.gamma()))

        # ricalcolo beta
        self.beta = asin((sin(_beta) * _distance) / self.distance)

        #trovo le componenti delle due distanze (prima e 
        # dopo lo spostamento) sul piano di alpha
        _adist = _distance * cos(_beta)
        _adist_new = self.distance * cos(self.beta)

        # trovo il nuovo alpha
        self.alpha += acos(((_adist**2 + _adist_new**2 - ds**2)/(2 * _adist * _adist_new))%1) * sgn(_alpha) * drc

###



# resources

# carico l'immagine per gli asteroidi ('asteroid.png')
asteroidimage = pyglet.resource.image('resources/asteroid.png')
# centro lo sprite dell'asteroide
center_image(asteroidimage)

###



# asteroids creation

# creo n asteroidi (che vengono messi in una lista)
asteroids = createasteroids(100)

###



# draw

@window.event
def on_draw():
    window.clear()
    for asteroid in asteroids:
        asteroid.draw()

###



# update

def update(dt):

    # di nuovo, speed e' una variabile globale, ricordiamolo a python
    global speed

    # se viene premuta una delle frecce, l'astronave ruota nella direzione indicata
    if keys[key.UP]:
        for asteroid in asteroids:
            asteroid.rotate('up')
    if keys[key.DOWN]:
        for asteroid in asteroids:
            asteroid.rotate('down')
    if keys[key.LEFT]:
        for asteroid in asteroids:
            asteroid.rotate('left')
    if keys[key.RIGHT]:
        for asteroid in asteroids:
            asteroid.rotate('right')

    # la barra spaziatrice e C accelerano e decelerano,
    # rispettivamente, l'astronave
    if keys[key.SPACE]:
        speed += acc * dt
    if keys[key.C]:
        speed -= acc * dt

    # il tasto X frena istantaneamente l'astronave
    if keys[key.X]:
        speed = 0

    # se e' presente una velocita' (ossia mi sto muovendo)
    # chiamo la funzione per spostare gli asteroidi
    # relativamente al giocatore
    if speed:
        for asteroid in asteroids:
            asteroid.move(dt)

###



# engage!

pyglet.clock.schedule(update)
pyglet.app.run()

###

