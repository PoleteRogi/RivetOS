import pygame
import lib.style as style

openApps = []
appsMemory = []

onOpen = None
onClose = None

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

threadings = []

import os
import sys

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

appPos = (0, 0)

def openApp(name, pos):
    global openApps
    global onOpen
    global appSize
    global appSizeGoal
    global isInApp
    global appPos

    appPos = pos

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
    global openApps

    if appSize < appSizeGoal:
        appSize += (appSizeGoal - appSize) / 5

    if appSize > appSizeGoal:
        appSize -= (appSize - appSizeGoal) / 5

    if appSize >= 0.9999:
        appSize = 1
    
    if appSize <= 0.0001 and appSize != 0:
        appSize = 0
        openApps.clear()
        style.RESET()
        updateScreen()

    if alertOpacity < alertOpacityGoal:
        alertOpacity += (alertOpacityGoal - alertOpacity) / 2

    if alertOpacity > alertOpacityGoal:
        alertOpacity -= (alertOpacity - alertOpacityGoal) / 2
    
    if alertOpacity >= 0.999:
        alertOpacity = 1    

    if alertOpacity <= 0.001:
        alertOpacity = 0

    if isShutingDown:     
        screen.fill(style.background)

        logo = pygame.image.load("./assets/icons/system/RivetLight.png").convert_alpha()

        width = 50
        height = 65

        logo = pygame.transform.scale(logo, (width, height))

        screen.blit(logo, (400 / 2 - width / 2, 800 / 2 - height / 2))

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

    if onClose != None:
        onClose()

def closeAllApps():
    global openApps
    global isInApp
    global appSizeGoal
    global isInInput
    global addText
    global charToAdd

    appSizeGoal = 0.0

    isInApp = False

    style.RESET()
    updateScreen()

    isInInput = False

    addText = False
    charToAdd = ''

    if onClose != None:
        onClose()

canCloseAlert = False

isShutingDown = False

def SHUT():
    global isShutingDown

    isShutingDown = True

    closeAllApps()
    setTimeout(terminate, 5000)

def terminate():
    global running
    running = False
    terminateThreadings()

    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('sudo shutdown now')

def terminateThreadings():
    for thread in threadings:
        thread.cancel()

from threading import Timer  
 
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs) 
    t.start()
    threadings.append(t) 
    return t

def closeAlertCanFunc():
    global canCloseAlert
    canCloseAlert = True

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

    setTimeout(closeAlertCanFunc, 500)

def closeAlert():
    global currentAlert
    global isInApp
    global alertOpacityGoal
    global canCloseAlert
    currentAlert = ";"

    alertOpacityGoal = 0

    isInApp = lastIsInApp

    canCloseAlert = False

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
    global appSize

    if needToUpdate == False:
        needToUpdate = True