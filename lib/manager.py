import pygame
import lib.style as style

openApps = []
appsMemory = []

onOpen = None

screen = None

appSize = 0.0
appSizeGoal = 0.0

isInApp = False
lastIsInApp = False

currentAlert = ""

running = True

isInInput = False

# DYNAMIC FPS. THIS FPS VALUE CHANGES WHEN LOOKING AT STATIC THINGS TO LOW FPS
fps = 60

def openApp(name):
    global openApps
    global onOpen
    global appSize
    global appSizeGoal
    global isInApp

    openApps.clear()
    appsMemory.clear()

    file = "./data/apps/" + name

    appSizeGoal = 1

    openApps.append(name.split(".")[0])

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
        appSize += (appSizeGoal - appSize) / 3

    if appSize > appSizeGoal:
        appSize -= (appSize - appSizeGoal) / 3

    if appSize >= 0.999:
        appSize = 1

def closeApp(name):
    global openApps
    global isInApp
    global appSizeGoal
    global isInInput

    openApps.remove(name)
    isInApp = False
    appSizeGoal = 0.0

    style.RESET()

    isInInput = False


def closeAllApps():
    global openApps
    global isInApp
    global appSizeGoal
    global isInInput

    # openApps.clear()

    appSizeGoal = 0.0

    isInApp = False

    style.RESET()

    isInInput = False

def alert(title, text, m=None):
    global currentAlert
    global lastIsInApp
    global isInApp

    currentAlert = text + ";" + title
    if m is not None:
        style.set_manager(m)

    lastIsInApp = isInApp
    isInApp = True


def closeAlert():
    global currentAlert
    global isInApp
    currentAlert = ""

    isInApp = lastIsInApp

def renderAlert():
    if currentAlert != "":
        style.alert(currentAlert.split(";")[0], currentAlert.split(";")[1])

def openInput():
    global isInInput
    isInInput = True

def closeInput():
    global isInInput
    isInInput = False