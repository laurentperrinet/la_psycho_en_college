#!/usr/bin/env python
from psychopy import visual, event, core, logging, gui, misc
import time
import numpy as np

try:
    fileName = 'data/2016-03-03_fle_anonymous'
    info = misc.fromFile(fileName + '.pickle')
    results = np.load(fileName + '.npy')

except:
    w, h = 2560, 1440 # iMac 27''
    w, h = 1920, 1200 # cinema display

    #if no file use some defaults
    info = {}
    info['observer'] = 'anonymous'
    info['screen_width'] = w
    info['screen_height'] = h
    info['nTrials'] = 30
    info['duration'] = 1. #duration of the stimulus in seconds
    info['radius'] = .006
    info['step'] = .02
    info['pos_flash'] = .5
    info['std_flash'] = .05
    info['noise'] = .05
    info['length'] = .5 # length of the trajectory, 1 is the height of the window

    experiment = 'fle'

    try:
        dlg = gui.DlgFromDict(info)
    except:
        print('Could not load gui... running with defaut parameters')
        print(info)
        
    info['timeStr'] = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    fileName = 'data/' + info['timeStr'] + '_' + experiment + '_' + info['observer'] + '.pickle'
    #save to a file for future use (ie storing as defaults)
    if dlg.OK:
        misc.toFile(fileName, info)
    else:
        print('Interrupted gui... quitting')
        core.quit() #user cancelled. quit


    win = visual.Window([info['screen_width'], info['screen_height']], fullscr=True, units='height')

    myMouse = event.Mouse()  #  will use win by default

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
                            
    def getResponse():
        #myMouse.setPos((0, 0))
        myMouse.setVisible(1)
        event.clearEvents()#clear the event buffer to start with
        resp = None#initially
        while 1:#forever until we return mouse events
            mouse1, mouse2, mouse3 = myMouse.getPressed()
            if (mouse1):
                return myMouse.getRel()
            elif mouse3 or mouse2:
                win.close()
                core.quit()
                return None 

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

    results = np.zeros((4, info['nTrials']))
    for i_trial in range(info['nTrials']):
        fixation.draw()
        win.flip()
        while not(myMouse.isPressedIn(fixation)):#forever until we return mouse events
            mouse1, mouse2, mouse3 = myMouse.getPressed()
            if mouse3 or mouse2:
                win.close()
                core.quit()
        pos_flash = info['pos_flash'] + (np.random.rand()-.5)*info['std_flash'] # a random number between 0 and 1
        noise_flash = np.random.randn()*info['noise']
        presentStimulus(pos_flash, noise_flash)
        #wait_for_response.draw()
        win.flip()
        ans = getResponse()
        print (ans)
        results[0, i_trial] = ans[0]
        results[1, i_trial] = ans[1]
        results[2, i_trial] = pos_flash
        results[3, i_trial] = noise_flash

    win.update()
    core.wait(0.5)

    win.close()

    #save data
    fileName = 'data/' + info['timeStr'] + '_' + experiment + '_' + info['observer']
    np.save(fileName, results)

print (fileName)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)
ax.scatter(results[2, :], results[0, :], c='r')
ax.scatter(results[2, :], results[1, :] + .3, c='b')
ax.plot([info['pos_flash']-info['std_flash'], info['pos_flash']+info['std_flash']], [info['length']*(info['pos_flash']-info['std_flash']-.5), info['length']*(info['pos_flash']+info['std_flash']-.5)], 'g--')
#pylab.axis([0., 1., -1.1, 1.1])
ax.set_xlabel('position')
error = results[0, :]/info['length']+.5-(results[2, :]-results[3, :])
ax.text(info['pos_flash']-info['std_flash'], info['length']*(info['pos_flash']+info['std_flash']-.5), 'FLE = %0.2f ' % np.mean(error) + '+/- %0.2f ' %  np.std(error))
fig.savefig('fle.pdf')
print('Done')   