# Example file showing a basic pygame "game loop"
import pygame
import lib.home as home
import lib.actionbar as actionbar
import lib.keyboard as keyboard
import lib.manager as manager
import lib.statusbar as statusbar
import lib.style as style
import requests
import sys
import os

# pygame setup
pygame.display.init()
pygame.font.init()

# RivetPhone has a resolution of 240x320. This is a placeholder
screen = pygame.display.set_mode((400, 800), pygame.NOFRAME, vsync=100000)
clock = pygame.time.Clock()

running = True

pygame.display.set_caption('Rivet')

man = manager

statusbar.init(man)

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
        
        closeApp()

def closeApp():
    home.wallpaperScaleGoal = 1.2

man.onOpen = openAppOnMemory
man.onClose = closeApp
man.screen = screen

actionbar.init(man)

manager.init(man)

while man.running:

    man.needToUpdate = False

    events = pygame.event.get()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in events:
        if event.type == pygame.QUIT:
            man.running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER
    home.render(screen, events, man)

    index = 0
    for app in man.openApps:
        
        exec('from data.apps.' + app + ' import *')

        eval(app)(man)

        index += 1

    keyboard.render(man)
    actionbar.render(man)

    man.renderAlert()

    statusbar.render(home, screen)

    man.update()

    if man.needToUpdate:
        # flip() the display to put your work on screen
        pygame.display.flip()
        
    clock.tick(60)