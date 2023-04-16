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


lastActionBarHover = False

def render(m):
    global homeButtonImage
    global lastActionBarHover

    pygame.draw.rect(
        m.screen, (style.modify_color(style.background, 0.95)), (0, 800 - 50 + 50 * (1 - m.appSize), 400, 50), 400
    )

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x = 200 - 40
    y = 750 + 25 - 20 + 40 * (1 - m.appSize)

    hover = False

    if m.isInApp == False and round(m.appSize) == 0:
        y = 800

    if x + 80 > mouse[0] > x and y + 40 > mouse[1] > y:
        hover = True
        homeButtonImage = pygame.transform.scale(
            originalHomeButtonImage, (100, 40)
        ).convert_alpha()

        x = 200 - 50
        y = 750 + 25 - 20 + 40 * (1 - m.appSize)

        if click[0] == 1:
            # CLOSE APP
            m.closeAllApps()

    else:
        homeButtonImage = pygame.transform.scale(
            originalHomeButtonImage, (80, 40)
        ).convert_alpha()

    if hover != lastActionBarHover:
        m.updateScreen()
        
    lastActionBarHover = hover

    m.screen.blit(homeButtonImage, (x, y))