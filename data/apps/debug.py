from lib.style import *

def click(m):
    m.alert('Test', 'XD')

def debug(m):
    set_direction('y')

    initApp(m)

    title = titleBar('Debug')

    inpt = input('Input', 100, None)

    text = label('Label')

    btn = button('Button', None)

    dialogBtn = button('Open dialog', click)