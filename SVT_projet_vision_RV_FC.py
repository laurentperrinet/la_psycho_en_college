#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Une expérience simple de recherche visuelle
===========================================

Cas dit de "recherche de conjonction d'attributs" parce-que la cible recherchée
est définie par deux attributs et elle ne `saute'' à l'oeil

Renvoie un tableau donnant l'exactitude de la réponse (colonnes "results":
1=réponse correcte; 0=réponse fausse) et les temps de réaction (colonnes RT) en
fonction de la position de la cible (colonne "pos_indx"),
de la configuration (colonne "config", ça correspond à combien d'éléments sont
présentés) et de la consigne (colonne "consigne": 1=cible présente,
0=cible absente).

Cette expérience devrait résulter relativement difficile (en tout cas moins facile
de la précedente, sur la recherche visuelle dite de "pop-out").
Pour passer l'expérience, chaque étudiant doit se mettre bien devant l'écran et se
concentrer pendant toute la durée. Il faut essayer de donner
la réponse rapidement sans pour autant se tromper.
Au début il faut rentrer des infos à la main:
nombre d'essais par condition - > mettre 5 au minimum, plus pour des résultats
plus précis (conseil: faire une manip "pilote" avec 1 seul essai par condition
pour se rendre compte de comment ça marche et du temps nécessaire)
largeur de l'écran -> mettre la votre
distance de l'écran -> mettre la votre
repertoire de sauvegarde ... vous savez maintenant!

Après la manip: visualiser la feuille excel pour chaque élève
A partir de la feuille excel on peu visualiser les temps de réaction en fonction
du nombre d'éléments présents dans la scène. La difficulté d’une tâche de recherche
visuelle se reflète dans la pente de cette function (RT en function du nombre d’éléments).
En pratique les élèves devraient:
1) séléctionner les essais avec une réponse correcte (colonne results=1)
2) grouper les essais qui correspondent à une même configuration (en pratique,
filtre sur la colonne config pour prendre 3 groupes avec: config=2, 4 ou 8 ainsi
que à une même consigne (colonne consigne = 1 ou 0)
3) visualisation: valeurs ordonnées de config sur l'axe X ; moyenne des temps de
réaction correspondant à chaque valeur de config - conseil utiliser des couleurs
differentes pour les deux condition “cible présente” et “cible absente”.
3) tracer des droites à travers les points:  il s’agit d’une régression linéaire.
4) Comparer les résultats: Observer si les temps de reaction augmentent plus ou
moins en function du nombre d’éléments quand la cible est présente plutôt que
absente et dans cette experience plutôt que dans l’autre experience de recherché
visuelle.

"""
experiment = 'RV_FC'

import numpy as np
from numpy.random import *
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
info['SaveDir'] = '/Users/montagnini.a/WORK/PROJECTS/ECOLE/SVT_projet_vision.py/data'
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
fileName = 'data/' + experiment + '_' + info['observer'] + '_' + info['timeStr'] + '.pickle'
#save to a file for future use (ie storing as defaults)
if dlg.OK:
    misc.toFile(fileName, info)
else:
    print('Interrupted gui... quitting')
    core.quit() #user cancelled. quit

# Create a visual window:
win = visual.Window(fullscr=True)

instructions = u"""

Le but de cette expérience est de dire si la lettre E de couleur rouge est presentée (ou pas)
parmi des distracteurs (des E de couleur vert ou des 3 de couleur rouge), tout en gardant bien l'oeil fixé sur la croix centrale.

Après la présentation des stimuli, répondez le plus rapidement possible avec:
    - la touche ">" (droite) si le caractère "E" rouge est présent
    - la touche "<" (gauche) si le caractère "E" rouge est absent

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
                win.close()
                core.quit()
                return None
            #valid response - check to see if correct
            elif key in ['left', 'right']:
                RT = stopwatch.getTime()   # --> RT in seconds
                if key in ['left'] :return [0,RT]
                else: return [1,RT]
            else:
                visual.TextStim(win, "pressez < ou > (ou Esc pour sortir) (mais pas %s)" %key, height=0.05, color='red').draw()
                win.flip()

# http://www.psychopy.org/general/units.html
def angle2cm(size_in_deg, screen_distance):
    return 2* screen_distance * np.tan(size_in_deg * np.pi / 180. / 2.)

def angle2norm(size_in_deg, screen_distance, screen_width):
    return angle2cm(size_in_deg, screen_distance) / screen_width * 2

def presentStimulus(consigne, pos_indx, config):
    """Present stimulus and distractors
    """
    if consigne==1:
        target_color = 'red'
    else: target_color = 'green'
    stim_xpos = angle2norm(eccentricity * xfac[pos_indx], info['screen_distance'], info['screen_width'])
    stim_ypos = angle2norm(eccentricity * yfac[pos_indx], info['screen_distance'], info['screen_width'])
    stim = visual.TextStim(win, text=u"E", units='norm', height=angle2norm(taille, info['screen_distance'], info['screen_width']), color=target_color,
                        pos=[stim_xpos, stim_ypos],
                        alignHoriz='center', alignVert='center', flipHoriz=not(consigne))
    stim.draw()
    for i in np.arange(config-1):
       flip = randint(2)
       if flip==1: # distractor = 3
          distr_col = 'red'
       else: distr_col = 'green'
       pos_shift = np.remainder(pos_indx + (i+1)*(8/config),8)
       distr_xpos = angle2norm(eccentricity * xfac[pos_shift], info['screen_distance'], info['screen_width'])
       distr_ypos = angle2norm(eccentricity * yfac[pos_shift], info['screen_distance'], info['screen_width'])
       distr = visual.TextStim(win, text=u"E", units='norm', height=angle2norm(taille, info['screen_distance'], info['screen_width']), color=distr_col,
                    pos=[distr_xpos, distr_ypos],
                    alignHoriz='center', alignVert='center', flipHoriz=flip)
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
    # fixation
    wait_for_next.draw()
    win.flip()
    core.wait(core_wait)
    # stimulus
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
