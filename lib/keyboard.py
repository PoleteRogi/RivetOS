import pygame
import lib.style as style

def init(m):
    pass

keyboardPosScale = 0
keyboardPosScaleGoal = 0

def render(m):
    global keyboardPosScale
    global keyboardPosScaleGoal
    if m.isInInput:
        keyboardPosScaleGoal = 1
    else:
        keyboardPosScaleGoal = 0

    if keyboardPosScale < keyboardPosScaleGoal:
        keyboardPosScale += (keyboardPosScaleGoal - keyboardPosScale) / 3

    if keyboardPosScale > keyboardPosScaleGoal:
        keyboardPosScale -= (keyboardPosScale - keyboardPosScaleGoal) / 3

    if keyboardPosScale >= 0.999:
        keyboardPosScale = 1

    pygame.draw.rect(m.screen, (253, 254, 242), (0, 800 - 216 + 216 * (1 - keyboardPosScale), 400, 216))
    
    button(m, '')

def button(m, key):
    borderSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    pygame.draw.rect(borderSurface, (0, 0, 0), (0, 800 - 216 + 216 * (1 - keyboardPosScale), 400, 1))

    width = 100
    height = 36

    x = 400 / 2 - width / 2
    y = 800 - 216 + (216 / 2) - (height / 2) + 216 * (1 - keyboardPosScale)

    buttonRect = (x, y, width, height)

    pygame.draw.rect(borderSurface, (0, 0, 0), buttonRect, 1, 10)

    borderSurface.set_alpha(52)

    m.screen.blit(borderSurface, (0, 0))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (
        x + width > mouse[0] > x
        and y + height > mouse[1] > y
    ):
        hoverSurface = pygame.Surface((400, 800), pygame.SRCALPHA)
        hoverSurface.set_alpha(25.6)
        
        pygame.draw.rect(hoverSurface, (0, 0, 0), buttonRect, int(height / 2), 10)

        m.screen.blit(hoverSurface, (0, 0))

        if click[0] == 1:
            m.keyboardInput('A')