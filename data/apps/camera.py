import datetime
import time
from lib.style import *
import sys
import pygame.camera
import pygame.image
from pygame.locals import *
import sys
import _thread
import glob

def init(m):
    # Initialize the camera
    if m.webcam == None:

        alert('Loading', 'Please wait while the camera starts.')

        m.updateScreen()

        cameras = pygame.camera.list_cameras()

        manager.webcam = pygame.camera.Camera(cameras[0], (1920, 1080))

        manager.webcam.start()

        manager.webcamThumbnail = manager.webcam.get_image().convert()

        list_of_files = glob.glob('./data/fs/camera/*')
        
        if len(list_of_files) > 0:
            latest_file = max(list_of_files, key=os.path.getctime)

            m.lastImage = latest_file

lastClicked = False

def clickdown(m):
    global lastClicked

    button('', action=None, color=BLACK, width=74, height=74, posX=400 / 2 - 74 / 2, posY=800 - 200 + 200 / 2 - 74 / 2, borderRadius=100, clickup=None)

    if lastClicked == False:
        lastClicked = True
        pic(m)

def pic(m):
    now = datetime.datetime.now()

    #imgName = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.jpg'
    #pygame.image.save(m.webcam.get_image().convert(), './data/fs/camera/' + imgName)

    imgName1 = 'cam1' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png'
    pygame.image.save(m.webcam.get_image().convert(), './data/tmp/' + imgName1)

    imgName2 = 'cam2' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png'
    pygame.image.save(m.webcam.get_image().convert(), './data/tmp/' + imgName2)

    imgName3 = 'cam3' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png'
    pygame.image.save(m.webcam.get_image().convert(), './data/tmp/' + imgName3)

    imgName4 = 'cam4' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png'
    pygame.image.save(m.webcam.get_image().convert(), './data/tmp/' + imgName4)

    os.system('py lib/ripp/ripp.py ' + imgName1 + ' ' + imgName2 + ' ' + imgName3 + ' ' + imgName4)

    list_of_files = glob.glob('./data/fs/camera/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    m.lastImage = latest_file

def clickup(m):
    global lastClicked
    lastClicked = False

def camera(m):
    # APP STYLE SETTINGS
    set_background(BLACK)
    set_foreground(WHITE)

    set_primary(RED)

    initApp(m)

    # Render Camera Image
    if m.webcam != None and m.screen != None:
        if m.appSize > 0.999:
            image = m.webcam.get_image().convert()

            raw(image, size=(600, 350), pos=(400 / 2 - 600 / 2, 800 / 2 - 350 / 2))

            if m.lastImage != None:
                raw(pygame.image.load(m.lastImage).convert(), (74, 74), (40, 800 - 200 + 200 / 2 - 74 / 2))

            m.updateScreen()
        else:
            raw(m.webcamThumbnail, size=(600 * m.appSize, 350 * m.appSize), pos=(400 / 2 - 600 / 2, 800 / 2 - 350 / 2))

    button('', action=clickdown, color=WHITE, width=74, height=74, posX=400 / 2 - 74 / 2, posY=800 - 200 + 200 / 2 - 74 / 2, borderRadius=100, clickup=clickup)
    
    

    # pygame.draw.rect(m.screen, WHITE, rect=(400 / 2 - 75 / 2, 800 - 200 + 200 / 2 - 75 / 2, 75, 75))


    #, borderRadius=100