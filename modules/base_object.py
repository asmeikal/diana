from math import sin, cos, asin, acos, radians, degrees, sqrt, pi
import random

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

def create_objects(n):
    '''Crea n oggetti. Ritorna una
    lista di oggetti.'''
    _objs = []
    for _ in range(n):
        _a = random.randint(-180,180)
        _b = random.randint(-90,90)
        _d = random.randint(1,100)
        _obj = BaseObject(_a,_b,_d)
        _objs.append(_obj)
    return _objs

class BaseObject(object):
    def __init__(self,alpha,beta,distance):
        """Per inizializzare l'oggetto servono gli angoli
        alpha e beta, non espressi in radianti, ed una distanza."""
        self.alpha = radians(alpha)
        self.beta = radians(beta)
        self.distance = distance
    def coords(self,fov):
        """Ritorna una coppia di coordinate x ed y, che rappresentano
        l'oggetto rispetto al punto di vista dell'astronave. 'fov' e'
        una tupla contentente l'angolo di visuale orizzontale e l'angolo
        di visuale verticale, nell'ordine, espressi in radianti.
        NB: le coordinate vanno da -1 a 1, moltiplicandole per l'altezza
        e la larghezza della finestra si ottiene la posizione effettiva."""
        self.control()
        if abs(self.alpha) <= fov[0]/2 and abs(self.beta) <= fov[1]/2:
            x = self.alpha/(fov[0]) + 0.5
            y = self.beta/(fov[1]) + 0.5
            return x, y
        return []
    def projected_coords(self,view):
        """Restituisce una lista di quattro coordinate che rappresentano la posizione
        dell'oggetto visto dall'alto e visto lateralmente, se l'oggetto non e'
        piu' distante di 'view' dal giocatore, altrimenti ritorna una lista vuota."""
        self.control()
        if self.distance <= view:
            alpha_x = cos(self.beta) * sin(self.alpha) * self.distance
            alpha_y = cos(self.beta) * cos(self.alpha) * self.distance
            beta_x = sin(self.beta) * self.distance
            beta_y = cos(self.beta) * cos(self.alpha) * self.distance
            return [alpha_x, alpha_y, beta_x, beta_y]
        return []
    def rotate(self,drc,turnrate):
        """Data una direzione 'drc', ruota l'astronave alla velocita'
        di rotazione 'turnrate' (espressa in radianti). Le possibili direzioni
        sono: right, left, up, down, tilt_right, tilt_left."""
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
                self.alpha = (pi/2 - asin((cos(_delta) * _radius)/(cos(self.beta)*self.distance))*sgn_quad(self.alpha)*_c)*sgn(self.alpha)
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
    def move(self,speed,dt):
        """Muovo il mondo relativamente rispetto al giocatore
        alla velocita' (speed) regolata all'inizio del file
        in avanti se la velocita' e' positiva, indietro altrimenti"""
        _drc = sgn(speed)
        _distance = self.distance
        _alpha = self.alpha
        _beta = self.beta
        _ds = speed * dt
        self.distance = sqrt((self.distance)**2 + _ds**2 - 2 * (self.distance) * _ds * cos(self.gamma()))
        self.beta = asin((sin(_beta) * _distance) / self.distance)
        _adist = _distance * cos(_beta)
        _adist_new = self.distance * cos(self.beta)
        self.alpha += acos(((_adist**2 + _adist_new**2 - _ds**2)/(2 * _adist * _adist_new))) * sgn(_alpha) * _drc
    def gamma(self):
        """Determina l'angolo gamma,
        l'angolo fra il vettore direzionale del giocatore
        e la retta che lo unisce all'oggetto,
        misurato sul piano passante fra i due"""
        if self.alpha == 0:
            return self.beta
        elif self.beta == 0:
            return self.alpha
        else:
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
        if abs(self.alpha) > pi:
            self.alpha = abs(2*pi - abs(self.alpha)) * (-sgn(self.alpha))
        if abs(self.beta) > pi/2:
            self.alpha = abs(pi - abs(self.alpha)) * (-sgn(self.alpha))
            self.beta = abs(pi - abs(self.beta)) * (sgn(self.beta))
        if self.distance < 0.1:
            print 'Sei morto!'
    def __str__(self):
        _base = 'An object distant {2:.2f} units, orizontal angle {0:.2f}, elevation {1:.2f}.'
        return _base.format(degrees(self.alpha),degrees(self.beta),self.distance)





