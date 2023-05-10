import pygame
import lib.style as style
from datetime import datetime
import math
import json
import os.path
from os import path

# LOAD WALLPAPER IMAGE
wallpaper = None

# STRETCH IT TO SCREEN SIZE

isLockscreen = True

alpha = 1
wallpaperScale = 1.5
iconScale = 20

wallpaperScaleGoal = 1
iconScaleGoal = 20

firstFrame = True

appIcons = []
appIconsScaled = []

normalFont = None
lockscreenTimeFont = None

lastHovers = []

hasTakenHomeScreenshot = False
homeScreenshot = None
homeScreenshotNoBlur = None

def appslist():
    appfileopen = open("./data/apps.json")
    content = appfileopen.read()
    appfileopen.close()

    return json.loads(content)


apps = appslist()

sin = 0

def render(screen, events, manager):
    global alpha
    global wallpaperScale
    global wallpaperScaleGoal
    global wallpaperScaled
    global wallpaper
    global isLockscreen
    global apps
    global firstFrame
    global iconScale
    global iconScaleGoal
    global lockscreenTimeFont
    global normalFont
    global lastHovers
    global hasTakenHomeScreenshot
    global homeScreenshot
    global homeScreenshotNoBlur
    global sin

    sin += 1

    if firstFrame:
        firstFrame = False
        
        wallpaper = pygame.image.load("./assets/block.png").convert()
        wallpaper = pygame.transform.scale(wallpaper, (400, 800))
        normalFont = pygame.font.Font(style.TEXT_REGULAR, 16)
        lockscreenTimeFont = pygame.font.Font(style.TEXT_SEMIBOLD, 168)

    if homeScreenshot == None and path.exists("./data/tmp/homescreen.png"):
        homeScreenshot = pygame.image.load("./data/tmp/homescreen.png").convert()
    
    if homeScreenshotNoBlur == None and path.exists("./data/tmp/homescreennoblur.png"):
        homeScreenshotNoBlur = pygame.image.load('./data/tmp/homescreennoblur.png').convert()

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

    compareString = str(wallpaperScaleGoal)[:5]

    if '.' in compareString:
        compareString = compareString + '00'
    else:
        compareString = compareString + '.000'

    if str(wallpaperScale)[:5] != compareString and not ('999' in str(wallpaperScale)):
        if manager.appSize < 0.00001:
            wallpaperScaled = pygame.transform.scale(
                wallpaper, (400 * wallpaperScale, 800 * wallpaperScale)
            )
        else:
            wallpaperScaled = pygame.transform.scale(
                homeScreenshot, (400 * (wallpaperScale - 0.2), 800 * (wallpaperScale - 0.2))
            )

        manager.updateScreen()

    if alpha != 256:
        s.set_alpha(alpha)

    if manager.appSize < 0.00001:
        s.blit(
            wallpaperScaled,
            (400 / 2 - 400 * wallpaperScale / 2, 800 / 2 - 800 * wallpaperScale / 2),
        )
    else:
        s.blit(
            wallpaperScaled,
            (400 / 2 - 400 * (wallpaperScale - 0.2) / 2, 800 / 2 - 800 * (wallpaperScale - 0.2) / 2),
        )

        realWallpaperScaled = pygame.transform.scale(
            homeScreenshotNoBlur, (400 * (wallpaperScale - 0.2), 800 * (wallpaperScale - 0.2))
        )

        s2 = pygame.Surface(
            (400, 800), pygame.SRCALPHA
        )  # per-pixel alpha              # notice the alpha value in the color

        s2.set_alpha(int(pow(1 - manager.appSize, 25) * 256))

        s2.blit(
            realWallpaperScaled,
            (400 / 2 - 400 * ((wallpaperScale - 0.2) / 2), 800 / 2 - 800 * ((wallpaperScale - 0.2) / 2)),
        )

        s.blit(s2, (0, 0))

    if isLockscreen:
        now = datetime.now()

        hours = now.strftime("%H")
        minutes = now.strftime("%M")

        hourText = lockscreenTimeFont.render(hours, True, style.foreground)

        hourTextRect = hourText.get_rect()
        hourTextRect.center = (400 // 2, 800 // 2 - 168 / 2)

        minuteText = lockscreenTimeFont.render(minutes, True, style.foreground)

        minuteTextRect = minuteText.get_rect()
        minuteTextRect.center = (400 // 2, (800 // 2 - 168 / 2) + 168 - 10)

        s.blit(hourText, hourTextRect)
        s.blit(minuteText, minuteTextRect)

        wallpaperScaleGoal = 1.1 + math.sin(sin / 100) * 0.1

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                isLockscreen = False
                wallpaperScaleGoal = 1.2
    else:
        iconScaleGoal = 1
        
        index = 0

        row = 0
        column = 0
        
        if (iconScale > 0.9999 and iconScale < 1.0001) and hasTakenHomeScreenshot == False and manager.isInApp == False:
            hasTakenHomeScreenshot = True
            manager.hasToTakeScreenshot = True

        for app in apps:
            renderAppsAfter = True

            name = app["name"]
            icon = app["icon"]
            file = app["file"]

            if len(lastHovers) - 1 != index:
                lastHovers.append(index)

            # 3 ROWS
            # 3 COLUMNS

            columnsize = ((400) / 3) - 20
            rowsize = ((610) / 3) - 20

            iconsize = 73

            if len(appIcons) <= index:
                iconimg = pygame.image.load("./assets/apps/" + icon).convert_alpha()
                appIcons.append(iconimg)
                image = pygame.transform.scale(appIcons[index], (iconsize, iconsize))
                appIconsScaled.append(image)

            else:
                image = appIconsScaled[index]

            originX = (
                (column * columnsize + 10 * 4) * iconScale
                + (columnsize / 2)
                - (iconsize / 2)
            )
            originY = (row * rowsize + 10 * 4) + (rowsize / 2) - (iconsize / 2)

            x = originX
            y = originY

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            hover = False

            if (
                x + iconsize > mouse[0] > x
                and y + iconsize > mouse[1] > y
                and manager.isInApp == False
            ):
                hover = True
                iconsize = 83
                x -= 5
                y -= 5
                if click[0] == 1:
                    appPos = (originX + iconsize / 2, originY + iconsize / 2)
                    # OPEN APP
                    manager.openApp(file, appPos)
                    wallpaperScaleGoal = 2

                if (file.split('.')[0] in manager.openApps) == False:
                    image = pygame.transform.scale(appIcons[index], (iconsize, iconsize))
            else:
                hover = False
                iconsize = 73
            
            renderOtherApps = True

            if file.split('.')[0] in manager.openApps:
                iconsize = 73 + (727 * manager.appSize)
                image = pygame.transform.scale(appIcons[index], (iconsize, iconsize))

                x = originX * (1 - manager.appSize) + (400 / 2 - iconsize / 2) * manager.appSize
                y = originY * (1 - manager.appSize) + (800 / 2 - iconsize / 2) * manager.appSize

                # x = manager.appPos[0] * (1 - manager.appSize)
            
            else: 
                if manager.appSize > 0.00001:
                    renderAppsAfter = False

            if lastHovers[index] != hover:
                manager.updateScreen()

            if renderAppsAfter:
                lastHovers[index] = hover

                size = image.get_size()
                rect = pygame.Surface(size, pygame.SRCALPHA)

                pygame.draw.rect(rect, (255, 255, 255), (0, 0, *size), border_radius=50)

                image.blit(rect, (0, 0), None, pygame.BLEND_RGBA_MIN)

                s.blit(image, (x, y))

                appNameText = normalFont.render(name, True, style.foreground)    

                appNameTextRect = appNameText.get_rect()
                appNameTextRect.center = (
                    x + (iconsize / 2),
                    y + (iconsize / 2) + iconsize - 20,
                )

                rect.set_alpha((1 - pow(manager.appSize, 10)) * 256)

                if manager.appSize < 0.0001:
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

                # outlineSurface.set_alpha(25.)

                # s.blit(outlineSurface, (0, 0))

            # UPDATE INDEX
            index += 1
            column += 1
            if column > 2:
                column = 0
                row += 1

    screen.blit(s, (0, 0))