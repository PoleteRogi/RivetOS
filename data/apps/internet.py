from lib.style import *
import pygame.image
import sys

def init(m):
    # m.notify('Debug', 'Test', 'This is a notification')
    pass

def internet(m):
    initApp(m)

    set_direction('y')
        
    scroll_box()  

    for i in range(50):
        label('Item ' + str(i))

    end_scroll_box()