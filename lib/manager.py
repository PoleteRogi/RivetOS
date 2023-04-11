import pygame
import lib.style as style

openApps = []
appsMemory = []

onOpen = None

screen = None

appSize = 0.0
appSizeGoal = 0.0

isInApp = False

def openApp(name):
    global openApps
    global onOpen
    global appSize
    global appSizeGoal
    global isInApp

    openApps.clear()
    appsMemory.clear()

    file = './data/apps/' + name

    appSizeGoal = 1

    openApps.append(name.split('.')[0])

    isInApp = True

    if onOpen != None:
        onOpen(file, name)
    
    style.RESET()

def update():
    global appSize
    global appSizeGoal
    global screen
    global s
    if appSize < appSizeGoal:
        appSize += (appSizeGoal - appSize) / 2
    
    if appSize > appSizeGoal:
        appSize -= (appSize - appSizeGoal) / 2

def closeApp(name):
    global openApps
    global isInApp
    global appSizeGoal

    openApps.remove(name)
    isInApp = False
    appSizeGoal = 0.0

    style.RESET()

def closeAllApps():
    global openApps
    global isInApp
    global appSizeGoal

    # openApps.clear()
    isInApp = False
    appSizeGoal = 0.0

    style.RESET()