from lib.style import *

def whatIsYourNamePage():
    manager.setupIndex = 1
    manager.charIndex = 0
    manager.loadingIndicatorOriginal = pygame.image.load('./assets/icons/system/SpinLoading.png').convert_alpha()
    manager.loadingIndicatorOriginal = pygame.transform.scale(manager.loadingIndicatorOriginal, (40, 40))

    manager.setTimeout(loadPage, 10000)

def loadPage():
    manager.updateStartupData()

def init(m):
    m.setupIndex = 0
    m.appPos = (0, 0)
    m.appSize = 1
    m.setTimeout(whatIsYourNamePage, 5000)
    pass

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

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

        print(m.charIndex)

        set_foreground((lerp(WHITE[0], BLACK[0], m.charIndex / 6), lerp(WHITE[1], BLACK[1], m.charIndex / 6), lerp(WHITE[2], BLACK[2], m.charIndex / 6)))
        label(text, center=True)
        set_foreground(foreground)

        # Spinning Loading Indicator

        angle = m.charIndex * 500
        x = 400 / 2
        y = 800 - 400 / 2

        rotated_image = pygame.transform.rotate(m.loadingIndicatorOriginal, angle)
        new_rect = rotated_image.get_rect(center = m.loadingIndicatorOriginal.get_rect(center = (x, y)).center)

        m.loadingIndicator = rotated_image
        
        m.screen.blit(m.loadingIndicator, new_rect)

        m.updateScreen()