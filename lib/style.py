import pygame

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

def modify_color(color, intensity):
    r = min(max(color[0] * intensity, 0), 255)
    g = min(max(color[1] * intensity, 0), 255)
    b = min(max(color[2] * intensity, 0), 255)
    return (r, g, b)

def set_manager(m):
    global manager
    manager = m


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

    padding = [20, 20, 20, 20]
    margin = [5, 10]

    direction = "x"


def initApp(m):
    global manager
    global xIndex
    global yIndex
    global surface

    xIndex = padding[0]
    yIndex = padding[1]

    manager = m

    if manager.appSize != 1 and not ('000' in str(manager.appSize)):
        manager.updateScreen()

    surface = pygame.Surface((400, 800), pygame.SRCALPHA)

    pygame.draw.rect(
        surface,
        background,
        (
            (manager.appPos[0] - 73 / 2 - 15) * (1 - manager.appSize),
            (manager.appPos[1] - 73 / 2 - 15) * (1 - manager.appSize),
            800 * manager.appSize + 73,
            800 * manager.appSize + 73,
        ),
        int(800),
        int(50 * (1 - manager.appSize))
    )

    surface.set_alpha(manager.appSize * 256)

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


def set_background(color):
    global background
    background = color


def set_foreground(color):
    global foreground
    foreground = color


def label(text):
    global xIndex
    global yIndex

    if manager.isInApp == False:
        return

    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    normalFont = pygame.font.Font(weight, 16)

    text = normalFont.render(text, True, foreground)

    textRect = text.get_rect()
    textRect.topleft = (x, y)

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + margin[0]
    if direction == "y":
        yIndex += textRect.height + margin[1]

inputbuttondown = False
gonnaClick = True

def input(text, width, value):
    global xIndex
    global yIndex
    global foreground
    global weight
    global inputbuttondown
    global gonnaClick

    if manager.isInApp == False:
        return
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    normalFont = pygame.font.Font(weight, 16)
  
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
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    pygame.draw.rect(manager.screen, background, (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), 10)

    # borderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)
    
    # pygame.draw.rect(borderSurface, (0, 0, 0), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)
    
    # if hover == False:
        # borderSurface.set_alpha(52)
    # else:
        # borderSurface.set_alpha(104)

    # if manager.isInInput:
        # pygame.draw.rect(borderSurface, (0, 0, 0), (x - 1, y - 1, textRect.width + 20 + 2, textRect.height + 20 + 2), 1, 11)
        # borderSurface.set_alpha(104)
        # pygame.draw.rect(borderSurface, (0, 0, 0), (textRect.left + textRect.width + 2, textRect.top, 2, textRect.height), 2, 0)
    # else:
        # pygame.draw.rect(borderSurface, (255, 255, 255), (x - 1, y - 1, textRect.width + 20 + 2, textRect.height + 20 + 2), 1, 10)

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

    if manager.isInApp == False:
        return
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    normalFont = pygame.font.Font(weight, 16)
    
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
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + 20 + margin[0]
    if direction == "y":
        yIndex += textRect.height + 20 + margin[1]

def button(text, action):
    global xIndex
    global yIndex
    global foreground
    global weight

    if manager.isInApp == False:
        return
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    oldweight = weight
    weight = TEXT_SEMIBOLD

    normalFont = pygame.font.Font(weight, 16)

    weight = oldweight

    oldforeground = foreground

    if primary == BLACK or primary == GREEN or primary == RED or primary == BLUE:
        foreground = WHITE
    
    text = normalFont.render(text, True, foreground)

    foreground = oldforeground

    textRect = text.get_rect()
    textRect.left = x + 10
    textRect.top = y + 10

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hover = False

    if (
        xIndex + textRect.width + 20 > mouse[0] > xIndex
        and yIndex + textRect.height + 20 > mouse[1] > yIndex
    ):
        xIndex -= 2
        yIndex -= 2
        textRect.width += 4
        textRect.height += 4
        hover = True
    else:
        pass

    manager.updateScreen()
    
    x = xIndex + manager.appPos[0] * (1 - manager.appSize)
    y = yIndex + manager.appPos[1] * (1 - manager.appSize)

    pygame.draw.rect(manager.screen, primary, (x, y, textRect.width + 20, textRect.height + 20), round((textRect.height + 20) / 2), 10)

    # borderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)
    
    # pygame.draw.rect(borderSurface, (0, 0, 0), (x, y, textRect.width + 20, textRect.height + 20), 1, 10)
    # pygame.draw.rect(borderSurface, (255, 255, 255), (x - 1, y - 1, textRect.width + 20 + 2, textRect.height + 20 + 2), 1, 10)

    # borderSurface.set_alpha(52)

    # manager.screen.blit(borderSurface, (0, 0))

    if hover:
        xIndex += 2
        yIndex += 2
        textRect.width -= 4
        textRect.height -= 4

    manager.screen.blit(text, textRect)

    if direction == "x":
        xIndex += textRect.width + 20 + margin[0]
    if direction == "y":
        yIndex += textRect.height + 20 + margin[1]
    
    if hover:
        if click[0] == 1:
            if action != None:
                action(manager)

            manager.isInInput = False

def titleBar(text, color=primary):
    global xIndex
    global yIndex
    global foreground
    global weight

    if manager.isInApp == False:
        return

    xIndex = 15
    yIndex = 45

    x = 0 + manager.appPos[0] * (1 - manager.appSize)
    y = 0 + manager.appPos[1] * (1 - manager.appSize)
    width = 400 * manager.appSize + 1
    height = 75 * manager.appSize

    pygame.draw.rect(manager.screen, color, (x, y, width, height))

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