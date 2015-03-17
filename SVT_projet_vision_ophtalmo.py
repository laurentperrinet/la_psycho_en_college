#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

Une expérience simple de mesure de l'acuité en fonction de l'eccentricité

Renvoie un tableau donnant en fonction de l'eccentricité et de la taille la consigne ainsi que le résultat (0 = mauvaise réponse; 1 = bonne réponse).

"""
experiment = 'Ophtalmo'

import numpy as np
# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, gui, misc, data


N_taille, taille_0 = 5, 1.
N_ecc = 3

N_trial_per_condition = 6
N_trial = N_ecc * N_taille * N_trial_per_condition / 2

core_wait = 0.400
core_wait_stim = 0.200

#if no file use some defaults
info = {}
info['observer'] = 'anonymous'
# info['SaveDir'] = '/Users/montagnini.a/WORK/PROJECTS/ECOLE/SVT_projet_vision.py/data'
info['SaveDir'] = 'data'
info['screen_width'] = 51.5
info['screen_distance'] = 57.
info['N_trial_per_condition'] = N_trial_per_condition
import time
info['timeStr'] = time.strftime("%b_%d_%H%M", time.localtime())

try:
    dlg = gui.DlgFromDict(info)
except:
    print('Could not load gui... running with defaut parameters')
    print(info)

# creating data directory
import os
try:
    os.mkdir(info['SaveDir'])
except:
    pass

# creating basic file name
fileName = os.path.join(info['SaveDir'], experiment + '_' + info['observer'] + '_' + info['timeStr'])

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

A la présentation du symbole "?", répondez avec:
    - la touche "<" (gauche) pour le caractère "3" (ou "E" inversée)
    - la touche ">" (droite) pour le caractère "E"

ATTENTION: certaines fois la tâche va être très difficile. Il faut tout
de même obligatoirement répondre!

Notez que l'ordre est aléatoire et donc qu'il ne faut pas nécessairement donner toujours la même réponse.

Pressez sur une de ces 2 touches pour continuer...

"""

# Objets correspondant à la croix de fixation, à la consigne de réponse et aux instructions:
wait_for_next = visual.TextStim(win,
                        text = u"+", units='norm', height=0.15, color='white',
                        pos=[0., -0.], alignHoriz='center', alignVert='center' )
wait_for_response = visual.TextStim(win,
                        text = u"?", units='norm', height=0.15, color='DarkSlateBlue',
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
                # info
                infotxt = visual.TextStim(win,
                                    text = u"Attention!!! : vous etes sortis de l'expérimentation, les résultats ne sont pas sauvés!"), units='norm', height=0.1, color='DarkSlateBlue',
                                    pos=[0., 0.], alignHoriz='center', alignVert='center' )
                infotxt.draw()
                # fixation
                win.flip()
                core.wait(core_wait)
                win.close()
                core.quit()
                return None
            #valid response - check to see if correct
            elif key in ['left', 'right']:
                if key in ['left'] :return 0
                else: return 1
            else:
                visual.TextStim(win, u"pressez < ou > (ou Esc / q pour sortir et annuler l'expérience) (mais pas %s)" %key, height=0.05, color='red').draw()
                win.flip()

# http://www.psychopy.org/general/units.html
def angle2cm(size_in_deg, screen_distance):
    return 2* screen_distance * np.tan(size_in_deg * np.pi / 180. / 2.)

def angle2norm(size_in_deg, screen_distance, screen_width):
    return angle2cm(size_in_deg, screen_distance) / screen_width * 2

def presentStimulus(consigne, eccen, taille):
    """Present stimulus
    """
    stim = visual.TextStim(win, text=u"E", units='norm', height=angle2norm(taille, info['screen_distance'], info['screen_width']), color='black',
                        pos=[angle2norm(eccen, info['screen_distance'], info['screen_width']), 0], alignHoriz='center', alignVert='center',
                        flipHoriz=not(consigne))
    stim.draw()

# initialisation: on montre les instructions
instructions_txt.draw()
win.flip()
getResponse()

#create your list of stimuli
stimList = []
for eccen in np.hstack((np.linspace(-15., -5., N_ecc, endpoint=True), np.linspace(5., 15., N_ecc, endpoint=True))):
    for taille in np.logspace(-1.5, 1.5, N_taille, endpoint=True, base=2) * taille_0: # en degrés d'angle visuel
        for consigne in [0, 1]:
            stimList.append(
                {'eccen':eccen, 'taille':taille, 'consigne':consigne} #this is a python 'dictionary'
                )

#organise them with the trial handler
trials = data.TrialHandler(stimList, info['N_trial_per_condition'])
trials.data.addDataType('result')#this will help store things with the stimuli

# on commence l'expérience
for trial in trials:

    # info
    infotxt = visual.TextStim(win,
                        text = u"{0} / {1}".format(trials.thisN+1, trials.nTotal), units='norm', height=0.1, color='DarkSlateBlue',
                        pos=[-.9, -.9], alignHoriz='center', alignVert='center' )
    infotxt.draw()
    # fixation
    wait_for_next.draw()
    win.flip()
    core.wait(core_wait)
    # stimulus
    infotxt.draw()
    wait_for_next.draw()
    presentStimulus(trial['consigne'], trial['eccen'], trial['taille'])
    win.flip()
    # réponse
    core.wait(core_wait_stim)
    infotxt.draw()
    wait_for_response.draw()
    win.flip()
    #result = getResponse()
    response = getResponse()
    if response == consigne: result=1
    else: result = 0
    trials.data.add('result', result)

win.update()
core.wait(0.5)
win.close()

#save data
trials.printAsText(stimOut=['eccen', 'taille', 'consigne'], #write summary data to screen
                  dataOut=['result_raw'])
trials.saveAsExcel(fileName=fileName.replace('.pickle', ''), # ...or an xlsx file (which supports sheets)
                  sheetName = 'rawData',
                  stimOut=['eccen', 'taille', 'consigne'],
                  dataOut=['result_raw'])
trials.saveAsPickle(fileName=fileName.replace('.pickle', '_data.pickle'))#this saves a copy of the whole object
