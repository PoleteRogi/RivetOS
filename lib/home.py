import pygame
import lib.style as style
from datetime import datetime
import math
import json

# LOAD WALLPAPER IMAGE
wallpaper = None

# STRETCH IT TO SCREEN SIZE

isLockscreen = True

alpha = 1
wallpaperScale = 1.5
iconScale = 20

sin = 0

wallpaperScaleGoal = 1
iconScaleGoal = 20

firstFrame = True

appIcons = []


def appslist():
    appfileopen = open("./data/apps.json")
    content = appfileopen.read()
    appfileopen.close()

    return json.loads(content)


apps = appslist()


def render(screen, events, manager):
    global alpha
    global wallpaperScale
    global wallpaperScaleGoal
    global wallpaperScaled
    global wallpaper
    global sin
    global isLockscreen
    global apps
    global firstFrame
    global iconScale
    global iconScaleGoal

    if firstFrame:
        firstFrame = False
        wallpaper = pygame.image.load("./assets/wallpaper.png").convert()
        wallpaper = pygame.transform.scale(wallpaper, (400, 800))

    sin += 0.01

    s = pygame.Surface(
        (400, 800), pygame.SRCALPHA
    )  # per-pixel alpha              # notice the alpha value in the color

    if alpha < 256:
        alpha += (256 - alpha) / 10

    if alpha > 256:
        alpha = 256

    if wallpaperScale > wallpaperScaleGoal:
        wallpaperScale -= (wallpaperScale - wallpaperScaleGoal) / 10

    if wallpaperScale < wallpaperScaleGoal:
        wallpaperScale += (wallpaperScaleGoal - wallpaperScale) / 10

    if iconScale > iconScaleGoal:
        iconScale -= (iconScale - iconScaleGoal) / 5

    if iconScale < iconScaleGoal:
        iconScale += (iconScaleGoal - iconScale) / 5

    # wallpaperScale = wallpaperScale * (((math.sin(sin) + 1) / 2) / 10) + 1
    wallpaperScaled = pygame.transform.scale(
        wallpaper, (400 * wallpaperScale, 800 * wallpaperScale)
    )

    s.set_alpha(alpha)

    s.blit(
        wallpaperScaled,
        (400 / 2 - 400 * wallpaperScale / 2, 800 / 2 - 800 * wallpaperScale / 2),
    )

    if isLockscreen:
        lockscreenTimeFont = pygame.font.Font(style.TEXT_SEMIBOLD, 168)

        now = datetime.now()

        hours = now.strftime("%H")
        minutes = now.strftime("%M")

        hourText = lockscreenTimeFont.render(hours, True, style.foreground)

        hourTextRect = hourText.get_rect()
        hourTextRect.center = (400 // 2, 400 // 2)

        minuteText = lockscreenTimeFont.render(minutes, True, style.foreground)

        minuteTextRect = minuteText.get_rect()
        minuteTextRect.center = (400 // 2, (400 // 2) + 168 - 10)

        s.blit(hourText, hourTextRect)
        s.blit(minuteText, minuteTextRect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                isLockscreen = False

    else:
        wallpaperScaleGoal = 1.2
        iconScaleGoal = 1

    index = 0

    row = 0
    column = 0
    for app in apps:
        name = app["name"]
        icon = app["icon"]
        file = app["file"]

        # 3 ROWS
        # 3 COLUMNS

        columnsize = ((400) / 3) - 20
        rowsize = ((610) / 3) - 20

        iconsize = 73

        if len(appIcons) <= index:
            iconimg = pygame.image.load("./assets/apps/" + icon).convert()
            appIcons.append(iconimg)

        x = (
            (column * columnsize + 10 * 3) * iconScale
            + (columnsize / 2)
            - (iconsize / 2)
        )
        y = (row * rowsize + 10 * 3) + (rowsize / 2) - (iconsize / 2)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            x + iconsize > mouse[0] > x
            and y + iconsize > mouse[1] > y
            and manager.isInApp == False
        ):
            iconsize = 83
            x -= 5
            y -= 5
            if click[0] == 1:
                # OPEN APP
                manager.openApp(file)

        else:
            iconsize = 73

        image = pygame.transform.scale(appIcons[index], (iconsize, iconsize))

        size = image.get_size()
        rect = pygame.Surface(size, pygame.SRCALPHA)

        pygame.draw.rect(rect, (255, 255, 255), (0, 0, *size), border_radius=50)

        image = image.copy().convert_alpha()
        image.blit(rect, (0, 0), None, pygame.BLEND_RGBA_MIN)

        s.blit(image, (x, y))

        normalFont = pygame.font.Font(style.TEXT_REGULAR, 16)

        appNameText = normalFont.render(name, True, style.foreground)

        appNameTextRect = appNameText.get_rect()
        appNameTextRect.center = (
            x + (iconsize / 2),
            y + (iconsize / 2) + iconsize - 20,
        )

        s.blit(appNameText, appNameTextRect)

        outlineSurface = pygame.Surface(
            (400, 800), pygame.SRCALPHA
        )  # per-pixel alpha              # notice the alpha value in the color

        pygame.draw.rect(
            outlineSurface,
            (0, 0, 0),
            pygame.Rect(
                (column * columnsize + 10 * 3) * iconScale
                + (columnsize / 2)
                - (iconsize / 2)
                - 2,
                (row * rowsize + 10 * 3) + (rowsize / 2) - (iconsize / 2) - 2,
                iconsize + 4,
                iconsize + 4,
            ),
            2,
            100,
        )

        outlineSurface.set_alpha(25.6)

        s.blit(outlineSurface, (0, 0))

        # UPDATE INDEX
        index += 1
        column += 1
        if column > 2:
            column = 0
            row += 1

    dockSurface = pygame.Surface((400, 800), pygame.SRCALPHA)

    dock = pygame.draw.rect(
        dockSurface,
        (255, 255, 255),
        (0, 800 - 100 + ((iconScale / 20 * 100)), 400, 100),
        400,
    )

    dockSurface.set_alpha(256 - (iconScale / 20 * 128) - 128)

    s.blit(dockSurface, (0, 0))

    screen.blit(s, (0, 0))
