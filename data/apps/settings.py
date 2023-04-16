from lib.style import *
import sys
import os

def init(m):
    pass

def quitAction(m):
    m.SHUT()

def restartAction(m):
    os.execl(sys.executable, sys.executable, *sys.argv)

def settings(m):
    # APP STYLE SETTINGS
    set_background((232, 233, 218))

    set_primary(RED)

    initApp(m)

    title = titleBar('Settings', color=BLACK)

    quitButton = button('Quit', quitAction)

    restartButton = button('Restart', restartAction)