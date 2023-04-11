import pygame
import lib.style as style
from datetime import datetime

homeButtonImage = None
originalHomeButtonImage = None


def init(m):
    global homeButtonImage
    global originalHomeButtonImage
    originalHomeButtonImage = pygame.image.load(
        "./assets/HomeButton.png"
    ).convert_alpha()
    homeButtonImage = pygame.transform.scale(
        originalHomeButtonImage, (80, 40)
    ).convert_alpha()


def render(m):
    global homeButtonImage
    actionBarSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    pygame.draw.rect(
        actionBarSurface, (0, 0, 0), (0, 800 - 50 + 50 * (1 - m.appSize), 400, 50), 400
    )

    actionBarSurface.set_alpha(32)

    m.screen.blit(actionBarSurface, (0, 0))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x = 200 - 40
    y = 750 + 25 - 20 + 40 * (1 - m.appSize)

    if m.isInApp == False and round(m.appSize) == 0:
        y = 800

    if x + 80 > mouse[0] > x and y + 40 > mouse[1] > y:

        homeButtonImage = pygame.transform.scale(
            originalHomeButtonImage, (85, 42.5)
        ).convert_alpha()

        x = 200 - 42.5
        y = 750 + 25 - 21 + 40 * (1 - m.appSize)

        if click[0] == 1:
            # CLOSE APP
            m.closeAllApps()

    else:
        homeButtonImage = pygame.transform.scale(
            originalHomeButtonImage, (80, 40)
        ).convert_alpha()

    m.screen.blit(homeButtonImage, (x, y))