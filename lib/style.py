import pygame
import os
import sys
import _thread

BLACK = (57, 62, 65)
WHITE = (246, 247, 235)
GREEN = (68, 187, 164)
RED = (233, 79, 55)
BLUE = (63, 136, 197)

foreground = BLACK
background = WHITE

TEXT_LIGHT = "./assets/fonts/ProximaNova/Proxima Nova Light.otf"
TEXT_REGULAR = "./assets/fonts/ProximaNova/Proxima Nova Reg.otf"
TEXT_SEMIBOLD = "./assets/fonts/ProximaNova/Proxima Nova Semibold.otf"
TEXT_BOLD = "./assets/fonts/ProximaNova/Proxima Nova Bold.otf"
TEXT_BLACK = "./assets/fonts/ProximaNova/Proxima Nova Black.otf"

# VARIABLES
primary = GREEN
secondary = BLACK
weight = TEXT_REGULAR

padding = [20, 20, 20, 20]
margin = [5, 5]

xIndex = padding[0]
yIndex = padding[1]

direction = "x"

manager = None

isScroll = False

buttonShadow = None
rectShadow = None
iconShadow = None

def modify_color(color, intensity):
    r = min(max(color[0] * intensity, 0), 255)
    g = min(max(color[1] * intensity, 0), 255)
    b = min(max(color[2] * intensity, 0), 255)
    return (r, g, b)

def set_manager(m):
    global manager
    manager = m

def scroll_box():
    global isScroll
    isScroll = True

def end_scroll_box():
    global isScroll
    isScroll = False

def RESET():
    global foreground
    global background
    global primary
    global secondary
    global weight
    global padding
    global margin
    global direction

    foreground = BLACK
    background = WHITE

    primary = GREEN
    secondary = BLACK
    weight = TEXT_REGULAR

    #padding = [20, 30, 20, 20]
    padding = [20, 20, 20, 20]
    margin = [5, 10]

    direction = "x"


def initApp(m):
    global manager
    global xIndex
    global yIndex
    global surface
    global buttonShadow
    global rectShadow
    global iconShadow

    if buttonShadow == None:
        buttonShadow = pygame.image.load('./assets/button.png').convert_alpha()
    
    if rectShadow == None:
        rectShadow = pygame.image.load('./assets/rect.png').convert_alpha()

    if iconShadow == None:
        iconShadow = pygame.image.load('./assets/app.png').convert_alpha()

    xIndex = padding[0]
    yIndex = padding[1]

    manager = m

    if manager.appSize != 1 and not ('000' in str(manager.appSize)):
        manager.updateScreen()

    surface = pygame.Surface((400, 800), pygame.SRCALPHA)

    try:
        pygame.draw.rect(
            surface,
            background,
            (
                m.appX,
                m.appY,
                (800 - 73) * manager.appSize + 73,
                (800 - 73) * manager.appSize + 73,
            ),
            int(800),
            int(50)
        )
    except:
        pygame.draw.rect(
            surface,
            background,
            (
                0,
                0,
                400,
                800,
            ),
        )

    surface.set_alpha(pow(manager.appSize, 0.5) * 256)

    manager.screen.blit(surface, (0, 0))

def set_direction(dir):
    global direction
    direction = dir


def set_primary(color):
    global primary
    primary = color


def set_weight(w):
    global weight
    weight = w

def set_text_size(size):
    global normalFont
    normalFont = pygame.font.Font(weight, size)

def set_background(color):
    global background
    background = color


def set_foreground(color):
    global foreground
    foreground = color


normalFont = None

lastScroll = 0
def label(text, center=False):
    global xIndex
    global yIndex
    global normalFont
    global lastScroll

    if normalFont == None:
        normalFont = pygame.font.Font(weight, 16)

    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)


    if lastScroll != manager.scroll:
        lastScroll = manager.scroll
        manager.updateScreen()

    if manager.isInApp == False or y > 800 * manager.appSize or x > 400 * manager.appSize:
        return

    text = normalFont.render(text, True, foreground)

    textRect = text.get_rect()
    if center == True:
        x = 400 / 2 - textRect.width / 2
        y = 800 / 2 - textRect.height / 2

    textRect.topleft = (x, y)

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + margin[0]
    if direction == "y":
        yIndex += textRect.height + margin[1]

def image(url, isAlpha=False, size=None, pos=None):
    global xIndex
    global yIndex

    if manager.isInApp == False:
        return

    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    if isAlpha == False:
        img = pygame.image.load('./assets/' + url).convert()
    else:
        img = pygame.image.load('./assets/' + url).convert_alpha()

    if size != None:
        img = pygame.transform.scale(img, size)

    rect = img.get_rect()
    if pos == None:
        rect.topleft = (x, y)
    else:
        rect.topleft = pos

    manager.screen.blit(img, rect)

    if direction == "x":
        xIndex += rect.width + margin[0]
    if direction == "y":
        yIndex += rect.height + margin[1]

def raw(img, size=None, pos=None):
    global xIndex
    global yIndex

    if manager.isInApp == False:
        return

    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)
    
    if size != None:
        img = pygame.transform.scale(img, (size[0], size[1]))

    rect = img.get_rect()
    if pos == None:
        rect.topleft = (x, y)
    else:
        rect.topleft = (pos[0] + manager.appPos[0] * (1 - manager.appSize), pos[1] + manager.appPos[1] * (1 - manager.appSize))

    manager.screen.blit(img, rect)

    if direction == "x":
        xIndex += rect.width + margin[0]
    if direction == "y":
        yIndex += rect.height + margin[1]

def rect(color, size, pos=None, borderRadius=0):
    global xIndex
    global yIndex

    if manager.isInApp == False:
        return

    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    if pos == None:
        rect = (int(x), int(y), size[0], size[1])
    else:
        rect = (pos[0] + manager.appPos[0] * (1 - manager.appSize), pos[1] + manager.appPos[1] * (1 - manager.appSize), size[0], size[1])

    if borderRadius == 0:
        pygame.draw.rect(manager.screen, color, rect)
    else:
        pygame.draw.rect(manager.screen, color, rect, border_radius=borderRadius, width=int(size[1] / 2))

    if direction == "x":
        xIndex += rect[2] + margin[0]
    if direction == "y":
        yIndex += rect[3] + margin[1]

inputbuttondown = False
gonnaClick = True

def input(text, width, value):
    global xIndex
    global yIndex
    global foreground
    global weight
    global inputbuttondown
    global gonnaClick
    global normalFont

    if manager.isInApp == False:
        return
    
    if normalFont == None:
        normalFont = pygame.font.Font(weight, 16)
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    m = manager

    if manager.addText == True:
        exec(text + ' += "' + manager.charToAdd.replace('"', "'") + '"')
        manager.addText = False

    text = normalFont.render(eval(text), True, foreground)

    textRect = text.get_rect()
    textRect.width = width
    textRect.left = x + 10
    textRect.top = y + 10

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hover = False

    if (
        x + textRect.width + 20 > mouse[0] > x
        and y + textRect.height + 20 > mouse[1] > y
    ):
        hover = True

        if click[0] == 1:
            if inputbuttondown == False and gonnaClick == True:
                inputbuttondown = True
                manager.isInInput = not manager.isInInput
                gonnaClick = False
        else:
            if inputbuttondown:
                gonnaClick = True
                inputbuttondown = False
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    rect = buttonShadow.get_rect()

    rect.topleft = (x - ((textRect.width + 20) / 25), y)
    rect.width = (textRect.width + 20) * 1.05
    rect.height = (textRect.height + 20) * 1.05

    shadowScaled = pygame.transform.scale(buttonShadow, (rect.width, rect.height))

    manager.screen.blit(shadowScaled, rect)

    pygame.draw.rect(manager.screen, background, (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), 10)
    

    # borderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)
    
    # pygame.draw.rect(borderSurface, (0, 0, 0), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)
    
    if hover == False:
        pygame.draw.rect(manager.screen, modify_color(background, 0.9), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)
    else:
        pygame.draw.rect(manager.screen, modify_color(background, 0.8), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)

    if manager.isInInput:
        pygame.draw.rect(manager.screen, modify_color(background, 0.8), (x, y, textRect.width + 20, textRect.height + 20), 2, 10)

    # manager.screen.blit(borderSurface, (0, 0))

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + 20 + margin[0]
    if direction == "y":
        yIndex += textRect.height + 20 + margin[1]

def textArea(text, width, height):
    global xIndex
    global yIndex
    global foreground
    global weight
    global inputbuttondown
    global gonnaClick
    global normalFont

    if manager.isInApp == False:
        return
    
    if normalFont == None:
        normalFont = pygame.font.Font(weight, 16)
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)
    
    m = manager

    if manager.addText == True:
        manager.addText = False
        exec(text + ' += "' + manager.charToAdd.replace('"', "'") + '"')

    text = normalFont.render(eval(text), True, foreground)

    textRect = text.get_rect()
    textRect.width = width
    textRect.height = height
    textRect.left = x + 10
    textRect.top = y + 10

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hover = False

    if (
        xIndex + textRect.width + 20 > mouse[0] > xIndex
        and yIndex + textRect.height + 20 > mouse[1] > yIndex
    ):
        hover = True

        if click[0] == 1:
            if inputbuttondown == False and gonnaClick == True:
                inputbuttondown = True
                manager.isInInput = not manager.isInInput
                gonnaClick = False
        else:
            if inputbuttondown:
                gonnaClick = True
                inputbuttondown = False

    if manager.isInInput:
        pygame.draw.rect(manager.screen, (0, 0, 0), (textRect.left + textRect.width + 2, textRect.top, 2, textRect.height), 2, 0)

    manager.updateScreen()
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    if isScroll:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
    else:
        y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + 20 + margin[0]
    if direction == "y":
        yIndex += textRect.height + 20 + margin[1]

def button(text, action, color=None, width=None, height=None, posX=None, posY=None, borderRadius=10):
    global xIndex
    global yIndex
    global foreground
    global weight
    global normalFont
    global buttonShadow

    if manager.isInApp == False:
        return

    if normalFont == None:
        normalFont = pygame.font.Font(weight, 16)
    
    x = 0
    y = 0

    if posX == None:
        x = xIndex + manager.appPos[0] * (1 - manager.appSize)
        if isScroll:
            y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
        else:
            y = yIndex + manager.appPos[1] * (1 - manager.appSize)
    else:
        x = posX * (1 - manager.appSize)
        if isScroll:
            y = posY * (1 - manager.appSize) - manager.scroll
        else:
            y = posY * (1 - manager.appSize)

    oldweight = weight
    weight = TEXT_SEMIBOLD

    weight = oldweight

    oldforeground = foreground

    if color == None:
        if primary == BLACK or primary == GREEN or primary == RED or primary == BLUE:
            foreground = WHITE
    else:
        if color == BLACK or color == GREEN or color == RED or color == BLUE:
            foreground = WHITE
    
    text = normalFont.render(text, True, foreground)

    foreground = oldforeground

    textRect = text.get_rect()
    textRect.left = x + 10
    textRect.top = y + 10

    if width != None:
        textRect.width = width - 20

    if height != None:
        textRect.height = height - 20

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hover = False
    
    clicked = False

    if (
        x + textRect.width + 20 > mouse[0] > x
        and y + textRect.height + 20 > mouse[1] > y
    ):
        posX = x - 2
        posY = y - 2
        textRect.width += 4
        textRect.height += 4
        hover = True
    else:
        pass

    manager.updateScreen()
    
    if posX == None:
        x = xIndex + manager.appPos[0] * (1 - manager.appSize)
        if isScroll:
            y = yIndex + manager.appPos[1] * (1 - manager.appSize) - manager.scroll
        else:
            y = yIndex + manager.appPos[1] * (1 - manager.appSize)
    else:
        x = posX * (manager.appSize)
        if isScroll:
            y = posY * (manager.appSize) - manager.scroll
        else:
            y = posY * (manager.appSize)

    if borderRadius < 100:
        rect = buttonShadow.get_rect()

        rect.topleft = (x - ((textRect.width + 20) / 25), y)
        rect.width = (textRect.width + 20) * 1.05
        rect.height = (textRect.height + 20) * 1.05

        shadowScaled = pygame.transform.scale(buttonShadow, (rect.width, rect.height))

        manager.screen.blit(shadowScaled, rect)
    else:
        rect = iconShadow.get_rect()

        rect.topleft = (x - ((textRect.width + 20) / 25), y)
        rect.width = (textRect.width + 20) * 1.05
        rect.height = (textRect.height + 20) * 1.05

        shadowScaled = pygame.transform.scale(iconShadow, (rect.width, rect.height))

        manager.screen.blit(shadowScaled, rect)

    if color == None:
        pygame.draw.rect(manager.screen, primary, (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), borderRadius)
        pygame.draw.rect(manager.screen, modify_color(primary, 0.9), (x, y, textRect.width + 20, textRect.height + 20), 1, borderRadius)
    else:
        pygame.draw.rect(manager.screen, color, (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), borderRadius)
        pygame.draw.rect(manager.screen, modify_color(color, 0.9), (x, y, textRect.width + 20, textRect.height + 20), 1, borderRadius)

    # borderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)
    
    # pygame.draw.rect(borderSurface, (0, 0, 0), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)
    # pygame.draw.rect(borderSurface, (255, 255, 255), (x - 1, y - 1, textRect.width + 20 + 2, textRect.height + 20 + 2), 1, 10)

    # borderSurface.set_alpha(52)

    # manager.screen.blit(borderSurface, (0, 0))

    if hover:
        x += 2
        y += 2

        if click[0] == 1:
            if action != None:
                action(manager)

            manager.isInInput = False

            clicked = True

    if clicked:
        if color == None:
            pygame.draw.rect(manager.screen, modify_color(primary, 0.8), (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), 10)
        else:
            pygame.draw.rect(manager.screen, modify_color(color, 0.8), (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), 10)

    if hover:
        textRect.width -= 4
        textRect.height -= 4

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + 20 + margin[0]
    if direction == "y":
        yIndex += textRect.height + 20 + margin[1]

def titleBar(text, color=primary):
    global xIndex
    global yIndex
    global foreground
    global weight
    global normalFont
    global rectShadow

    if manager.isInApp == False:
        return

    xIndex = 15
    yIndex = 45

    x = manager.appX
    if isScroll:
        y = manager.appY - manager.scroll
    else:
        y = manager.appY - 5
    width = 1000 * manager.appSize + 1
    height = 75 * manager.appSize + 5

    rect = rectShadow.get_rect()

    rect.topleft = (x - (width / 10), y - 10)
    rect.width = (width) * 1.155
    rect.height = (height) * 1.19

    shadowScaled = pygame.transform.scale(rectShadow, (rect.width, rect.height))

    if not (manager.appSize < 1):
        manager.screen.blit(shadowScaled, rect)

    #pygame.draw.rect(manager.screen, color, (x, y, width, height), border_radius=int(50 * (1 - manager.appSize)))
    pygame.draw.rect(manager.screen, color, (x, y, width, height), border_top_left_radius=50, border_top_right_radius=50)
    pygame.draw.rect(manager.screen, modify_color(color, 0.8), (x, y + height - 1, width, 1))

    if color == BLACK or color == GREEN or color == RED or color == BLUE:
        foreground = WHITE

    lastWeight = weight

    weight = TEXT_SEMIBOLD

    label(text)

    if color == BLACK or color == GREEN or color == RED or color == BLUE:
        foreground = BLACK

    weight = lastWeight

    # outline and border
    # outlineBorderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    # pygame.draw.rect(outlineBorderSurface, (0, 0, 0), (x, y + height - 1, width, 1))
    # pygame.draw.rect(outlineBorderSurface, (255, 255, 255), (x, y + height, width, 1))

    # outlineBorderSurface.set_alpha(51.2)

    # manager.screen.blit(outlineBorderSurface, (0, 0))

    xIndex = padding[0]
    yIndex = 75 + padding[1]


def alert(text, title):
    if manager.currentAlert != ";":
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and manager.canCloseAlert:
            manager.closeAlert()

    allSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    backgroundAlert = pygame.Surface((400, 800), pygame.SRCALPHA)

    backgroundAlert.fill((0, 0, 0))

    backgroundAlert.set_alpha(128)

    allSurface.blit(backgroundAlert, (0, 0))

    width = 200
    height = 100

    x = (400 / 2) - (width / 2)
    y = (800 / 2) - (height / 2)

    pygame.draw.rect(allSurface, WHITE, (x, y, width, height), width, 10)

    normalFont = pygame.font.Font(TEXT_REGULAR, 16)
    boldFont = pygame.font.Font(TEXT_BOLD, 24)

    title = boldFont.render(title, True, foreground)

    titleRect = title.get_rect()
    titleRect.topleft = (x + 20, y + 20)

    allSurface.blit(title, titleRect)

    t = normalFont.render(text, True, foreground)

    tRect = t.get_rect()
    tRect.topleft = (x + 20, y + 20 + 24 + 10)

    allSurface.blit(t, tRect)

    allSurface.set_alpha(manager.alertOpacity * 256)

    manager.screen.blit(allSurface, (0, 0))

    if manager.alertOpacity != manager.alertOpacityGoal:
        manager.updateScreen()

def web(url, x, y, width, height):
    _thread.start_new_thread( create_web_window, (url, x, y, width, height) )

def create_web_window(url, x, y, width, height):
    os.system('py lib/rwebsdk/rwebsdk.py ' + str(url) + ' ' + str(x) + ' ' + str(y) + ' ' + str(width) + ' ' +  str(height))