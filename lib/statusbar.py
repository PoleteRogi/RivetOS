import pygame
import lib.style as style
from datetime import datetime

normalFont = None
titleFont = None

import threading

manager = None

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    
    manager.threadings.append(t)

    return t

def init(m):
    global normalFont
    global titleFont
    global manager
    global lockscreenTimeFont
    global blurredscreenimage

    manager = m

    normalFont = pygame.font.Font(style.TEXT_REGULAR, 16)
    titleFont = pygame.font.Font(style.TEXT_SEMIBOLD, 18)

    set_interval(m.updateScreen, 1)

showedNotifications = []

currentNotification = None
notificationShowValueGoal = 0
notificationShowValue = 0

from threading import Timer  
 
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs) 
    t.start()
    manager.threadings.append(t) 
    return t

def closeNotification():
    global notificationShowValueGoal
    notificationShowValueGoal = 0

def renderNotifications():
    global currentNotification
    global notificationShowValueGoal
    global notificationShowValue
    for notification in manager.notifications:
        if not (notification in showedNotifications):
            showedNotifications.append(notification)

            currentNotification = notification
            notificationShowValueGoal = 1
            # notificationShowValue = 0

            setTimeout(closeNotification, 2000)
    
    if notificationShowValue > notificationShowValueGoal:
        notificationShowValue -= (notificationShowValue - notificationShowValueGoal) / 5

    if notificationShowValue < notificationShowValueGoal:
        notificationShowValue += (notificationShowValueGoal - notificationShowValue) / 5

    if notificationShowValue >= 0.999:
        notificationShowValue = 1
    
    if notificationShowValue <= 0.001:
        notificationShowValue = 0
        currentNotification = None

    if currentNotification != None:
        NOTIFICATION_WIDTH = 360
        NOTIFICATION_HEIGHT = 100
        NOTIFICATION_X = (400 / 2 - NOTIFICATION_WIDTH / 2)
        NOTIFICATION_Y = 20 - (NOTIFICATION_HEIGHT + 40) * (1 - notificationShowValue)

        pygame.draw.rect(manager.screen, style.WHITE, (NOTIFICATION_X, NOTIFICATION_Y, NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT), border_radius=10)

        pygame.draw.rect(manager.screen, style.modify_color(style.WHITE, 0.8), (NOTIFICATION_X, NOTIFICATION_Y, NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT), width=1, border_radius=10)

        titleText = titleFont.render(notification.title, True, style.BLACK)
        manager.screen.blit(titleText, (NOTIFICATION_X + 20, NOTIFICATION_Y + 20))

        contentText = normalFont.render(notification.text, True, style.BLACK)
        manager.screen.blit(contentText, (NOTIFICATION_X + 20, NOTIFICATION_Y + 20 + 18 + 10))
    
    if notificationShowValue != 0 and notificationShowValue != notificationShowValueGoal:
        manager.updateScreen()

def renderControlCenter():
    backgroundS = pygame.Surface((400, 800), pygame.SRCALPHA)     
    backgroundS.fill((255, 255, 255))

    foregroundS = pygame.Surface((400, 800), pygame.SRCALPHA)     

    if controlCenterOpened:
        backgroundS.set_alpha(225)
        foregroundS.set_alpha(256)
    else:
        backgroundS.set_alpha(0)
        foregroundS.set_alpha(0)

    now = datetime.now()

    time = now.strftime("%H:%M")

    timeText = normalFont.render(time, True, style.foreground)

    timeTextRect = timeText.get_rect()
    timeTextRect.center = (400 // 2, 30)

    foregroundS.blit(timeText, timeTextRect)

    # battery = psutil.sensors_battery()

    # percent = str(battery.percent)
    percent = '100'

    percentText = normalFont.render(percent + '%', True, style.foreground)

    percentTextRect = percentText.get_rect()
    percentTextRect.right = 400 - 60
    percentTextRect.centery = 60 // 2

    foregroundS.blit(percentText, percentTextRect)

    index = 0

    for notification in manager.notifications:
        NOTIFICATION_WIDTH = 360
        NOTIFICATION_HEIGHT = 100
        NOTIFICATION_X = (400 / 2 - NOTIFICATION_WIDTH / 2)
        NOTIFICATION_Y = 60 + index * (NOTIFICATION_HEIGHT + 10)

        pygame.draw.rect(foregroundS, style.WHITE, (NOTIFICATION_X, NOTIFICATION_Y, NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT), border_radius=10)

        pygame.draw.rect(foregroundS, style.modify_color(style.WHITE, 0.8), (NOTIFICATION_X, NOTIFICATION_Y, NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT), width=1, border_radius=10)

        titleText = titleFont.render(notification.title, True, style.BLACK)
        foregroundS.blit(titleText, (NOTIFICATION_X + 20, NOTIFICATION_Y + 20))

        contentText = normalFont.render(notification.text, True, style.BLACK)
        foregroundS.blit(contentText, (NOTIFICATION_X + 20, NOTIFICATION_Y + 20 + 18 + 10))

        index += 1

    manager.screen.blit(backgroundS, (0, 0))
    manager.screen.blit(foregroundS, (0, 0))

controlCenterOpened = False

def render(home, screen, events):
    global controlCenterOpened
    now = datetime.now()
    
    # if manager.isInApp:
        # pygame.draw.rect(manager.screen, style.background, (0, 0, 400, 30))

    if notificationShowValue < 0.5:
        if home.isLockscreen == False and controlCenterOpened == False:
            time = now.strftime("%H:%M")

            timeText = normalFont.render(time, True, style.foreground)

            timeTextRect = timeText.get_rect()
            timeTextRect.center = (400 // 2, (30 // 2))

            screen.blit(timeText, timeTextRect)

    # battery = psutil.sensors_battery()

    #percent = str(battery.percent)
    percent = '100'

    percentText = normalFont.render(percent + '%', True, style.foreground)

    percentTextRect = percentText.get_rect()
    percentTextRect.right = 400 - 8
    percentTextRect.centery = 30 // 2

    if controlCenterOpened == False:
        screen.blit(percentText, percentTextRect)

    mouse = pygame.mouse.get_pos()

    barLimit = 30

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and mouse[1] <= barLimit:
            controlCenterOpened = not controlCenterOpened

    renderControlCenter()

    renderNotifications()

    # dynamic island
    # pygame.draw.rect(screen, (0, 0, 0), (400 / 2 - 100 / 2, 7, 100, 24), 12, 50)