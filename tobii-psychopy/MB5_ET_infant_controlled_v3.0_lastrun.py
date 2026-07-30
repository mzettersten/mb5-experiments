#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.1.3),
    on Fri 31 Jul 10:09:16 2026
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from Tobii_SDK_connect
import tobii_research as tr
from psychopy import visual
from psychopy import sound, core
import time

win = visual.Window(fullscr=True)

## Create a 440 Hz test tone, 2 seconds long
#test = sound.Sound(value=440, secs=2.0)  # no device argument
#test.setVolume(1.0)
## Play the sound
#test.play()
## Wait for the sound to finish
#core.wait(test.getDuration())
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.1.3'
expName = 'Test'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'order_number': '644',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1920, 1080]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/marcus/Documents/Python_Repos/mb5-experiments/tobii-psychopy/MB5_ET_infant_controlled_v3.0_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('data')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('data')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=True, allowStencil=False,
            monitor='testMonitor', color=(0.0000, 0.0000, 0.0000), colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = (0.0000, 0.0000, 0.0000)
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Start_ET" ---
    start_image = visual.ImageStim(
        win=win,
        name='start_image', 
        image='materials/MB5_logo.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    # Run 'Begin Experiment' code from Tobii_SDK_connect
    #set runtime variables
    #trial order file name
    print(expInfo)
    trial_file = "trials/order_"+str(int(expInfo['order_number']))+".csv"
    
    
    found_eyetrackers = tr.find_all_eyetrackers()
    if not found_eyetrackers:
        raise RuntimeError("No Tobii eye trackers found!")
    
    my_eyetracker = found_eyetrackers[0]
    print(f"Using eye tracker: {my_eyetracker}")
    
    latest_gaze = {}
    
    def gaze_callback(gaze_sample):
        latest_gaze.clear()
        latest_gaze.update(gaze_sample.copy())
    
    def get_current_gaze():
    
        if not latest_gaze:
            return None
    
        left = latest_gaze.get('left_gaze_point_on_display_area')
        right = latest_gaze.get('right_gaze_point_on_display_area')
    
        left_valid = latest_gaze.get('left_gaze_point_validity') == 1
        right_valid = latest_gaze.get('right_gaze_point_validity') == 1
    
        left_x = left[0] if left and left_valid else None
        left_y = left[1] if left and left_valid else None
        right_x = right[0] if right and right_valid else None
        right_y = right[1] if right and right_valid else None
    
        if left_x is not None and right_x is not None:
            aspect = win.size[0] / win.size[1]
            gaze_x = (((left_x + right_x) / 2) - 0.5) * aspect
            gaze_y = 0.5 - ((left_y + right_y) / 2)
            return (gaze_x, gaze_y)
    
        elif left_x is not None:
            aspect = win.size[0] / win.size[1]
            gaze_x = (left_x - 0.5) * aspect
            gaze_y = 0.5 - left_y
            return (gaze_x, gaze_y)
    
        elif right_x is not None:
            aspect = win.size[0] / win.size[1]
            gaze_x = (right_x - 0.5) * aspect
            gaze_y = 0.5 - right_y
            return (gaze_x, gaze_y)
    
        else:
            return None
    
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_callback, as_dictionary=True)
    print('ET started')
    
    # --- Initialize components for Routine "Exp_Start_Screen" ---
    starter_image = visual.ImageStim(
        win=win,
        name='starter_image', units='norm', 
        image='materials/bunnies.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(2, 2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    start_exp_key_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Laughing_Baby" ---
    baby_video = visual.MovieStim(
        win, name='baby_video',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0), size=(1.8,1), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    
    # --- Initialize components for Routine "Familiarization" ---
    ROI_Familiarization = visual.Rect(
        win=win, name='ROI_Familiarization',
        width=(0.75, 0.75)[0], height=(0.75, 0.75)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=(0.0000, 0.0000, 0.0000), fillColor=(0.0000, 0.0000, 0.0000),
        opacity=None, depth=0.0, interpolate=True)
    imgFam = visual.ImageStim(
        win=win,
        name='imgFam', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.75, 0.75),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    
    # --- Initialize components for Routine "Central_Fixation" ---
    central_fixation = visual.MovieStim(
        win, name='central_fixation',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0), size=(0.7,0.4), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    
    # --- Initialize components for Routine "Test_Period" ---
    ROI_right = visual.Rect(
        win=win, name='ROI_right',
        width=(0.75, 0.75)[0], height=(0.75, 0.75)[1],
        ori=0.0, pos=(0.8, 0), draggable=False, anchor='center-right',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=(0.0000, 0.0000, 0.0000), fillColor=(0.0000, 0.0000, 0.0000),
        opacity=None, depth=0.0, interpolate=True)
    ROI_left = visual.Rect(
        win=win, name='ROI_left',
        width=(0.75, 0.75)[0], height=(0.75, 0.75)[1],
        ori=0.0, pos=(-0.8, 0), draggable=False, anchor='center-left',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=(0.0000, 0.0000, 0.0000), fillColor=(0.0000, 0.0000, 0.0000),
        opacity=None, depth=-1.0, interpolate=True)
    imgLeft = visual.ImageStim(
        win=win,
        name='imgLeft', 
        image=None, mask=None, anchor='center-left',
        ori=0.0, pos=(-0.8, 0), draggable=False, size=(0.75, 0.75),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    imgRight = visual.ImageStim(
        win=win,
        name='imgRight', 
        image=None, mask=None, anchor='center-right',
        ori=0.0, pos=(0.8, 0), draggable=False, size=(0.75, 0.75),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    
    # --- Initialize components for Routine "Stop_ET" ---
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='materials/MB5_logo.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Start_ET" ---
    # create an object to store info about Routine Start_ET
    Start_ET = data.Routine(
        name='Start_ET',
        components=[start_image],
    )
    Start_ET.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for Start_ET
    Start_ET.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Start_ET.tStart = globalClock.getTime(format='float')
    Start_ET.status = STARTED
    thisExp.addData('Start_ET.started', Start_ET.tStart)
    Start_ET.maxDuration = None
    # keep track of which components have finished
    Start_ETComponents = Start_ET.components
    for thisComponent in Start_ET.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Start_ET" ---
    thisExp.currentRoutine = Start_ET
    Start_ET.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *start_image* updates
        
        # if start_image is starting this frame...
        if start_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_image.frameNStart = frameN  # exact frame index
            start_image.tStart = t  # local t and not account for scr refresh
            start_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_image.started')
            # update status
            start_image.status = STARTED
            start_image.setAutoDraw(True)
        
        # if start_image is active this frame...
        if start_image.status == STARTED:
            # update params
            pass
        
        # if start_image is stopping this frame...
        if start_image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > start_image.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                start_image.tStop = t  # not accounting for scr refresh
                start_image.tStopRefresh = tThisFlipGlobal  # on global time
                start_image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'start_image.stopped')
                # update status
                start_image.status = FINISHED
                start_image.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Start_ET,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Start_ET.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Start_ET.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Start_ET.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start_ET" ---
    for thisComponent in Start_ET.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Start_ET
    Start_ET.tStop = globalClock.getTime(format='float')
    Start_ET.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Start_ET.stopped', Start_ET.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if Start_ET.maxDurationReached:
        routineTimer.addTime(-Start_ET.maxDuration)
    elif Start_ET.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "Exp_Start_Screen" ---
    # create an object to store info about Routine Exp_Start_Screen
    Exp_Start_Screen = data.Routine(
        name='Exp_Start_Screen',
        components=[starter_image, start_exp_key_resp],
    )
    Exp_Start_Screen.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for start_exp_key_resp
    start_exp_key_resp.keys = []
    start_exp_key_resp.rt = []
    _start_exp_key_resp_allKeys = []
    # store start times for Exp_Start_Screen
    Exp_Start_Screen.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Exp_Start_Screen.tStart = globalClock.getTime(format='float')
    Exp_Start_Screen.status = STARTED
    thisExp.addData('Exp_Start_Screen.started', Exp_Start_Screen.tStart)
    Exp_Start_Screen.maxDuration = None
    # keep track of which components have finished
    Exp_Start_ScreenComponents = Exp_Start_Screen.components
    for thisComponent in Exp_Start_Screen.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Exp_Start_Screen" ---
    thisExp.currentRoutine = Exp_Start_Screen
    Exp_Start_Screen.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *starter_image* updates
        
        # if starter_image is starting this frame...
        if starter_image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            starter_image.frameNStart = frameN  # exact frame index
            starter_image.tStart = t  # local t and not account for scr refresh
            starter_image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(starter_image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'starter_image.started')
            # update status
            starter_image.status = STARTED
            starter_image.setAutoDraw(True)
        
        # if starter_image is active this frame...
        if starter_image.status == STARTED:
            # update params
            pass
        
        # *start_exp_key_resp* updates
        waitOnFlip = False
        
        # if start_exp_key_resp is starting this frame...
        if start_exp_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_exp_key_resp.frameNStart = frameN  # exact frame index
            start_exp_key_resp.tStart = t  # local t and not account for scr refresh
            start_exp_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_exp_key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_exp_key_resp.started')
            # update status
            start_exp_key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(start_exp_key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(start_exp_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if start_exp_key_resp.status == STARTED and not waitOnFlip:
            theseKeys = start_exp_key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _start_exp_key_resp_allKeys.extend(theseKeys)
            if len(_start_exp_key_resp_allKeys):
                start_exp_key_resp.keys = _start_exp_key_resp_allKeys[-1].name  # just the last key pressed
                start_exp_key_resp.rt = _start_exp_key_resp_allKeys[-1].rt
                start_exp_key_resp.duration = _start_exp_key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Exp_Start_Screen,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Exp_Start_Screen.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Exp_Start_Screen.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Exp_Start_Screen.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Exp_Start_Screen" ---
    for thisComponent in Exp_Start_Screen.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Exp_Start_Screen
    Exp_Start_Screen.tStop = globalClock.getTime(format='float')
    Exp_Start_Screen.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Exp_Start_Screen.stopped', Exp_Start_Screen.tStop)
    # check responses
    if start_exp_key_resp.keys in ['', [], None]:  # No response was made
        start_exp_key_resp.keys = None
    thisExp.addData('start_exp_key_resp.keys',start_exp_key_resp.keys)
    if start_exp_key_resp.keys != None:  # we had a response
        thisExp.addData('start_exp_key_resp.rt', start_exp_key_resp.rt)
        thisExp.addData('start_exp_key_resp.duration', start_exp_key_resp.duration)
    thisExp.nextEntry()
    # the Routine "Exp_Start_Screen" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trialLoop = data.TrialHandler2(
        name='trialLoop',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(expInfo['order_number'] + ".csv"), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(trialLoop)  # add the loop to the experiment
    thisTrialLoop = trialLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
    if thisTrialLoop != None:
        for paramName in thisTrialLoop:
            globals()[paramName] = thisTrialLoop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrialLoop in trialLoop:
        trialLoop.status = STARTED
        if hasattr(thisTrialLoop, 'status'):
            thisTrialLoop.status = STARTED
        currentLoop = trialLoop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
        if thisTrialLoop != None:
            for paramName in thisTrialLoop:
                globals()[paramName] = thisTrialLoop[paramName]
        
        # --- Prepare to start Routine "Laughing_Baby" ---
        # create an object to store info about Routine Laughing_Baby
        Laughing_Baby = data.Routine(
            name='Laughing_Baby',
            components=[baby_video],
        )
        Laughing_Baby.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        baby_video.setMovie('materials/baby_video_grey.mp4')
        # Run 'Begin Routine' code from code_attention_check
        # ---------- BEGIN ROUTINE ----------
        trialClock = core.Clock()
        roiClock = core.Clock()
        videoStarted = False
        videoStartTime = None
        gazeTime = 0
        gazeInROI = False
        continueRoutine = True
        sampleIndex = 0
        # Load Video Stim
        baby_video.setAutoDraw(False)
        baby_video.stop()
        baby_video.seek(0)
        # draw 1st frame and clear (attempt to solve black flash screen)
        baby_video.draw()
        win.clearBuffer()
        
        # Reset Audio Stim
        baby_sound = sound.Sound(r'materials\\baby_sound.wav')
        baby_sound.setVolume(1.0)
        soundPlayed = False
        
        # Get aspect ratio
        aspect = win.size[0] / win.size[1]
        
        # Define ROI
        x0 = -aspect / 2
        x1 =  aspect / 2
        y0 = -0.5
        y1 =  0.5
        
        print('Attention check started')
        # store start times for Laughing_Baby
        Laughing_Baby.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Laughing_Baby.tStart = globalClock.getTime(format='float')
        Laughing_Baby.status = STARTED
        thisExp.addData('Laughing_Baby.started', Laughing_Baby.tStart)
        Laughing_Baby.maxDuration = None
        # keep track of which components have finished
        Laughing_BabyComponents = Laughing_Baby.components
        for thisComponent in Laughing_Baby.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Laughing_Baby" ---
        thisExp.currentRoutine = Laughing_Baby
        Laughing_Baby.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrialLoop, 'status') and thisTrialLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *baby_video* updates
            
            # if baby_video is stopping this frame...
            if baby_video.status == STARTED:
                if bool(False) or baby_video.isFinished:
                    # keep track of stop time/frame for later
                    baby_video.tStop = t  # not accounting for scr refresh
                    baby_video.tStopRefresh = tThisFlipGlobal  # on global time
                    baby_video.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'baby_video.stopped')
                    # update status
                    baby_video.status = FINISHED
                    baby_video.setAutoDraw(False)
            # Run 'Each Frame' code from code_attention_check
            # Get current time
            currentTime = trialClock.getTime()
            # Get current gaze
            gazePos = get_current_gaze()
            
            if gazePos is not None:
                gazeX, gazeY = gazePos
                # Check if gaze is anywhere on the screen ROI
                if x0 <= gazeX <= x1 and y0 <= gazeY <= y1:
                    if not videoStarted:
                        baby_video.setAutoDraw(True)
                        baby_video.play()
                        videoStarted = True
                        videoStartTime = t
                        if not soundPlayed:
                            baby_sound.play()
                            soundPlayed = True
            else:
                gazeX, gazeY = None, None
                
            # ---------- SAVE RAW GAZE SAMPLE ----------
            
            sampleIndex += 1
            thisExp.addData('gaze_sample_index', sampleIndex)
            thisExp.addData('gaze_time', currentTime)
            # Make a safe copy of latest_gaze to prevent thread issues
            current_sample = latest_gaze.copy() if latest_gaze else None
            # Save all raw gaze fields from latest_gaze
            if current_sample is not None:
                keys = list(current_sample.keys())
                for k in keys:
                    thisExp.addData(k, current_sample[k])
            else:
                thisExp.addData('no_gaze_data', 1)
            
            # End routine after 3 seconds
            if videoStarted and videoStartTime is not None:
                if t - videoStartTime >= 3.0:
                    continueRoutine = False
                    
            # Optional: allow escape key to quit experiment
            if 'escape' in event.getKeys():
                core.quit()
            
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=Laughing_Baby,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Laughing_Baby.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Laughing_Baby.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Laughing_Baby.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Laughing_Baby" ---
        for thisComponent in Laughing_Baby.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Laughing_Baby
        Laughing_Baby.tStop = globalClock.getTime(format='float')
        Laughing_Baby.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Laughing_Baby.stopped', Laughing_Baby.tStop)
        baby_video.setAutoDraw(False)
        baby_video.stop()  # ensure movie has stopped at end of Routine
        # Run 'End Routine' code from code_attention_check
        baby_video.stop()
        baby_sound.stop()
        # not sure this is needed
        # baby_video.seek(0)
        # baby_video.setAutoDraw(False)
        # the Routine "Laughing_Baby" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "Familiarization" ---
        # create an object to store info about Routine Familiarization
        Familiarization = data.Routine(
            name='Familiarization',
            components=[ROI_Familiarization, imgFam],
        )
        Familiarization.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        imgFam.setImage(familiar_stimulus_path)
        # Run 'Begin Routine' code from code_familiarization
        # Timer for this trial
        trialClock = core.Clock()  # overall max display time
        roiClock = core.Clock()    # timer for fixation in ROI
        
        # Gaze tracking
        gazeTime = 0  # will store the gaze time inside ROI
        sampleIndex = 0
        inROI = 0
        gazeInROI = False
        
        fam_sound = sound.Sound(r'materials\\familiarization_sound.wav')
        fam_sound.setVolume(1.0)
        #print("Duration:", Fam.getDuration())
        fam_sound.play()
        
        # Define ROI
        x0, y0 = ROI_Familiarization.pos[0] - ROI_Familiarization.size[0]/2, ROI_Familiarization.pos[1] - ROI_Familiarization.size[1]/2
        x1, y1 = ROI_Familiarization.pos[0] + ROI_Familiarization.size[0]/2, ROI_Familiarization.pos[1] + ROI_Familiarization.size[1]/2
        
        # Read times from Excel
        minTime = float(familiarization_time)   # time required in ROI to end routine
        maxTime = float(familiarization_time_timeout)  # maximum trial duration
        
        print('Fam started')
        # store start times for Familiarization
        Familiarization.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Familiarization.tStart = globalClock.getTime(format='float')
        Familiarization.status = STARTED
        thisExp.addData('Familiarization.started', Familiarization.tStart)
        Familiarization.maxDuration = None
        # keep track of which components have finished
        FamiliarizationComponents = Familiarization.components
        for thisComponent in Familiarization.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Familiarization" ---
        thisExp.currentRoutine = Familiarization
        Familiarization.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrialLoop, 'status') and thisTrialLoop.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *ROI_Familiarization* updates
            
            # if ROI_Familiarization is starting this frame...
            if ROI_Familiarization.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ROI_Familiarization.frameNStart = frameN  # exact frame index
                ROI_Familiarization.tStart = t  # local t and not account for scr refresh
                ROI_Familiarization.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ROI_Familiarization, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'ROI_Familiarization.started')
                # update status
                ROI_Familiarization.status = STARTED
                ROI_Familiarization.setAutoDraw(True)
            
            # if ROI_Familiarization is active this frame...
            if ROI_Familiarization.status == STARTED:
                # update params
                pass
            
            # *imgFam* updates
            
            # if imgFam is starting this frame...
            if imgFam.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                imgFam.frameNStart = frameN  # exact frame index
                imgFam.tStart = t  # local t and not account for scr refresh
                imgFam.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(imgFam, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'imgFam.started')
                # update status
                imgFam.status = STARTED
                imgFam.setAutoDraw(True)
            
            # if imgFam is active this frame...
            if imgFam.status == STARTED:
                # update params
                pass
            # Run 'Each Frame' code from code_familiarization
            # Get current time
            currentTime = trialClock.getTime()
            # Get current gaze position from latest_gaze
            gazePos = get_current_gaze()  # returns (x, y) or None
            
            if gazePos is not None:
                gazeX, gazeY = gazePos
            
                # Check if gaze is inside ROI
                if x0 <= gazeX <= x1 and y0 <= gazeY <= y1:
                    inROI = 1
                    if not gazeInROI:       # first frame in ROI
                        roiClock.reset()
                        gazeInROI = True
                    gazeTime = roiClock.getTime()  # update gazeTime continuously while in ROI
                else:
                    if gazeInROI:           # gaze just left ROI
                        gazeTime += roiClock.getTime()  # finalize accumulated time
                        gazeInROI = False
            
            # ---------- SAVE RAW GAZE SAMPLE ----------
            
            sampleIndex += 1
            thisExp.addData('gaze_sample_index', sampleIndex)
            thisExp.addData('gaze_time', currentTime)
            
            # Make a safe copy of latest_gaze to prevent thread issues
            current_sample = latest_gaze.copy() if latest_gaze else None
            
            # Save all raw gaze fields from latest_gaze
            if current_sample is not None:
                keys = list(current_sample.keys())
                for k in keys:
                    thisExp.addData(k, current_sample[k])
            else:
                thisExp.addData('no_gaze_data', 1)
            
            # Save processed values safely
            thisExp.addData('gaze_x', gazeX if 'gazeX' in locals() else None)
            thisExp.addData('gaze_y', gazeY if 'gazeY' in locals() else None)
            thisExp.addData('gaze_in_roi', inROI if 'inROI' in locals() else 0)
            thisExp.addData('gaze_time_in_roi', gazeTime if 'gazeTime' in locals() else 0)
            
            thisExp.nextEntry()  # VERY IMPORTANT
            
            # ---------- END CONDITIONS ----------
            
            if gazeTime >= minTime:
                continueRoutine = False
            
            if currentTime >= maxTime:
                continueRoutine = False
            
            if 'escape' in event.getKeys():
                core.quit()
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=Familiarization,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Familiarization.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Familiarization.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Familiarization.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Familiarization" ---
        for thisComponent in Familiarization.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Familiarization
        Familiarization.tStop = globalClock.getTime(format='float')
        Familiarization.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Familiarization.stopped', Familiarization.tStop)
        # Run 'End Routine' code from code_familiarization
        fam_sound.stop()
        
        # the Routine "Familiarization" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        testLoop = data.TrialHandler2(
            name='testLoop',
            nReps=2.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(testLoop)  # add the loop to the experiment
        thisTestLoop = testLoop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTestLoop.rgb)
        if thisTestLoop != None:
            for paramName in thisTestLoop:
                globals()[paramName] = thisTestLoop[paramName]
        
        for thisTestLoop in testLoop:
            testLoop.status = STARTED
            if hasattr(thisTestLoop, 'status'):
                thisTestLoop.status = STARTED
            currentLoop = testLoop
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisTestLoop.rgb)
            if thisTestLoop != None:
                for paramName in thisTestLoop:
                    globals()[paramName] = thisTestLoop[paramName]
            
            # --- Prepare to start Routine "Central_Fixation" ---
            # create an object to store info about Routine Central_Fixation
            Central_Fixation = data.Routine(
                name='Central_Fixation',
                components=[central_fixation],
            )
            Central_Fixation.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            central_fixation.setMovie('materials/attention_video_grey.mp4')
            # Run 'Begin Routine' code from code_check_fixation
            trialClock = core.Clock()
            roiClock = core.Clock()
            videoStarted = False
            videoStartTime = None
            gazeTime = 0
            gazeInROI = False
            continueRoutine = True
            sampleIndex = 0
            # Get video stim
            central_fixation.setAutoDraw(False)
            central_fixation.stop()
            central_fixation.seek(0)
            
            # draw 1st frame and clear (attempt to solve black flash screen)
            baby_video.draw()
            win.clearBuffer()
            
            # play sound
            attention_sound = sound.Sound(r'materials\\attention_sound.wav')
            attention_sound.setVolume(1.0)
            soundPlayed = False
            # Get aspect ratio
            aspect = win.size[0] / win.size[1]
            
            # Define ROI
            x0 = -aspect / 2
            x1 =  aspect / 2
            y0 = -0.5
            y1 =  0.5
            
            print('Attention check started')
            
            # store start times for Central_Fixation
            Central_Fixation.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Central_Fixation.tStart = globalClock.getTime(format='float')
            Central_Fixation.status = STARTED
            thisExp.addData('Central_Fixation.started', Central_Fixation.tStart)
            Central_Fixation.maxDuration = None
            # keep track of which components have finished
            Central_FixationComponents = Central_Fixation.components
            for thisComponent in Central_Fixation.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Central_Fixation" ---
            thisExp.currentRoutine = Central_Fixation
            Central_Fixation.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTestLoop, 'status') and thisTestLoop.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *central_fixation* updates
                
                # if central_fixation is stopping this frame...
                if central_fixation.status == STARTED:
                    if bool(False) or central_fixation.isFinished:
                        # keep track of stop time/frame for later
                        central_fixation.tStop = t  # not accounting for scr refresh
                        central_fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        central_fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'central_fixation.stopped')
                        # update status
                        central_fixation.status = FINISHED
                        central_fixation.setAutoDraw(False)
                # Run 'Each Frame' code from code_check_fixation
                # Get current time
                currentTime = trialClock.getTime()
                
                # Get current gaze
                gazePos = get_current_gaze()  # returns (x, y) in 'height' units
                
                if gazePos is not None:
                    gazeX, gazeY = gazePos
                    # Check if gaze is anywhere on the screen ROI
                    if x0 <= gazeX <= x1 and y0 <= gazeY <= y1:
                        if not videoStarted:
                            # Start the movie immediately
                            central_fixation.setAutoDraw(True)
                            central_fixation.play()
                            videoStarted = True
                            videoStartTime = t 
                            if not soundPlayed:
                                attention_sound.play()
                                soundPlayed = True
                            
                else:
                    gazeX, gazeY = None, None
                
                # ---------- SAVE RAW GAZE SAMPLE ----------
                
                sampleIndex += 1
                thisExp.addData('gaze_sample_index', sampleIndex)
                thisExp.addData('gaze_time', currentTime)
                
                # Make a safe copy of latest_gaze to prevent thread issues
                current_sample = latest_gaze.copy() if latest_gaze else None
                
                # Save all raw gaze fields from latest_gaze
                if current_sample is not None:
                    keys = list(current_sample.keys())
                    for k in keys:
                        thisExp.addData(k, current_sample[k])
                else:
                    thisExp.addData('no_gaze_data', 1)
                
                # End routine after 3 seconds
                if videoStarted and videoStartTime is not None:
                    if t - videoStartTime >= 3.0:  # 3 seconds after video started
                        continueRoutine = False
                
                # Optional: allow escape key to quit experiment
                if 'escape' in event.getKeys():
                    core.quit()
                
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Central_Fixation,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Central_Fixation.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Central_Fixation.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Central_Fixation.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Central_Fixation" ---
            for thisComponent in Central_Fixation.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Central_Fixation
            Central_Fixation.tStop = globalClock.getTime(format='float')
            Central_Fixation.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Central_Fixation.stopped', Central_Fixation.tStop)
            central_fixation.setAutoDraw(False)
            central_fixation.stop()  # ensure movie has stopped at end of Routine
            # Run 'End Routine' code from code_check_fixation
            central_fixation.stop()
            attention_sound.stop()
            # not sure this is needed
            # baby_video.seek(0)
            # baby_video.setAutoDraw(False)
            # the Routine "Central_Fixation" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "Test_Period" ---
            # create an object to store info about Routine Test_Period
            Test_Period = data.Routine(
                name='Test_Period',
                components=[ROI_right, ROI_left, imgLeft, imgRight],
            )
            Test_Period.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_test
            # set up test imaga rotation
            if testLoop.thisN == 0:
                imgLeft.image = left_image_path_1
                imgRight.image = right_image_path_1
            else:
                imgLeft.image = right_image_path_1
                imgRight.image = left_image_path_1
            
            # Timer for this trial
            trialClock = core.Clock()  # overall max display tim2e
            roiClockLeft = core.Clock()    # timer for fixation in ROI
            roiClockRight = core.Clock()
            
            # Gaze tracking
            sampleIndex = 0
            
            gazeTimeLeft = 0 
            inROILeft = 0
            gazeInROILeft = False
            
            gazeTimeRight = 0
            inROIRight = 0
            gazeInROIRight = False
            
            # Define ROI Left
            x0, y0 = ROI_left.pos[0] - ROI_left.size[0]/2, ROI_left.pos[1] - ROI_left.size[1]/2
            x1, y1 = ROI_left.pos[0] + ROI_left.size[0]/2, ROI_left.pos[1] + ROI_left.size[1]/2
            
            # Define ROI Right
            x2, y2 = ROI_right.pos[0] - ROI_right.size[0]/2, ROI_right.pos[1] - ROI_right.size[1]/2
            x3, y3 = ROI_right.pos[0] + ROI_right.size[0]/2, ROI_right.pos[1] + ROI_right.size[1]/2
            
            maxTime = 5
            
            print('Test started')
            # store start times for Test_Period
            Test_Period.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Test_Period.tStart = globalClock.getTime(format='float')
            Test_Period.status = STARTED
            thisExp.addData('Test_Period.started', Test_Period.tStart)
            Test_Period.maxDuration = None
            # keep track of which components have finished
            Test_PeriodComponents = Test_Period.components
            for thisComponent in Test_Period.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Test_Period" ---
            thisExp.currentRoutine = Test_Period
            Test_Period.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTestLoop, 'status') and thisTestLoop.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *ROI_right* updates
                
                # if ROI_right is starting this frame...
                if ROI_right.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    ROI_right.frameNStart = frameN  # exact frame index
                    ROI_right.tStart = t  # local t and not account for scr refresh
                    ROI_right.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ROI_right, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'ROI_right.started')
                    # update status
                    ROI_right.status = STARTED
                    ROI_right.setAutoDraw(True)
                
                # if ROI_right is active this frame...
                if ROI_right.status == STARTED:
                    # update params
                    pass
                
                # *ROI_left* updates
                
                # if ROI_left is starting this frame...
                if ROI_left.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    ROI_left.frameNStart = frameN  # exact frame index
                    ROI_left.tStart = t  # local t and not account for scr refresh
                    ROI_left.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ROI_left, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'ROI_left.started')
                    # update status
                    ROI_left.status = STARTED
                    ROI_left.setAutoDraw(True)
                
                # if ROI_left is active this frame...
                if ROI_left.status == STARTED:
                    # update params
                    pass
                
                # *imgLeft* updates
                
                # if imgLeft is starting this frame...
                if imgLeft.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    imgLeft.frameNStart = frameN  # exact frame index
                    imgLeft.tStart = t  # local t and not account for scr refresh
                    imgLeft.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(imgLeft, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'imgLeft.started')
                    # update status
                    imgLeft.status = STARTED
                    imgLeft.setAutoDraw(True)
                
                # if imgLeft is active this frame...
                if imgLeft.status == STARTED:
                    # update params
                    pass
                
                # *imgRight* updates
                
                # if imgRight is starting this frame...
                if imgRight.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    imgRight.frameNStart = frameN  # exact frame index
                    imgRight.tStart = t  # local t and not account for scr refresh
                    imgRight.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(imgRight, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'imgRight.started')
                    # update status
                    imgRight.status = STARTED
                    imgRight.setAutoDraw(True)
                
                # if imgRight is active this frame...
                if imgRight.status == STARTED:
                    # update params
                    pass
                # Run 'Each Frame' code from code_test
                # Current time
                currentTime = trialClock.getTime()
                # Get current gaze position
                gazePos = get_current_gaze()  # (x, y) or None
                
                if gazePos is not None:
                    gazeX, gazeY = gazePos
                
                    # Left ROI
                    if x0 <= gazeX <= x1 and y0 <= gazeY <= y1:
                        inROILeft = 1
                        if not gazeInROILeft:
                            roiClockLeft.reset()
                            gazeInROILeft = True
                        gazeTimeLeft = roiClockLeft.getTime()
                    else:
                        inROILeft = 0
                        if gazeInROILeft:
                            gazeTimeLeft += roiClockLeft.getTime()
                            gazeInROILeft = False
                
                    # Right ROI
                    if x2 <= gazeX <= x3 and y2 <= gazeY <= y3:
                        inROIRight = 1
                        if not gazeInROIRight:
                            roiClockRight.reset()
                            gazeInROIRight = True
                        gazeTimeRight = roiClockRight.getTime()
                    else:
                        inROIRight = 0
                        if gazeInROIRight:
                            gazeTimeRight += roiClockRight.getTime()
                            gazeInROIRight = False
                
                # ---------- SAVE RAW GAZE SAMPLE ----------
                
                sampleIndex += 1
                thisExp.addData('gaze_sample_index', sampleIndex)
                thisExp.addData('gaze_time', currentTime)
                
                # Make a safe copy of latest_gaze to prevent thread issues
                current_sample = latest_gaze.copy() if latest_gaze else None
                
                # Save all raw gaze fields from latest_gaze
                if current_sample is not None:
                    keys = list(current_sample.keys())
                    for k in keys:
                        thisExp.addData(k, current_sample[k])
                else:
                    thisExp.addData('no_gaze_data', 1)
                
                # Save processed values safely
                thisExp.addData('gaze_x', gazeX if 'gazeX' in locals() else None)
                thisExp.addData('gaze_y', gazeY if 'gazeY' in locals() else None)
                thisExp.addData('gaze_in_roi_right', inROIRight if 'inROIright' in locals() else 0)
                thisExp.addData('gaze_time_in_roi_right', gazeTimeRight if 'gazeTimeRight' in locals() else 0)
                thisExp.addData('gaze_in_roi_left', inROILeft if 'inROIleft' in locals() else 0)
                thisExp.addData('gaze_time_in_roi_left', gazeTimeLeft if 'gazeTimeLeft' in locals() else 0)
                
                thisExp.nextEntry()  # VERY IMPORTANT
                
                if currentTime >= maxTime:
                    continueRoutine = False
                
                # Optional: exit experiment
                if 'escape' in event.getKeys():
                    core.quit()
                
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Test_Period,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Test_Period.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Test_Period.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Test_Period.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Test_Period" ---
            for thisComponent in Test_Period.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Test_Period
            Test_Period.tStop = globalClock.getTime(format='float')
            Test_Period.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Test_Period.stopped', Test_Period.tStop)
            # the Routine "Test_Period" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisTestLoop as finished
            if hasattr(thisTestLoop, 'status'):
                thisTestLoop.status = FINISHED
            # if awaiting a pause, pause now
            if testLoop.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                testLoop.status = STARTED
        # completed 2.0 repeats of 'testLoop'
        testLoop.status = FINISHED
        
        # mark thisTrialLoop as finished
        if hasattr(thisTrialLoop, 'status'):
            thisTrialLoop.status = FINISHED
        # if awaiting a pause, pause now
        if trialLoop.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            trialLoop.status = STARTED
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trialLoop'
    trialLoop.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Stop_ET" ---
    # create an object to store info about Routine Stop_ET
    Stop_ET = data.Routine(
        name='Stop_ET',
        components=[image],
    )
    Stop_ET.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for Stop_ET
    Stop_ET.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Stop_ET.tStart = globalClock.getTime(format='float')
    Stop_ET.status = STARTED
    thisExp.addData('Stop_ET.started', Stop_ET.tStart)
    Stop_ET.maxDuration = None
    # keep track of which components have finished
    Stop_ETComponents = Stop_ET.components
    for thisComponent in Stop_ET.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Stop_ET" ---
    thisExp.currentRoutine = Stop_ET
    Stop_ET.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *image* updates
        
        # if image is starting this frame...
        if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            image.frameNStart = frameN  # exact frame index
            image.tStart = t  # local t and not account for scr refresh
            image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'image.started')
            # update status
            image.status = STARTED
            image.setAutoDraw(True)
        
        # if image is active this frame...
        if image.status == STARTED:
            # update params
            pass
        
        # if image is stopping this frame...
        if image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > image.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                image.tStop = t  # not accounting for scr refresh
                image.tStopRefresh = tThisFlipGlobal  # on global time
                image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.stopped')
                # update status
                image.status = FINISHED
                image.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Stop_ET,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Stop_ET.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Stop_ET.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Stop_ET.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Stop_ET" ---
    for thisComponent in Stop_ET.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Stop_ET
    Stop_ET.tStop = globalClock.getTime(format='float')
    Stop_ET.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Stop_ET.stopped', Stop_ET.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if Stop_ET.maxDurationReached:
        routineTimer.addTime(-Stop_ET.maxDuration)
    elif Stop_ET.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    # Run 'End Experiment' code from Tobii_SDK_disconnect
    # Stop eye tracker recording
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_callback)
    print('ET stopped')
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
