from lib.style import *
import sys

def init(m):
    pass

def quitAction(m):
    m.SHUT()

def settings(m):
    # APP STYLE SETTINGS
    set_background((232, 233, 218))

    set_primary(RED)

    initApp(m)

    title = titleBar('Settings', color=BLACK)

    quitButton = button('Quit', quitAction)