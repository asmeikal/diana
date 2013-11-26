from time import time
import image as im

class Logger(object):
    def __init__(self, victim, attrs, updates_sec=10):
        self.freq = 1.0/updates_sec
        self.victim = victim
        self.attrs = attrs
        self.start = time()
        self.lastcall = 0
        self.fname = 'log.txt'
        self.clear()
        self.f = open(self.fname,'a')
        # self.f.write('T')
        # for attr in self.attrs:
        #     self.f.write(' - ' + attr)
        # self.linebreak()
    def log(self):
        if self.currenttime() - self.lastcall > 0.1:
            self.f.write("{0:.4f}".format(time()-self.start))
            for _ in self.attrs:
                self.f.write(' : ' + "{0:.4f}".format(getattr(self.victim,_)))
            self.linebreak()
            self.lastcall = self.currenttime()
    def clear(self):
        with open(self.fname,'w') as f:
            f.write('')
    def linebreak(self):
        self.f.write('\n')
    def terminate(self):
        self.f.close()
        drawresults(self)
    def currenttime(self):
        return time() - self.start

def drawresults(arg):
    img = []
    with open(arg.fname,'r') as info:
        # titles = info.readline()
        # titles = titles.split(' - ')
        data = info.read()
    data = data.splitlines()
    for line in range(len(data)):
        data[line] = data[line].split(':')
        for n in range(len(data[line])):
            data[line][n] = float(data[line][n])
    for nn in range(1,len(data[0])):
        data_to_draw = []
        for j in range(len(data)):
            data_to_draw += [data[j][nn]]
        img += graph(data_to_draw) + create(len(data),30,(128,128,128))
    im.save('log.png',img)

def graph(data):
    data_len = len(data)
    data_max = max(data)
    data_min = min(data)
    data_delta = data_max - data_min
    if data_delta == 0: return []
    retimg = create(data_len,400,(0,0,0))
    for jj in range(0,len(retimg),40):
        for ii in range(len(retimg[0])):
            retimg[jj][ii] = (64,64,64)
    for jj in range(len(retimg[0])):
        time = max(0,int(data_len * jj / len(retimg[0]))-1)
        line = max(0,int((data[time] - data_min) * len(retimg) / data_delta) -1)
        retimg[line][jj] = (255,128,128)
    return retimg



def create(iw, ih, c):
    '''Crea e ritorna un'immagine (matrice) di larghezza iw, altezza ih
    e riempita con il colore c'''
    img = []
    for _ in range(ih):
        row = []
        for _ in range(iw):
            row.append(c)
        img.append(row)
    return img


