# Example file showing a basic pygame "game loop"
import pygame
import lib.home as home
import lib.actionbar as actionbar
import lib.keyboard as keyboard
import lib.manager as manager
from datetime import datetime
import lib.style as style
import requests
import sys
import os

# pygame setup
pygame.init()

# RivetPhone has a resolution of 240x320. This is a placeholder
screen = pygame.display.set_mode((400, 800))
clock = pygame.time.Clock()

running = True

pygame.display.set_caption('Rivet')

man = manager

def openAppOnMemory(file, name):
    try:
        f = open(file)
        content = f.read()
        f.close()
        man.appsMemory.append(content)

        exec('from data.apps.' + name.split('.')[0] + ' import *')

        eval('init')(man)
    except Exception as e:
        # CLOSE THE APP IN CASE OF AN ERROR
        man.closeApp(name.split('.')[0])

        if type(e) == FileNotFoundError:
            man.alert('Error', 'App file does not exist', m=man)
        else:
            man.alert('Error', 'Unknown error ocurred')
            print(e)

man.onOpen = openAppOnMemory
man.screen = screen

actionbar.init(man)

manager.init(man)

while running:
    events = pygame.event.get()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if man.isInApp == False:
        style.RESET()

    # RENDER
    home.render(screen, events, man)

    index = 0
    for app in man.openApps:
        
        exec('from data.apps.' + app + ' import *')

        eval(app)(man)

        index += 1

    keyboard.render(man)
    actionbar.render(man)

    if man.isInApp == False:
        style.RESET()

    man.renderAlert()

    normalFont = pygame.font.Font(style.TEXT_REGULAR, 16)

    now = datetime.now()

    if home.isLockscreen == False:
        time = now.strftime("%H:%M")

        timeText = normalFont.render(time, True, style.foreground)

        timeTextRect = timeText.get_rect()
        timeTextRect.center = (400 // 2, (30 // 2))

        screen.blit(timeText, timeTextRect)


    # flip() the display to put your work on screen
    pygame.display.flip()

    man.update()

    # clock.tick(man.fps)  # limits FPS to 60