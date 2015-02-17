#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

Une expérience simple de mesure de l'acuité en fonction de l'eccentricité

"""
experiment = 'ophtalmo'

import numpy as np
# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, gui, misc

#if no file use some defaults
info = {}
info['observer'] = 'anonymous'
info['screen_width'] = 51.5
info['screen_distance'] = 57.
info['nTrials'] = 50

try:
    dlg = gui.DlgFromDict(info)
except:
    print('Could not load gui... running with defaut parameters')
    print(info)

import time
info['timeStr'] = time.strftime("%b_%d_%H%M", time.localtime())
fileName = 'data/' + experiment + info['observer'] + '_' + info['timeStr'] + '.pickle'
#save to a file for future use (ie storing as defaults)
if dlg.OK:
    misc.toFile(fileName, info)
else:
    print('Interrupted gui... quitting')
    core.quit() #user cancelled. quit

# Create a visual window:
win = visual.Window(fullscr=True)

instructions = u"""

Le but de cette expérience est de distinguer la lettre qui est présentée
tout en gardant l'oeil fixé sur la croix centrale.

A la présentation d'un symbole "?", répondez avec:
    - la touche "<" (gauche) pour le charactère "3"
    - la touche ">" (droite) pour le charactère "E"

Pressez sur une de ces 2 touches pour continuer...

"""

# Objets correspondant à la croix de fixation, à la consigne de réponse et aux instructions:
wait_for_next = visual.TextStim(win, 
                        text = u"+", units='norm', height=0.05, color='BlanchedAlmond',
                        pos=[0., -0.], alignHoriz='center', alignVert='center' ) 
wait_for_response = visual.TextStim(win, 
                        text = u"?", units='norm', height=0.05, color='DarkSlateBlue',
                        pos=[0., -0.], alignHoriz='center', alignVert='center' ) 
instructions_txt = visual.TextStim(win, 
                        text = instructions, units='norm', height=0.05, color='BlanchedAlmond',
                        pos=[0., -0.], alignHoriz='center', alignVert='center' ) 

def getResponse():
    event.clearEvents() # clear the event buffer to start with
    resp = None#initially
    while True: # forever until we return a keypress
        for key in event.getKeys():
            #quit
            if key in ['escape', 'q']:
                win.close()
                core.quit()
                return None
            #valid response - check to see if correct
            elif key in ['left', 'right']:
                if key in ['left'] :return -1
                else: return 1
            else:
                visual.TextStim(win, "pressez < ou > (ou Esc pour sortir) (mais pas %s)" %key, height=0.05, color='red').draw()
                win.flip()

def angle2cm(size_in_deg, screen_distance):
    return 2* screen_distance * np.tan(size_in_deg * np.pi / 180. / 2.)

def presentStimulus(consigne, eccen, taille):
    """Present stimulus
    """
    if consigne: texte = u"E"
    else: texte = u"3"
    
    stim = visual.TextStim(win, text = texte, units='cm', height=angle2cm(taille, info['screen_distance']), color='black',
                        pos=[0., angle2cm(eccen, info['screen_distance'])], alignHoriz='center', alignVert='center' )
    stim.draw()

# http://www.psychopy.org/general/units.html
N_ecc = 3
eccen_ = np.linspace(5., 15., N_ecc, endpoint=True) # en degrés d'angle visuel
N_taille = 5
taille_ = np.logspace(-1, 1., N_taille, endpoint=True, base=10) * 2.  # en degrés d'angle visuel
core_wait = 0.100
core_wait_stim = 0.300

# initialisation: on montre les instructions
instructions_txt.draw()
win.flip()
getResponse()

# on commence l'expérience
results = numpy.zeros((4, info['nTrials']))
for i_trial in range(info['nTrials']):
    wait_for_next.draw()
    win.flip()
    core.wait(core_wait)
    consigne = np.random.randint(2) # au hasard E ou 3
    eccen = eccen_[np.random.randint(N_ecc)]
    taille = taille_[np.random.randint(N_taille)]
    presentStimulus(consigne, eccen, taille)
    win.flip()
    core.wait(core_wait_stim)
    wait_for_response.draw()
    win.flip()
    result = getResponse()
    results[0, i_trial] = consigne
    results[1, i_trial] = eccen
    results[2, i_trial] = taille
    results[3, i_trial] = result

win.update()
core.wait(0.5)
win.close()

print results
#save data
fileName = 'data/' + experiment + info['observer'] + '_' + info['timeStr']
numpy.save(fileName, results)