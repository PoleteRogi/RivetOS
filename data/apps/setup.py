from lib.style import *

def whatIsYourNamePage():
    manager.setupIndex = 1
    manager.charIndex = 0
    manager.loadingIndicator = pygame.image.load('./assets/icons/system/SpinLoading.png').convert_alpha()
    manager.loadingIndicator = pygame.transform.scale(manager.loadingIndicator, (40, 40))

    manager.setTimeout(loadPage, 10000)

def loadPage():
    manager.updateStartupData()

def init(m):
    m.setupIndex = 0
    m.setTimeout(whatIsYourNamePage, 5000)
    pass

def setup(m):
    global xIndex
    global yIndex
    set_direction('y')

    initApp(m)
    
    if m.setupIndex == 0:
        imageWidth = 50
        imageHeight = 65
        imageX = 400 / 2 - imageWidth / 2
        imageY = 800 / 2 - imageHeight / 2

        image('icons/system/RivetLight.png', isAlpha=True, size=(imageWidth, imageHeight), pos=(imageX, imageY))
    
    if m.setupIndex == 1:
        set_weight(TEXT_BOLD)
        set_text_size(32)
        
        text = 'RivetOS'

        if m.charIndex < len(text):
            m.charIndex += 0.01

        set_foreground(modify_color(background, 0.9))
        label(text, center=True)
        set_foreground(foreground)
        label(text[0:round(m.charIndex)], center=True)

        # Spinning Loading Indicator

        # m.loadingIndicator = pygame.transform.rotate(m.loadingIndicator, 1)
        
        # raw(m.loadingIndicator)

        m.updateScreen()