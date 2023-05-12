from lib.style import *
import sys
import os

def init(m):
    m.currentSettingsTab = 0
    pass

def quitAction(m):
    m.SHUT()

def restartAction(m):
    os.execl(sys.executable, sys.executable, *sys.argv)

def openTab1(m):
    m.currentSettingsTab = 0

def openTab2(m):
    m.currentSettingsTab = 0

def goHome(m):
    m.currentSettingsTab = 0

def settings(m):
    # APP STYLE SETTINGS
    set_background((232, 233, 218))

    initApp(m)

    set_direction('y')

    scroll_box()  

    if m.currentSettingsTab == 0:
        title = titleBar('Settings', color=BLACK)

        button('Tab1', openTab1, color=WHITE, width=400 - 60)
        button('Tab2', openTab2, color=WHITE, width=400 - 60)
    
    if m.currentSettingsTab == 10:
        title = titleBar('Tab 1', color=BLACK)

    if m.currentSettingsTab == 20:
        title = titleBar('Tab 2', color=BLACK)

    end_scroll_box()