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

currentAlert = ";"

running = True

isInInput = False

alertOpacity = 0
alertOpacityGoal = 0

# DYNAMIC FPS. THIS FPS VALUE CHANGES WHEN LOOKING AT STATIC THINGS TO LOW FPS
fps = 60

charToAdd = ''
addText = False

onInputEvent = None

needToUpdate = False

def keyboardInput(char):
    global charToAdd
    global addText

    charToAdd = char
    addText = True

    if onInputEvent != None:
        onInputEvent()

def addOnInput(event):
    global onInputEvent
    onInputEvent = event    

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
    global alertOpacity
    if appSize < appSizeGoal:
        appSize += (appSizeGoal - appSize) / 3

    if appSize > appSizeGoal:
        appSize -= (appSize - appSizeGoal) / 3

    if appSize >= 0.999:
        appSize = 1

    if alertOpacity < alertOpacityGoal:
        alertOpacity += (alertOpacityGoal - alertOpacity) / 2

    if alertOpacity > alertOpacityGoal:
        alertOpacity -= (alertOpacity - alertOpacityGoal) / 2
    
    if alertOpacity >= 0.999:
        alertOpacity = 1    

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
    global addText
    global charToAdd

    # openApps.clear()

    appSizeGoal = 0.0

    isInApp = False

    style.RESET()

    isInInput = False

    addText = False
    charToAdd = ''

def alert(title, text, m=None):
    global currentAlert
    global alertOpacityGoal
    global lastIsInApp
    global isInApp

    alertOpacityGoal = 1

    currentAlert = text + ";" + title
    if m is not None:
        style.set_manager(m)

    lastIsInApp = isInApp
    isInApp = True


def closeAlert():
    global currentAlert
    global isInApp
    global alertOpacityGoal
    currentAlert = ";"

    alertOpacityGoal = 0

    isInApp = lastIsInApp

def renderAlert():
    style.alert(currentAlert.split(";")[0], currentAlert.split(";")[1])

def openInput():
    global isInInput
    isInInput = True

def closeInput():
    global isInInput
    isInInput = False

def read_file(file):
    f = open('./data/fs/' + file, 'r')
    content = f.read()
    f.close()
    return content

def write_file(file, content):
    try:
        f = open('./data/fs/' + file, 'w')
        f.write(content)
        f.close()
        return True
    except:
        return False

def init(m):
    style.set_manager(m)

def updateScreen():
    global needToUpdate

    if needToUpdate == False:
        needToUpdate = True