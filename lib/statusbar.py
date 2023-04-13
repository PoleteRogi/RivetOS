import pygame
import lib.style as style
from datetime import datetime
import psutil

normalFont = None

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
    global manager

    manager = m

    normalFont = pygame.font.Font(style.TEXT_REGULAR, 16)

    set_interval(m.updateScreen, 1)

def render(home, screen):
    now = datetime.now()

    if home.isLockscreen == False:
        time = now.strftime("%H:%M")

        timeText = normalFont.render(time, True, style.foreground)

        timeTextRect = timeText.get_rect()
        timeTextRect.center = (400 // 2, (30 // 2))

        screen.blit(timeText, timeTextRect)

    battery = psutil.sensors_battery()

    plugged = battery.power_plugged
    percent = str(battery.percent)
    
    percentText = normalFont.render(percent + '%', True, style.background)

    percentTextRect = percentText.get_rect()
    percentTextRect.right = 400 - 8
    percentTextRect.centery = 30 // 2

    screen.blit(percentText, percentTextRect)