
# il mio obiettivo e' un ambiente con una grande quantita' di stelle
# ossia, pixel bianchi. non mi importa della distanza, sono stelle.
# non mi devo poter muovere, a questo livello.
# non hanno nessun attributo, rotazione o simile: solo una posizione
# relativa rispetto al giocatore, centro del mondo


# importo le librerie, mi assicuro ci siano i keyhandlers
import pyglet, random
from pyglet.window import key

# fisso una resource path
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

# creo The Window
window = pyglet.window.Window(800, 600, caption='A world of stars')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
ww = window.width
wh = window.height

# creo un batch dove mettere tutte le stelle
starbatch = pyglet.graphics.Batch()

# carico lo sprite per la stella, un pixel bianco
starimage = pyglet.resource.image('star.png')

# definisco una classe per le stelle
# generate casualmente
class Star(pyglet.sprite.Sprite):
    '''Una stella in un punto casuale attorno all'oggetto.
    Una stella e' un oggetto posto a distanza infinita, 
    identificato solo da due angoli'''
    def __init__(self, *args, **kwargs):
        super(Star, self).__init__(*args, **kwargs)
        self.posalpha, self.posbeta = random.randint(-180,180), random.randint(-180,180)
        self.control()
    def control(self,*args,**kwargs):
        '''Control svolge due lavori (pessima cosa, lo so):
        controlla che gli angoli che identificano la stella
        non vadano fuori range, di fatto rendendo il mondo 
        una grande sfera, e posiziona la stella nel cielo
        rispetto al giocatore.'''
        if abs(self.posalpha) > 180: self.posalpha = abs(abs(self.posalpha)-360) * self.posalpha/abs(self.posalpha) * (-1)
        if abs(self.posbeta) > 180: self.posbeta = abs(abs(self.posbeta)-360) * self.posbeta/abs(self.posbeta) * (-1)
        self.x = self.posalpha * ww/180 + ww/2
        self.y = self.posbeta * wh/180 + wh/2

# definisco una funzione per creare le stelle in massa
def createstars(n,batch=None):
    '''Crea n stelle e, se presente, le mette in un batch'''
    starslist = []
    for _ in range(n):
        star = Star(img=starimage,batch=batch)
        starslist.append(star)
    return starslist

# chiamo la funzione, e metto le stelle (una lista di stelle)
# in una variabile. mi servira' piu' avanti
starscreation = createstars(500,batch=starbatch)

@window.event
def on_draw():
    window.clear()
    # disegno le stelle, in batch
    starbatch.draw()

def update(dt):
    # le quattro frecce si occupano di ruotare l'universo
    # verso l'alto e verso il basso, verso destra e verso sinistra
    if keys[key.UP] or keys[key.W]:
        for s in starscreation:
            s.posbeta += 1
            s.control()
    if keys[key.DOWN] or keys[key.S]:
        for s in starscreation:
            s.posbeta -= 1
            s.control()
    if keys[key.LEFT] or keys[key.A]:
        for s in starscreation:
            s.posalpha -= 1
            s.control()
    if keys[key.RIGHT] or keys[key.D]:
        for s in starscreation:
            s.posalpha += 1
            s.control()
    # if keys[key.Q]:
    #     for s in starscreation:
    #         s.posalpha += 1
    #         s.posbeta -= 1
    #         s.control()
    # if keys[key.E]:
    #     for s in starscreation:
    #         s.posalpha -= 1
    #         s.posbeta += 1
    #         s.control()

# engage!
pyglet.clock.schedule(update)
pyglet.app.run()