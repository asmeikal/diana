import png

def create(iw, ih, c):
    '''Crea e ritorna un'immagine di larghezza iw, altezza ih e con
    tutti i pixels di colore c'''
    img = []
    for _ in range(ih):
        row = []
        for _ in range(iw):
            row.append(c)
        img.append(row)
    return img

def _topng(img):
    png_img = []
    for row in img:
        png_row = []
        for c in row:
             png_row += c
        png_img.append(png_row)
    return png_img

def save(filename, img):
    '''Converte l'immagine img nel formato PNG e la salva nel file filename'''
    png_img = _topng(img)
    with open(filename,'wb') as f:
        png.Writer(len(img[0]),len(img)).write(f,png_img)

def load(filename):
    '''Carica l'immagine in formato PNG dal file filename, la converte nel
    formato a matrice di tuple e la ritorna'''
    with open(filename,'rb') as f:
        iw, ih, png_img, _ = png.Reader(file=f).asRGB8()
        png_img = [ [ v for v in png_row ] for png_row in png_img ]
    img = []
    for png_row in png_img:
        row = []
        for i in range(0,len(png_row),3):
            row.append( (png_row[i+0],png_row[i+1],png_row[i+2]) )
        img.append( row )
    return img

def visf(filename):
    '''Visualizza inline sulla shell di IPython l'immagine in formato PNG
    contenuta nel file filename'''
    import IPython.display as ipd
    ipd.display_png(ipd.Image(filename=filename))

def visd(img):
    '''Visualizza inline sulla shell di IPython l'immagine img, nel formato
    a matrice di tuple'''
    import io, png
    import IPython.display as ipd
    png_img = _topng(img)
    bf = io.BytesIO()
    png.Writer(len(img[0]), len(img)).write(bf, png_img)
    ipd.clear_output()
    ipd.display_png(bf.getvalue(), raw=True)
    
def visq(img, title=''):
    '''Visualizza l'immagine img, nel formato a matrice di tuple, dalla shell
    di IPython in una finestra separata. Utile per fare anumazioni.'''
    import matplotlib.pyplot as plt
    import io, png
    png_img = _topng(img)
    bf = io.BytesIO()
    png.Writer(len(img[0]), len(img)).write(bf, png_img)
    bf.seek(0)
    image = plt.imread(bf)
    plt.axis('off')
    plt.title(title)
    plt.imshow(image)
    plt.pause(0.1)

def inside(img, i, j):
    '''Ritorna True se il pixel (i, j) e' dentro l'immagine img, False
    altrimenti'''
    iw, ih = len(img[0]), len(img)
    return 0 <= i < iw and 0 <= j < ih

def draw_quad_simple(img, x, y, w, h, c):
    '''Disegna su img un rettangolo con lo spigolo in alto a sinistra in (x, y),
    larghezza w, altezza h e di colore c. Va in errore se il rettangolo
    fuoriesce dall'immagine.'''
    for j in range(y,y+h):
        for i in range(x,x+w):
            img[j][i] = c

def draw_quad(img, x ,y, w, h, c):
    '''Disegna su img un rettangolo con lo spigolo in alto a sinistra in (x, y),
    larghezza w, altezza h e di colore c. Disegna solamente la parte del
    rettangolo che e' dentro l'immagine.'''
    for j in range(y,y+h):
        for i in range(x,x+w):
            if inside(img,i,j):
                img[j][i] = c

def draw_checkers(img, s, c0, c1):
    '''Disegna su img una scacchiera di celle di dimensione s colorate in
    modo alternato c0 e c1'''
    for jj in range(len(img)/s):
        for ii in range(len(img[0])/s):
            if (ii + jj) % 2: c = c1
            else: c = c0
            draw_quad(img,ii*s,jj*s,s,s,c)

def draw_gradient_h(img, c0, c1):
    '''Disegna su img un gradiente di colore da sinistra a destra, dal
    colore c0 al colore c1'''
    r0, g0, b0 = c0
    r1, g1, b1 = c1
    for j in range(len(img)):
        for i in range(len(img[0])):
            u = float(i) / float(len(img[0]))
            r = round(r0 * (1-u) + r1 * u)
            g = round(g0 * (1-u) + g1 * u)
            b = round(b0 * (1-u) + b1 * u)
            img[j][i] = (r,g,b)

def draw_gradient_v(img, c0, c1):
    '''Disegna su img un gradiente di colore dall'alto in basso, dal
    colore c0 al colore c1'''
    r0, g0, b0 = c0
    r1, g1, b1 = c1
    for j in range(len(img)):
        for i in range(len(img[0])):
            v = float(j) / float(len(img))
            r = round(r0 * (1-v) + r1 * v)
            g = round(g0 * (1-v) + g1 * v)
            b = round(b0 * (1-v) + b1 * v)
            img[j][i] = (r,g,b)

def draw_gradient_quad(img, c00, c01, c10, c11):
    '''Disegna un gradiente di colore combinato orizzontale e verticale
    con c00 in alto a sinistra, c01 in basso a sinistra, c10 in alto a destra
    e c11 in basso a destra'''
    for j in range(len(img)):
        for i in range(len(img[0])):
            u = float(i) / float(len(img[0]))
            v = float(j) / float(len(img))
            c = [0,0,0]
            for k in range(3):
                c[k] = round(c00[k] * (1-u) * (1-v) + 
                             c01[k] * (1-u) * v +
                             c10[k] * u * (1-v) +
                             c11[k] * u * v)
            img[j][i] = tuple(c)


