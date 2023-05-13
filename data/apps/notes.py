from lib.style import *

def init(m):
    m.notesText = m.read_file('notes/notes.txt')
    m.lastNotesText = m.notesText

def autosave(m):
    if m.notesText != m.lastNotesText:
        m.lastNotesText = m.notesText

        m.write_file('notes/notes.txt', m.notesText)

def notes(m):
    initApp(m)

    # title = titleBar('Notes', color=GREEN)

    # txtArea = textArea('m.notesText', 400, 500)

    # autosave(m)