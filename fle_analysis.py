#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flash_lag Effect




"""
#Sauvegarde les donnees et on fait un graphique des resultats
import os
from psychopy import misc

#fileName = os.path.join(info['datapath'], info['timeStr'] + '_' + info['experiment'] + '_' + info['observer'] + '.pickle')
fileName = os.path.join('data', '2016-03-29_163136_fle_anonymous')
fileName = os.path.join('data', '2016-03-29_171633_fle_anonymous')
fileName = os.path.join('data', 'debug_fle_anonymous')
print (fileName)
info = misc.fromFile(fileName + '.pickle')
print(info)
import numpy as np
results = np.load(fileName + '.npy')
print(results[0, :])

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)
ax.scatter(results[2, :], results[0, :], c='r', label=u'perçu')
ax.scatter(results[2, :], results[2, :], c='b', marker='.',label=u'réel')
#ax.plot([info['pos_flash']-info['std_flash'], info['pos_flash']+info['std_flash']], [info['length']*(info['pos_flash']-info['std_flash']-.5), info['length']*(info['pos_flash']+info['std_flash']-.5)], 'g--')
ax.plot([info['pos_flash']-info['std_flash'], info['pos_flash']+info['std_flash']], [info['pos_flash']-info['std_flash'], info['pos_flash']+info['std_flash']], 'g--')
#pylab.axis([0., 1., -1.1, 1.1])
ax.set_xlabel(u'position du flash') 
ax.set_ylabel(u'position reportée / cliquée')
ax.legend()
error = results[0, :]-(results[2, :]-results[3, :])
ax.text(.46, .6, 'FLE = %0.2f ' % np.mean(error) + '+/- %0.2f ' %  np.std(error))
fig.savefig('fle.pdf')
print('Done')