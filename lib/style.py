import pygame

BLACK = (57, 62, 65)
WHITE = (246, 247, 235)
GREEN = (68, 187, 164)
RED = (233, 79, 55)
BLUE = (63, 136, 197)

foreground = BLACK
background = WHITE

TEXT_LIGHT = './assets/fonts/ProximaNova/Proxima Nova Light.otf'
TEXT_REGULAR = './assets/fonts/ProximaNova/Proxima Nova Reg.otf'
TEXT_SEMIBOLD = './assets/fonts/ProximaNova/Proxima Nova Semibold.otf'
TEXT_BOLD = './assets/fonts/ProximaNova/Proxima Nova Bold.otf'
TEXT_BLACK = './assets/fonts/ProximaNova/Proxima Nova Black.otf'

# VARIABLES
primary = GREEN
secondary = BLACK
weight = TEXT_REGULAR

padding = [20, 20, 20, 20]
margin = [5, 10]

xIndex = padding[0] 
yIndex = padding[1]

direction = 'x'

manager = None

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

    direction = 'x'

def initApp(m):
    global manager
    global xIndex
    global yIndex
    global surface

    xIndex = padding[0] 
    yIndex = padding[1]

    manager = m

    pygame.draw.rect(manager.screen, background, (400 / 2 - 400 * manager.appSize / 2, 800 / 2 - 800 * manager.appSize / 2, 400 * manager.appSize, 800 * manager.appSize))

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
    
    normalFont = pygame.font.Font(weight, 16)

    text = normalFont.render(text, True, foreground)

    textRect = text.get_rect()
    textRect.left = xIndex
    textRect.top = yIndex

    manager.screen.blit(text, textRect)

    if direction == 'x':
        xIndex += textRect.width + margin[0]
    if direction == 'y':
        yIndex += textRect.height + margin[1]

def titleBar(text, color=primary):
    global xIndex
    global yIndex
    global foreground
    global weight

    if manager.isInApp == False:
        return

    xIndex = 15
    yIndex = 45

    pygame.draw.rect(manager.screen, color, (0, 0, 400, 75))

    if color == BLACK or color == GREEN or color == RED or color == BLUE:
        foreground = WHITE

    lastWeight = weight

    weight = TEXT_SEMIBOLD

    label(text)

    if color == BLACK or color == GREEN or color == RED or color == BLUE:
        foreground = BLACK

    weight = lastWeight

    # outline and border
    outlineBorderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    pygame.draw.rect(outlineBorderSurface, (0, 0, 0), (0, 75 - 1, 400, 1))
    pygame.draw.rect(outlineBorderSurface, (255, 255, 255), (0, 75, 400, 1))

    outlineBorderSurface.set_alpha(51.2)

    manager.screen.blit(outlineBorderSurface, (0, 0))

    xIndex = padding[0]
    yIndex = 75 + padding[1]