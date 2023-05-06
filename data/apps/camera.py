from lib.style import *
import sys
import pygame.camera
import pygame.image
from pygame.locals import *
import sys

def init(m):
    # Initialize the camera
    if m.webcam == None:

        alert('Loading', 'Please wait while the camera starts.')

        m.updateScreen()

        cameras = pygame.camera.list_cameras()

        manager.webcam = pygame.camera.Camera(cameras[0], (400, 800))
        manager.webcam.start()

        manager.webcamThumbnail = manager.webcam.get_image().convert()

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

            raw(image, size=(600, 400), pos=(400 / 2 - 600 / 2, 800 / 2 - 400 / 2))

            m.updateScreen()
        else:
            raw(m.webcamThumbnail, size=(600 * m.appSize, 400 * m.appSize), pos=(400 / 2 - 600 / 2, 800 / 2 - 400 / 2))

    rect(modify_color(BLACK, 1), (400 * m.appSize, 200 * m.appSize), pos=(0, 800 - 200))

    rect(background, (75 * m.appSize, 75 * m.appSize), pos=(400 / 2 - 75 / 2, 800 - 200 + 200 / 2 - 75 / 2), borderRadius=100)