from lib.style import *

def init(m):
    m.input = 'Input'

def click(m):
    m.alert('Test', 'XD')

def clickNotify(m):
    m.notify('Debug', 'Test', 'This is a notification')

def debug(m):
    set_direction('y')

    initApp(m)

    title = titleBar('Debug')

    inpt = input('m.input', 100, None)

    text = label('Label')

    btn = button('Button', None)

    dialogBtn = button('Open dialog', click)

    notificationBtn = button('Notify', clickNotify)