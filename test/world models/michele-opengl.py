

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
# from modules import debugger
from pyglet.gl import *

from math import sin, cos, asin, acos, radians, degrees, sqrt, pi

def arc_check(func):
    """Controlla che l'argomento delle inverse delle
    funzioni goniometriche rientri nel dominio."""
    def inner(x):
        x = min(1,max(x,-1))
        _ = func(x)
        return _
    return inner

acos = arc_check(acos)
asin = arc_check(asin)

# importo pyglet, random e varie funzioni della libreria matematica
###



# settings

fov = (radians(30),radians(20))                # field of view (or,ver)
# per capire quale sara' il campo visivo, raddoppio i valori:
# ad esempio, (60,40) mi indica 120 gradi di visuale orizzontale
# e 80 gradi di visuale verticale
turnrate = radians(1.0/4)                          # velocita' di rotazione
acc = 20                                       # accelerazione
speed = 0                                      # velocita' della nave

# per semplificare le modifiche agli attributi della nave,
# imposto qui all'inizio il mio FOV, l'accelerazione della
# nave, la velocita' di rotazione, ed inizializzo la velocita' a 0
###



# window

window = pyglet.window.Window(fullscreen=True)
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

def sgn_quad(a):
    """Funzione "segno del quadrante":
    restituisce 1 se l'oggetto si trova di fronte
    al giocatore, -1 se si trova alle spalle"""
    if abs(a) < pi/2:
        return 1
    return -1

def sgn_dir(drc):
    """Restituisce 1 per movimenti verso destra o l'alto,
    -1 altrimenti"""
    if drc in ('down','left','tilt_left'):
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
        ast = Asteroid()
        asteroids.append(ast)
    return asteroids

###



# asteroid class

class Asteroid(object):

    def __init__(self, **kwargs):
        # eredito attributi e metodi da pyglet.sprite.Sprite
        ###
        # da qui definisco i miei attributi per l'asteroide
        self.alpha = radians(random.randint(-180,180))      # alpha compreso fra -pi e pi
        self.beta = radians(random.randint(-90,90))         # beta compreso fra -pi/2 e pi/2
        # alpha e beta indicano la posizione relativa dell'asteroide rispetto a me
        # i valori di alpha e beta sono convertiti da subito in radianti
        # per comodita' (thanks Matteo) lavoro unicamente con i radianti
        self.distance = random.randint(1,200)
        # decoro il metodo draw() degli sprite usando "powerdrawer", definita subito dopo

    def coords(self):
        self.control()
        if abs(self.alpha) <= fov[0] and abs(self.beta) <= fov[1]:
            x = sin(self.alpha) * ww/(fov[0]*2) + ww/2
            y = sin(self.beta) * wh/(fov[1]*2) + wh/2
            return x, y
        return []

    def projected_coords(self):
        """Imposto le coordinate alpha e beta"""
        self.control()
        alpha_x = cos(self.beta) * sin(self.alpha) * self.distance + ww/4
        alpha_y = cos(self.beta) * cos(self.alpha) * self.distance + wh/2
        beta_x = sin(self.beta) * self.distance + 3*ww/4
        beta_y = cos(self.beta) * cos(self.alpha) * self.distance + wh/2
        return alpha_x, alpha_y, beta_x, beta_y

    def gamma(self):
        """Determina l'angolo gamma,
        l'angolo fra il vettore direzionale del giocatore
        e la retta che lo unisce all'oggetto,
        misurato sul piano passante fra i due"""
        if self.alpha == 0:
            return self.beta
        elif self.beta == 0:
            return self.alpha
        # la matematika entra in gioco solo se alpha e beta
        # sono diversi da zero
        _ = sqrt( 2 - 2 * cos(self.alpha) * cos(self.beta))
        return 2 * asin( _ / 2 )

    def delta(self):
        """Determina l'angolo delta, ed il raggio
        del cerchio che lo descrive"""
        def angle():
            if self.beta == 0 or self.alpha == 0:
                return self.beta
            elif abs(self.alpha) == pi/2:
                return pi/2 * sgn(self.beta)
            return asin((_x/_radius))
        _x = sin(self.beta) * self.distance
        _y = cos(self.beta) * self.distance * cos(self.alpha)
        _radius = sqrt(_x**2 + _y**2)
        return angle(), _radius

    def epsilon(self):
        """Determina l'angolo epsilon, ed il raggio
        del cerchio che lo descrive"""
        def angle():
            if self.beta == 0 or abs(self.alpha) == pi/2:
                return self.beta
            elif self.alpha == 0:
                return pi/2 * sgn(self.beta)
            return asin((_x/_radius))
        _x = sin(self.beta) * self.distance
        _y = cos(self.beta) * self.distance * sin(self.alpha)
        _radius = sqrt(_x**2 + _y**2)
        return angle(), _radius

    def control(self):
        """Control rende ciclici i valori di alpha e beta
        e termina la 'partita' se il giocatore passa troppo
        vicino ad un asteroide"""
        if abs(self.beta) == pi/2:
            self.alpha = 0
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
        if self.distance < 0.1:
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
        if drc in ('right','left'):
            self.alpha += turnrate * sgn_dir(drc)

        elif drc in ('up','down'):
            _delta, _radius = self.delta()
            _delta += turnrate * sgn_quad(self.alpha) * sgn_dir(drc)
            _c = 1
            if abs(_delta) >= pi/2:
                _delta = abs(pi - abs(_delta)) * sgn(_delta)
                _c *= -1
            self.beta = asin((_radius * sin(_delta))/self.distance)
            if self.alpha not in (-pi,0,pi):
                self.alpha = (pi/2 - asin((cos(_delta) * _radius) / (cos(self.beta) * self.distance)) * sgn_quad(self.alpha) * _c)*sgn(self.alpha)
            if abs(self.beta) >= pi/2:
                self.alpha = abs(pi - abs(self.alpha)) * (-sgn(self.alpha))

        elif drc in ('tilt_right','tilt_left'):
            _epsilon, _radius = self.epsilon()
            _epsilon += turnrate * sgn(self.alpha) * sgn_dir(drc)
            _q = sgn_quad(self.alpha)
            if abs(_epsilon) == pi/2:
                self.beta = asin(_radius/self.distance)
                self.alpha = (pi/2 - pi/2*_q)
            else:
                self.beta = asin(_radius*sin(_epsilon)/self.distance)
                self.alpha = asin((cos(_epsilon)*_radius)/(cos(self.beta)*self.distance)) * sgn(self.alpha)
                if _q < 0:
                    self.alpha = abs(pi - abs(self.alpha)) * sgn(self.alpha)

        # se sto ruotando in orizzontale, il lavoro e' piu' semplice
        # aumenta o diminuisce il valore di alpha

    def move(self,speed,dt):
        """Muovo il mondo relativamente rispetto al giocatore
        alla velocita' (speed) regolata all'inizio del file
        in avanti se la velocita' e' positiva, indietro altrimenti"""

        # la direzione dipende dal segno di speed
        _drc = sgn(speed)

        # segno la posizione dell'asteroide prima del movimento
        _distance = self.distance
        _alpha = self.alpha
        _beta = self.beta

        # spostamento = velocita' per delta-t
        _ds = speed * dt

        # hic est mathematika
        # credo convenga scrivere una guida a parte
        # per spiegare le funzioni usate

        # ricalcolo la distanza
        self.distance = sqrt((self.distance)**2 + _ds**2 - 2 * (self.distance) * _ds * cos(self.gamma()))

        # ricalcolo beta
        self.beta = asin((sin(_beta) * _distance) / self.distance)

        #trovo le componenti delle due distanze (prima e 
        # dopo lo spostamento) sul piano di alpha
        _adist = _distance * cos(_beta)
        _adist_new = self.distance * cos(self.beta)

        # trovo il nuovo alpha
        self.alpha += acos(((_adist**2 + _adist_new**2 - _ds**2)/(2 * _adist * _adist_new))) * sgn(_alpha) * _drc

###



# asteroids creation

# creo n asteroidi (che vengono messi in una lista)
asteroids = createasteroids(1000)

###



# draw

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    ast_coords = []
    for asteroid in asteroids:
        ast_coords += list(asteroid.coords())
    vertices_gl = (GLfloat * len(ast_coords))(*ast_coords)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
    glDrawArrays(GL_POINTS, 0, len(ast_coords) // 2)

###



# update

def update(dt):

    # di nuovo, speed e' una variabile globale, ricordiamolo a python
    global speed

    # se viene premuta una delle frecce, l'astronave ruota nella direzione indicata
    if keys[key.UP] or keys[key.W]:
        for asteroid in asteroids:
            asteroid.rotate('up')
    if keys[key.DOWN] or keys[key.S]:
        for asteroid in asteroids:
            asteroid.rotate('down')
    if keys[key.LEFT] or keys[key.A]:
        for asteroid in asteroids:
            asteroid.rotate('left')
    if keys[key.RIGHT] or keys[key.D]:
        for asteroid in asteroids:
            asteroid.rotate('right')
    if keys[key.Q]:
        for asteroid in asteroids:
            asteroid.rotate('tilt_left')
    if keys[key.E]:
        for asteroid in asteroids:
            asteroid.rotate('tilt_right')

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
            asteroid.move(speed,dt)

###



# engage!

pyglet.clock.schedule_interval(update,1/120.0)
pyglet.app.run()

###

