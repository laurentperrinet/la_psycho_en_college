#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Demo: show a very basic program: hello world

"""

# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, gui, misc

# Create a visual window:
win = visual.Window(fullscr=True)

# Create (but not yet display) some text:
msg1 = visual.TextStim(win, text=u"Bonjour à tous!")  # default position = centered

# Draw the text to the hidden visual buffer:
msg1.draw()
visual.TextStim(win, text=u"en bas", pos=(0, -0.3)).draw()
visual.TextStim(win, text=u"X", pos=(0, -1.), color='red').draw()
visual.TextStim(win, text=u"X", pos=(0, 1.), color='blue').draw()
visual.TextStim(win, text=u"en haut", pos=(0, 0.3)).draw()
visual.TextStim(win, text=u"X", pos=(-1, 0.), color='green').draw()
visual.TextStim(win, text=u"X", pos=(1, 0.), color='green').draw()

# Show the hidden buffer--everything that has been drawn since the last win.flip():
win.flip()

# Wait 3 seconds so people can see the message, then we are exiting gracefully (in a puff of dust):
core.wait(3)
win.close()
