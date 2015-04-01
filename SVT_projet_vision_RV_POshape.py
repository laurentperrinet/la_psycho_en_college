#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

Une expérience simple de recherche visuelle
"""
experiment = 'RV'

import numpy as np
# Import key parts of the PsychoPy library:
from psychopy import visual, core, event, gui, misc, data

N_config = 3
N_presence = 2
N_trial_per_condition = 5
N_trial = N_config * N_presence * N_trial_per_condition * 8

eccentricity = 6
taille = 2
xfac = [1,np.sqrt(2)/2,0,-np.sqrt(2)/2,-1,-np.sqrt(2)/2,0,np.sqrt(2)/2]
yfac = [0,np.sqrt(2)/2,1,np.sqrt(2)/2,0,-np.sqrt(2)/2,-1,-np.sqrt(2)/2]

stopwatch = core.Clock()
core_wait = 0.500
core_wait_stim = 0.500

#if no file use some defaults
info = {}
info['observer'] = 'anonymous'
#info['SaveDir'] = '/Users/montagnini.a/WORK/PROJECTS/ECOLE/SVT_projet_vision.py/data'
info['SaveDir'] = 'data'
info['screen_width'] = 30
info['screen_distance'] = 40.
info['N_trial_per_condition'] = N_trial_per_condition


try:
    dlg = gui.DlgFromDict(info)
except:
    print('Could not load gui... running with default parameters')
    print(info)

import time
info['timeStr'] = time.strftime("%b_%d_%H%M", time.localtime())
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

Le but de cette expérience est de dire si la lettre E est presentée (ou pas)
parmi des distracteurs (des chiffres 3), tout en gardant bien l'oeil fixé sur la croix centrale.

Après la présentation des stimuli, répondez le plus rapidement possible avec:
    - la touche ">" (droite) si le caractère "E" est présent 
    - la touche "<" (gauche) si le caractère "E" est absent 

ATTENTION: certaines fois la tache va etre plus difficile que d'autres. Il faut toujours rester concentrés, bien
fixer la croix centrale et essayer de donner la réponse correcte le plus rapidement possible.
En bas à gauche de l'écran vous verrez défiler le nombre de l'essai courant: ne vous faites pas distraire par cela,
c'est une information que votre binome peut surveiller et vous en informer de temps en temps.
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
                                    text = u"Attention!!! : vous etes sortis de l'expérimentation, les résultats ne sont pas sauvés!", units='norm', height=0.1, color='DarkSlateBlue',
                                    pos=[0., 0.], alignHoriz='center', alignVert='center' )
                infotxt.draw()
                # fixation
                win.flip()
                core.wait(2.0)
                win.close()
                core.quit()
                return None
            #valid response - check to see if correct
            elif key in ['left', 'right']:
                RT = stopwatch.getTime()   # --> RT in seconds
                if key in ['left'] :return [0,RT]
                else: return [1,RT]
            else:
                visual.TextStim(win, u"pressez < ou > (ou Esc / q pour sortir et annuler l'expérience) (mais pas %s)" %key, height=0.05, color='red').draw()
                win.flip()

# http://www.psychopy.org/general/units.html
def angle2cm(size_in_deg, screen_distance):
    return 2* screen_distance * np.tan(size_in_deg * np.pi / 180. / 2.)

def angle2norm(size_in_deg, screen_distance, screen_width):
    return angle2cm(size_in_deg, screen_distance) / screen_width * 2

def presentStimulus(consigne, pos_indx, config):
    """Present stimulus and distractors
    """
    stim_xpos = angle2norm(eccentricity * xfac[pos_indx], info['screen_distance'], info['screen_width'])
    stim_ypos = angle2norm(eccentricity * yfac[pos_indx], info['screen_distance'], info['screen_width'])
    stim = visual.TextStim(win, text=u"E", units='height', height=angle2norm(taille, info['screen_distance'], info['screen_width']), color='black',
                        pos=[stim_xpos, stim_ypos], 
                        alignHoriz='center', alignVert='center', flipHoriz=not(consigne))
    stim.draw()
    for i in np.arange(config-1):
       pos_shift = np.remainder(pos_indx + (i+1)*(8/config),8)
       distr_xpos = angle2norm(eccentricity * xfac[pos_shift], info['screen_distance'], info['screen_width'])
       distr_ypos = angle2norm(eccentricity * yfac[pos_shift], info['screen_distance'], info['screen_width'])
       distr = visual.TextStim(win, text=u"E", units='height', height=angle2norm(taille, info['screen_distance'], info['screen_width']), color='black',
                    pos=[distr_xpos, distr_ypos], 
                    alignHoriz='center', alignVert='center', flipHoriz=1)
       distr.draw()

# initialisation: on montre les instructions
instructions_txt.draw()
win.flip()
getResponse()


#create your list of stimuli
stimList = []
for pos_indx in [0,1,2,3,4,5,6,7]:
    for config in [2,4,8]: # en degrés d'angle visuel
        for consigne in [0, 1]:
            stimList.append(
                {'pos_indx':pos_indx, 'config':config, 'consigne':consigne} #this is a python 'dictionary'
                )

#organise them with the trial handler
trials = data.TrialHandler(stimList, info['N_trial_per_condition'])
trials.data.addDataType('result')#this will help store things with the stimuli

# on commence l'expérience
for trial in trials:
    # info
    infotxt = visual.TextStim(win,
                        text = u"{0} / {1}".format(trials.thisN+1, trials.nTotal), units='norm', height=0.1, color='DarkSlateBlue',
                        pos=[-.8, -.9], alignHoriz='center', alignVert='center' )
    infotxt.draw()
    # fixation
    wait_for_next.draw()
    win.flip()
    core.wait(core_wait)
    # stimulus
    infotxt.draw()
    wait_for_next.draw()
    presentStimulus(trial['consigne'], trial['pos_indx'], trial['config'])
    win.flip()
    stopwatch.reset()
    # réponse
#    core.wait(core_wait_stim)
#    wait_for_response.draw()
 #   win.flip()
    #result = getResponse()
    [response, respRT] = getResponse()
#   if response == consigne: result=1
 #   else: result = 0
    if response == consigne: result=1
    else: result = 0
    trials.data.add('result', result)
    trials.data.add('RT', respRT)

win.update()
core.wait(0.5)
win.close()

#save data
trials.printAsText(stimOut=['pos_indx', 'config', 'consigne'], #write summary data to screen
                  dataOut=['result_raw','RT_raw'])
trials.saveAsExcel(fileName=fileName.replace('.pickle', ''), # ...or an xlsx file (which supports sheets)
                  sheetName = 'rawData',
                  stimOut=['pos_indx', 'config', 'consigne'],
                  dataOut=['result_raw','RT_raw'])
#trials.saveAsPickle(fileName=fileName.replace('.pickle', '_data.pickle'))#this saves a copy of the whole object  