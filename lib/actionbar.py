import math
import lib.home as home
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

def actionbuttons(m):
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

x = 200 - 40
y = 800 - 8 - 8

lasthover = False
lastclick = False

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def actionbar(m):
    global lastActionBarHover
    global x
    global y
    global lasthover
    global lastclick

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hover = False

    if x + 80 > mouse[0] > x and y + 40 > mouse[1] > y:
        hover = True
        lasthover = True

    if click[0] == 1 and lasthover == True:
        lastclick = True

        appSize = 1 - (0 - ((mouse[1] - 4 - (800 - 8 - 8)) / 130))

        y = max(appSize * 130 + 670 + 4 - 8 - 8 - 4, 800 - 75)

        m.appSizeGoal = appSize
        home.wallpaperScaleGoal = min(max(lerp(1.2, 2, appSize), 1.2), 2)
        m.updateScreen()
    
    if click[0] == 0:
        if lasthover == True or lastclick == True:
            lasthover = False
            lastclick = False

            if m.appSizeGoal < 0.8:
                m.closeAllApps()
            else:
                m.appSizeGoal = 1

            y = 800 - 8 - 8

            m.updateScreen()

    pygame.draw.rect(m.screen, style.foreground, (x, y, 80, 8), 4, 50)

    if hover != lastActionBarHover:
        m.updateScreen()
        
    lastActionBarHover = hover

def render(m):
    if m.guiRender == True:
        #actionbuttons(m)
        actionbar(m)