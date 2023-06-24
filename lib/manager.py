import pygame
import lib.style as style
import json
from os import listdir
from os.path import isfile, join

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

hasLoadedGallery = False

# DYNAMIC FPS. THIS FPS VALUE CHANGES WHEN LOOKING AT STATIC THINGS TO LOW FPS
fps = 60

charToAdd = ''
addText = False

onInputEvent = None

needToUpdate = False

threadings = []

guiRender = True

webcam = None

hasToTakeScreenshot = False

lastImage = None

class Notification:
    def __init__(self, app, title, text):
        self.app = app
        self.title = title
        self.text = text

notifications = []

scroll = 0
scrollX = 0

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
    global scroll
    global velocityY

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

    velocityY = 0
    velocityX = 0

    scroll = 0
lastMousePos = (0, 0)
lastLastMousePos = (0, 0)
lastClick = 0
velocityY = 0
velocityX = 0

def update():
    global appSize
    global appSizeGoal
    global screen
    global s
    global alertOpacity
    global openApps
    global lastMousePos
    global lastLastMousePos
    global lastClick
    global scroll
    global scrollX
    global velocityY
    global velocityX

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
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0] == 1 and isInApp and lastClick != click:
        # MOUSE DOWN
        lastClick = click
        lastMousePos = mouse
        
    elif lastClick != click:
        # MOUSE UP
        lastClick = click

    if click[0] == 1 and lastLastMousePos != mouse[1]:
        lastLastMousePos = mouse[1]
        velocityY = round(0 - (lastLastMousePos - lastMousePos[1]) / 20)
    else:
        lastMousePos = mouse
    if click[0] == 1 and lastLastMousePos != mouse[0]:
        lastLastMousePos = mouse[0]
        velocityX = round(0 - (lastLastMousePos - lastMousePos[0]) / 10)
    else:
        lastMousePos = mouse

    if click[0] != 1:
        if velocityY > 0:
            velocityY -= 0.5
        elif velocityY < 0:
            velocityY += 0.5

        if velocityX > 0:
            velocityX -= 0.5
        elif velocityX < 0:
            velocityX += 0.5

        if scroll < 0:
            velocityY = (0 - scroll) / 10

        if scrollX < 0:
            velocityX = (0 - scrollX) / 10

        if scrollX > 400:
            velocityX = (400 - scrollX) / 10

        velocityY = round(velocityY * 10) / 10

        velocityX = round(velocityX * 10) / 10

        scroll += round(velocityY)
        scrollX += round(velocityX)

    scroll += round((lastMousePos[1] - mouse[1]) / 30)
    scrollX += round((lastMousePos[0] - mouse[0]) / 30)

    if click[0] != 1:
        if scroll <= 0 and velocityY <= 0.5:
            scroll = lerp(scroll, 0, 0.1)
            velocityY = lerp(velocityY, 0, 0.1)

        if scrollX <= 0 and velocityX <= 0.5:
            scrollX = lerp(scrollX, 0, 0.1)
            velocityX = lerp(velocityX, 0, 0.1)

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def closeApp(name):
    global openApps
    global isInApp
    global appSizeGoal
    global isInInput
    global scrollX

    openApps.remove(name)
    isInApp = False
    appSizeGoal = 0.0

    style.RESET()

    isInInput = False

    if onClose != None:
        onClose()

    scrollX = 0

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
    
def file_list(path):
    onlyfiles = [f for f in listdir('./data/fs/' + path) if isfile(join('./data/fs/' + path, f))]

    return onlyfiles

def init(m):
    style.set_manager(m)
    checkStartupData()

pin = None

def checkStartupData():
    global pin

    startup_data = read_file('../startup.json')
    
    data = json.loads(startup_data)

    isSetup = data['setup']

    if data['pin'] != 'nopin':    
        pin = data['pin']

    if isSetup == False:
        openSetup()

def openSetup():
    global guiRender
    global appSize
    openApp('setup.py', (400 / 2, 800 / 2))
    guiRender = False
    appSize = 1

def updateStartupData():
    startup_data = read_file('../startup.json')

    data = json.loads(startup_data)

    data['setup'] = True

    content = json.dumps(data)

    write_file('../startup.json', content)

    os.execl(sys.executable, sys.executable, *sys.argv)

def updateScreen():
    global needToUpdate
    global appSize

    if needToUpdate == False:
        needToUpdate = True

def notify(app, title, text):
    global notifications
    notification = Notification(app, title, text)
    notifications.append(notification)