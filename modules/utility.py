import pyglet

def drawlabel(text,ver):
    '''Draw a simple label, useful debugging tool.
    text is the text drawn, ver is the vertical position
    starting from bottom left angle'''
    l = pyglet.text.Label(text=text, x=10, y=ver).draw()

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2