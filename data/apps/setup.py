from lib.style import *

def init(m):
    pass

def setup(m):
    global xIndex
    global yIndex
    set_direction('y')

    initApp(m)
    
    imageWidth = 50
    imageHeight = 65
    imageX = 400 / 2 - imageWidth / 2
    imageY = 800 / 2 - imageHeight / 2

    image('icons/system/RivetLight.png', isAlpha=True, size=(imageWidth, imageHeight), pos=(imageX, imageY))