#!/usr/bin/env python

#script for testing screen locations
## creates between 2-4 windows (controlled through number_of_windows) and displays their respective
## screen indices in psychopy

from psychopy import visual, event, core, gui

#### PARAMETERS ####
number_of_windows = 3 # change this to two if you want to check the indices for a setup with two monitors/windows
####################

win0 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor0', units='pix', winType='pyglet',screen=0)
win1 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor1', units='pix', winType='pyglet',screen=1)
if number_of_windows > 2:
    win2 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor2', units='pix', winType='pyglet',screen=2)
if number_of_windows > 3:
    win3 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                monitor='infoMonitor3', units='pix', winType='pyglet',screen=3)
                                 
                                 
text0 = visual.TextStim(win0, "SCREEN INDEX 0", height=60, pos=[0,0], color="white")
text1 = visual.TextStim(win1, "SCREEN INDEX 1", height=60, pos=[0,0], color="white")
if number_of_windows > 2:
    text2 = visual.TextStim(win2, "SCREEN INDEX 2", height=60, pos=[0,0], color="white")
if number_of_windows > 3:
    text3 = visual.TextStim(win3, "SCREEN INDEX 3", height=60, pos=[0,0], color="white")

text0.draw()
text1.draw()
if number_of_windows > 2:
    text2.draw()
if number_of_windows > 3:
    text3.draw()

win0.flip()
win1.flip()
if number_of_windows > 2:
    win2.flip()
if number_of_windows > 3:
    win3.flip()

core.wait(5.0)

win0.close()
win1.close()
if number_of_windows > 2:
    win2.close()
if number_of_windows > 3:
    win3.close()

core.quit()