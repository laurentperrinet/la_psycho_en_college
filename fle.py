#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flash_lag Effect




"""

from psychopy import visual, event, core, logging, gui, misc
import time
import numpy as np

# paramètres par défault
w, h = 2560, 1440 # iMac 27''
w, h = 1920, 1200 # cinema display
w, h = 1366, 768 # anthony

#if no file use some defaults
info = {}
info['experiment'] = 'fle' 
info['datapath'] = 'data' 
info['observer'] = 'anonymous'
info['screen_width'] = w
info['screen_height'] = h
info['nTrials'] = 20
info['duration'] = 1. #duration of the stimulus in seconds
info['radius'] = .008
info['step'] = .02
info['pos_flash'] = .5
info['std_flash'] = .05
info['noise'] = .05
info['length'] = .5 # length of the trajectory, 1 is the height of the window


try:
    dlg = gui.DlgFromDict(info)
except:
    print('Could not load gui... running with defaut parameters')
    print(info)

import os
try:
    os.mkdir(info['datapath'])
except:
    pass


info['timeStr'] = 'debug' # time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
fileName = os.path.join(info['datapath'], info['timeStr'] + '_' + info['experiment'] + '_' + info['observer'] + '.pickle')
#save to a file for future use (ie storing as defaults)
if dlg.OK:
    misc.toFile(fileName, info)
else:
    print('Interrupted gui... quitting')
    core.quit() #user cancelled. quit


win = visual.Window([info['screen_width'], info['screen_height']], fullscr=True, units='height')


instructions = u"""

Le but de cette expérience est de suivre un stimulus visuel bleu sur l'écran et de localiser approximativement ca position une fois qu'un flash rouge apparaît au centre de l'écran. Lisez attentivement les étapes avant de commencer l'expérience.


Etapes:

1) Au début de l'éxpérience un cercle de couleur beige apparaît sur l'écran. Utiliser la souris pour cliquer sur ce cercle et démarrer l'expérience.

2) La souris et le cercle beige vont disparaître et le stimulus bleu mobile va apparaître à gauche de l'écran. 

3) Vous devez suivre ce stimulus et vous concentrez sur ca position au moment où le flash rouge apparaît au centre de l'écran.

4) Une fois que le stimulus bleu disparaît la souris et le cercle beige re-apparaîtront. 

5) Vous utiliserez la souris pour cliquer à l'endroit où vous avez perçues le point bleu lors de l'apparition du flash. 

6) Appuyer ensuite sur le cercle beige pour répéter les étapes 1 à 5. 

7) Vous devez faire cette exercice 30 fois. 


 Cliquer sur l'écran si vous avez lu et compris les étapes.

"""

myMouse = event.Mouse()  #  will use win by default

#On construit les differents cercles et l'arriere plan.
stim = visual.Circle(win, units='height', 
        radius = info['radius'],
        interpolate = True, fillColor='Navy',
        autoLog=False)#this stim changes too much for autologging to be useful

flash = visual.Circle(win, units='height', 
        radius = info['radius'],
        interpolate = True, fillColor='Red',
        autoLog=True)#this stim changes too much for autologging to be useful

fixation = visual.Circle(win, units='height', 
        pos=[0., 0.3], radius = 0.03,
        interpolate = True, fillColor='BlanchedAlmond',
        autoLog=True)#this stim changes too much for autologging to be useful

wait_for_response = visual.TextStim(win, 
                        text = u"?", units='norm', height=0.15, color='DarkSlateBlue',
                        pos=[0., -0.], alignHoriz='center', alignVert='center' ) 
fixation_t = visual.TextStim(win, 
                        text = u"+", units='norm', height=0.15, color='BlanchedAlmond',
                        pos=[0., 0.3], alignHoriz='center', alignVert='center' ) 
                        
instructions_txt = visual.TextStim(win,
                        text = instructions, units='norm', height=0.05, color='White',
                        pos=[0., 0.], alignHoriz='center', alignVert='center' )

#Tant que la souris est visible il y a pas de stimuli sur l'ecran.
#Une fois stimuli lance on enregistre la nouvelle position de la souris.
def getResponse():
    #myMouse.setPos((0, 0))
    myMouse.setVisible(1)
    event.clearEvents()#clear the event buffer to start with
    resp = None#initially
    while 1:#forever until we return mouse events
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        if (mouse1):
            return myMouse.getRel()
            
# initialisation: on montre les instructions
instructions_txt.draw()
win.flip()
getResponse()


#Quand le stimulus bleu mobile apparait la souris disparait. 
#Tant que le stimulus present est inferieur a "duration" le flash rouge n'apparait pas, sinon il apparait.
clock = core.Clock()
def presentStimulus(pos_flash, noise_flash):
    """Present stimulus
    """
    clock.reset()
    myMouse.setVisible(0)
    did_flash = False
    while clock.getTime() < info['duration']:
        fixation.draw()
        stim.setPos(( info['length']*(np.float(clock.getTime()/info['duration'])-.5), info['step']/2))
        stim.draw()
        if not(did_flash) and (clock.getTime() / info['duration']) > pos_flash:
            flash.setPos(( info['length']*(np.float(clock.getTime()/info['duration'])-.5) + noise_flash, -info['step']/2))
            flash.draw()
            did_flash = True
            #print clock.getTime(), np.float(clock.getTime()/info['duration'])-.5, stim.pos
        win.flip()

#On va dessiner le stimuli et faire une mise a jour de la fenetre pour le nombre de nTrials.
#Tant que la souris est visible pas de stimuli.
#le flash rouge apparait pas toujours au centre il peut ce deplace a gauche ou a droite apres chaque trial.
#On print les reponses du positionnement des flash rouges et des reponses choisis.
results = np.zeros((4, info['nTrials']))
for i_trial in range(info['nTrials']):
    fixation.draw()
    win.flip()
    while not(myMouse.isPressedIn(fixation)):#forever until we return mouse events
        mouse1, mouse2, mouse3 = myMouse.getPressed()
    pos_flash = info['pos_flash'] + (np.random.rand()-.5)*info['std_flash'] # a random number between 0 and 1
    noise_flash = np.random.randn()*info['noise']
    presentStimulus(pos_flash, noise_flash)
    #wait_for_response.draw()
    win.flip()
    ans = getResponse()
    print (ans)
    results[0, i_trial] = .5*ans[0]+.5
    results[1, i_trial] = .5*ans[1]+.5
    results[2, i_trial] = pos_flash
    results[3, i_trial] = noise_flash

win.update()
core.wait(0.5)

win.close()

#save data
fileName = os.path.join(info['datapath'], info['timeStr'] + '_' + info['experiment'] + '_' + info['observer'] + '.npy')
np.save(fileName, results)