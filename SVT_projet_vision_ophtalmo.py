#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

Expérience eccentricité
-----------------------

Une expérience simple de mesure de l'acuité en fonction de l'eccentricité

Renvoie un tableau donnant en fonction de l'eccentricité et de la taille la
consigne ainsi que le résultat (0 = mauvaise réponse; 1 = bonne réponse).


Je propose de commencer par la première manip ("ophtalmo") qui a pour but de se
familiariser avec les mesures psychophysiques en se concentrant sur l'analyse de l'acuité visuelle (donc de la capacité à reconnaitres de petits détails) à differents endroits du champs visuel (on parle de differente eccentricité et on mesure ça en degrés d'angle visuel). Cette manip est fortement liee a' une partie importante traitee dans votre livre de texte en SVT, c'est a' dire la composition non uniforme de la retine, avec beaucoup plus de recepteurs sensibles aux valiations de la lumiere dans l'espace (les cones) concentres dans la region centrale par rapport a' la peripherie. La reconnaissance de la lettre (entre E et 3) repose sur cette sensibilite' et elle est donc meilleure a' petite eccentricite'.

Pour passer l'expérience, chaque étudiant doit se mettre bien devant l'écran et
se concentrer pendant toute la durée.  Au début il faut rentrer des infos à la main:
nombre d'essais par condition - > mettre 5 au minimum, mais si possible 10 (conseil
faire une manip "pilote" avec 1 seul essai par condition pour se rendre compte de
comment ça marche)
largeur de l'écran -> mettre la votre
distance de l'écran -> mettre la votre
repertoire de sauvegarde ... vous savez maintenant!

Après la manip: visualiser la feuille excel pour chaque étudiant
Pour évaluer l'acuité on trace des courbes psychométriques pour eventuellement en
déduire un seuil de discrimination. Dans notre cas, pour une valeur d'eccentricité
donnée (première colonne du fichier excel: valeurs 5, 10 ou 15 avec signe positif
si à droite ou négatif si à gauche du centre) on calcule la fraction de réponses
correctes (quatrième colonne et suivantes: 1=correct, 0=faux) en fonction de la
taille de la cible (deuxième colonne:, cinq valeurs qui vont de 1 jusqu'à 2.828...).
En pratique les élèves devraient:
1) grouper les essais qui correspondent à une même eccentricité (en pratique,
filtre sur la première colonne pour prendre 3 groupes avec: eccentricité=(+5 ou - 5),
(+10 ou - 10), (+15 ou - 15))
2) visualisation: valeurs ordonnées de taille de la lettre sur l'axe X ; moyenne
des reponses (les 0 ert les 1 des colonnes résultats) correspondant à chaque valeur
de taille - conseil utiliser des couleurs differentes pour les trois goupes
correspondants aux trois valeurs d'eccentricité
3) tracer des courbes (fit) à travers les points: typiquement on utilise des
gaussiennes cumulatives, mais une autre fonction raisonnable peut aller aussi
(voir les exemples de courbe psychometrique sur internet, par ex:
http://www.google.fr/imgres?imgurl=http%3A%2F%2Fwebvision.med.utah.edu%2Fimageswv%2FKall04.jpeg&imgrefurl=http%3A%2F%2Fwebvision.med.utah.edu%2Fbook%2Fpart-viii-gabac-receptors%2Fpsychophysics-of-vision%2F&h=601&w=652&tbnid=-MwjAm68cgLGcM%3A&zoom=1&docid=1V4pJlXAqQ4BtM&ei=HXQJVcjHJMHzas-SgKAH&tbm=isch&iact=rc&uact=3&dur=2758&page=1&start=0&ndsp=19&ved=0CC0QrQMwBA):
    cette partie est plus compliquée et on pourra revenir la-dessus. Moi personellement,
    je ne sais pas faire des ajustement de fonctions aux donnees avec excel,
    mais on doit pouvoir trouver :-)
4) dependant de (3): estimer le seuil de discrimination de la lettre pour les trois
eccentricités: le seul est definit comme la valeur de X (taille de la lettre) pour
laquelle la probabilité de donner une reponse correcte (Y dans notre figure) est
égale à 0.75.

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
                        pos=[-.8, -.9], alignHoriz='center', alignVert='center' )
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
    consigne=trial['consigne']
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
