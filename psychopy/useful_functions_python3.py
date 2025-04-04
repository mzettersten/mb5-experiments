import os
import glob
import math
import random
from psychopy import core, visual, prefs, event, gui,misc, data
from psychopy import sound
import socket
import datetime
try:
	import pygame
except ImportError:
	pass


def createDirectories(directories):
	if not isinstance(directories,list):
		directories=[directories]		
	for cur_directory in directories:
		if not os.path.exists(cur_directory):
			try:
				os.makedirs(cur_directory)
			except:
				print("could not create", cur_directory)

 
def importTrials(trialsFilename, colNames=None, separator='\t'):
	try:
		trialsFile = open(trialsFilename, 'rb')
	except IOError:
		print(trialsFilename, 'is not a valid file')
	
	if colNames is None: # Assume the first row contains the column names
		colNames = trialsFile.next().rstrip().split(separator)
	trialsList = []
	for trialStr in trialsFile:
		trialList = trialStr.rstrip().split(separator)
		assert len(trialList) == len(colNames)
		trialDict = dict(list(zip(colNames, trialList)))
		trialsList.append(trialDict)
	return trialsList


def importTrialsWithHeader(trialsFilename, colNames=None, separator='\t', header=True,check_lengths=True):
	try:
		trialsFile = open(trialsFilename, 'r')
	except IOError:
		print(trialsFilename, 'is not a valid file')
	
	if colNames is None: # Assume the first row contains the column names
		colNames = trialsFile.readline().rstrip().split(separator)
	trialsList = []
	for trialStr in trialsFile:
		trialList = trialStr.rstrip().split(separator)
		if check_lengths:
			assert len(trialList) == len(colNames)
		trialDict = dict(list(zip(colNames, trialList)))
		trialsList.append(trialDict)
	if header:
		return (colNames, trialsList)
	else:
		return trialList

def oldImportTrials(fileName,method="sequential",seed=random.randint(1,100)):
	""" From baseDefsPsychopy. Used in some older scripts such as sameDiff"""
	(stimList,fieldNames) = data.importConditions(fileName,returnFieldNames=True)
	trials = data.TrialHandler(stimList,1,method=method,seed=seed) #seed is ignored for sequential; used for 'random'
	return (trials,fieldNames)


def createRespNew(allSubjVariables,subjVariables,fieldVarNames,fieldVars,**respVars):
	"""Creates  a key and value list of all the variables passed in from various sources (runtime, trial params, dep. vars."""
	"""Old function.. only in use in old scripts like sameDiff."""
	
	def stripUnderscores(keyList):
		return [curKey.split('_')[1] for curKey in keyList]
			
	trial = [] #initalize array
	header=[]
	for curSubjVar, varInfo in sorted(allSubjVariables.items()):
		header.append(allSubjVariables[curSubjVar]['name'])
		trial.append(subjVariables[varInfo['name']])
	for curFieldVar in fieldVars:
		trial.append(curFieldVar)
	for curRespVar in sortDictValues(respVars):
		trial.append(str(curRespVar))
	header.extend(fieldVarNames)
	header.extend(stripUnderscores(sortDictValues(respVars,'keys')))
	return [header,trial]

def printHeader(header,headerFile='header.txt',separator="\t", overwrite=False):
	if overwrite or (not overwrite and not os.path.isfile(headerFile)):
		headerFile = open(headerFile,'w')
		writeToFile(headerFile,header,writeNewLine=True,separator=separator)
		return True
	else:
		return False		

def evaluateLists(trialList):
	assert isinstance(trialList,list)
	for curTrial in trialList:
		assert isinstance(curTrial,dict)
		for key,value in list(curTrial.items()):
			try:
				if isinstance(eval(curTrial[key]),list) or isinstance(eval(curTrial[key]),dict) or isinstance(eval(curTrial[key]),tuple):
					curTrial[key]=eval(value)
			except:
				pass
	return trialList


def circularList(lst,seed):
	if not isinstance(lst,list):
		lst = list(range(lst))
	i = 0
	random.seed(seed)
	random.shuffle(lst)
	while True:
		yield lst[i]
		if (i+1) % len(lst) ==0:
			random.shuffle(lst)
		i = (i + 1)%len(lst)


def setAndPresentStimulus(win,stimuli,duration=0):
	"""Stimuli can be a list or a single draw-able stimulus"""
	if isinstance(stimuli,list):
		for curStim in stimuli:
			curStim.draw()
	else:
		stimuli.draw()
	if duration==0: #single frame
		win.flip()
	else: 
		win.flip()
		core.wait(duration)
	return


def showText(win,textToShow,color="black",waitForKey=True,acceptOnly=0,inputDevice="keyboard",mouse=False,pos=[0,0],scale=1,font="NA"):
	global event
	event.clearEvents()
	win.flip()
	if win.units == "pix":
		height = 30*scale
		wrapWidth=int(win.size[0]*.8)
	elif win.units == "deg":
		height=.7*scale
		wrapWidth=30
	else:
		wrapWidth=None
	if font!= "NA":
		textStim = visual.TextStim(win, pos=pos,wrapWidth=wrapWidth,color=color,height=height,text=textToShow,font=font)
	else:
		textStim = visual.TextStim(win, pos=pos,wrapWidth=wrapWidth,color=color,height=height,text=textToShow)	
	textStim.draw()
	win.flip()
	if mouse:
		while any(mouse.getPressed()):
			core.wait(.1) #waits for the user to release the mouse
		while not any(mouse.getPressed()):
			pass
		return
	elif inputDevice=="keyboard":
		if waitForKey:
			if acceptOnly==0:
				event.waitKeys()
			else:
				print('waiting for ', acceptOnly)
				event.waitKeys(keyList=[acceptOnly])
			return
		else:
			return
	elif inputDevice=="gamepad": #also uses mouse if mouse is not false
		while True:
			for event in pygame.event.get(): #check responses
				if mouse:
					if event.type==pygame.MOUSEBUTTONDOWN:
						pygame.event.clear() 
						return
				if event.type==pygame.KEYDOWN or event.type==pygame.JOYBUTTONDOWN:
					pygame.event.clear() 
					return


def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(400,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()
	
def getSubjCode(preFilledInText=''):
	 userVar = {'subjCode':preFilledInText}
	 dlg = gui.DlgFromDict(userVar)
	 return userVar['subjCode']

def getRunTimeVars(varsToGet,order,expName):
	"""Get run time variables, see http://www.psychopy.org/api/gui.html for explanation"""
	order.append('expName')
	varsToGet['expName']= expName
	try:
		previousRunTime = misc.fromFile(expName+'_lastParams.psydat')
		for curVar in list(previousRunTime.keys()):
			if isinstance(varsToGet[curVar],list) or curVar=="room" or curVar=="date_time":
				pass #don't load it in
			else:
				varsToGet[curVar] = previousRunTime[curVar]
	except:
		pass

	if 'room' in varsToGet and 'date_time' in varsToGet:
		infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=['room','date_time'],order=order)
	else:
		infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=[expName],order=order)	

	misc.toFile(expName+'_lastParams.psydat', varsToGet)
	if infoDlg.OK:
		return varsToGet
	else: print('User Cancelled')

def openOutputFile(subjCode,suffix):
	if  os.path.isfile(subjCode+'_'+suffix+'.txt'):
		popupError('Error: That subject code already exists')
		return False
	else:
		try:
			outputFile = open(subjCode+'_'+suffix+'.txt','w')
		except:
			print('could not open file for writing')
		return outputFile

def	calculateRectangularCoordinates(distanceX, distanceY, numCols, numRows,yOffset=0,xOffset=0):
	coords = [[0,0]]*numCols*numRows
	curObj=0
	for curCol in range(0,numCols): #x-coord
		for curRow in range(0,numRows): #y-coord
			coords[curObj]= (curCol*distanceX, curRow*distanceY)
			curObj=curObj+1
	xCorrected = max([coord[0] for coord in coords])/2 -xOffset
	yCorrected = max([coord[1] for coord in coords])/2 -yOffset

	return [(coord[0]-xCorrected, coord[1]-yCorrected) for coord in coords]


def getKeyboardResponse(validResponses,duration=0):
	event.clearEvents()
	responded = False
	done = False
	rt = '*'
	responseTimer = core.Clock()
	while True: 
		if not responded:
			responded = event.getKeys(keyList=validResponses, timeStamped=responseTimer) 
		if duration>0:
			if responseTimer.getTime() > duration:
				break
		else: #end on response
			if responded:
				break
	if not responded:
		return ['*','*']
	else:
		return responded[0] #only get the first resp



def initGamepad():
	pygame.joystick.init() # init main joystick device system
	try:
		stick = pygame.joystick.Joystick(0)
		stick.init() # init instance
		return stick
	except pygame.error:
		raise SystemExit("---->No joystick/gamepad found. Make sure one is plugged in<--")
	
		
		
#TO DO: move stick to the last parameter so it's treated as optional - that way we can have a generic response function that either takes or doesn't take a joystick parameter as provided.
def getGamepadResponse(stick,validResponses,duration=0):
	"""joystick needs to be initialized first (with initGamepad or manually). Only returns the first response. """
	def getJoystickResponses(): #returns buttons. If none are pressed, checks the hat.
		for n in range(stick.get_numbuttons()):
			if stick.get_button(n) : # if this is down
				return n
		for n in range(stick.get_numhats()):
			return stick.get_hat(n)

	responded = False
	timeElapsed = False
	responseTimer = core.Clock()
	response=rt='*'
	pygame.event.clear() #clear event cue
	responseTimer.reset()
	while not responded and not timeElapsed:
		for event in pygame.event.get(): # iterate over event stack
			if event.type==pygame.JOYBUTTONDOWN or event.type==pygame.JOYHATMOTION:
				response = getJoystickResponses()
				if response in validResponses:
					rt =  responseTimer.getTime()
					responded = True
					break
		if duration>0 and responseTimer.getTime() > duration:
			timeElapsed=True
	if not responded:
		return ['*','*']
	else:
		return (response,rt)



def getMouseResponse(mouse,duration=0):
	event.clearEvents()
	responseTimer = core.Clock()
	numButtons=len(event.mouseButtons)
	response = [0]*numButtons
	timeElapsed = False
	mouse.clickReset()
	responseTimer.reset()
	rt = '*'
	while not any(response) and not timeElapsed:
		(response,rt) = mouse.getPressed(getTime=True)
		if duration>0 and responseTimer.getTime() > duration:
			timeElapsed=True
	
	if not any(response): #if there was no response (would only happen if duration is set)
		return ('*','*')
	else:
		nonZeroResponses = [x for x in rt if x>0]
		firstResponseButtonIndex = rt.index(min(nonZeroResponses)) #only care about the first (earliest) click
		return (firstResponseButtonIndex,rt[firstResponseButtonIndex])


def writeToFile(fileHandle,trial,separator='\t', sync=True,writeNewLine=False):
	"""Writes a trial (array of lists) to a previously opened file"""
	line = separator.join([str(i) for i in trial]) #TABify
	if writeNewLine:
		line += '\n' #add a newline
	try:
		fileHandle.write(line)
	except:
		print('file is not open for writing')
	if sync:
			fileHandle.flush()
			os.fsync(fileHandle)
			
def polarToRect(angleList,radius):
	"""Accepts a list of angles and a radius.  Outputs the x,y positions for the angles"""
	coords=[]
	for curAngle in angleList:
		radAngle = (float(curAngle)*2.0*math.pi)/360.0
		xCoord = round(float(radius)*math.cos(radAngle),0)
		yCoord = round(float(radius)*math.sin(radAngle),0)
		coords.append([xCoord,yCoord])
	return coords
					
def euclidDistance(pointA,pointB):
	return math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)



def loadFiles(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
	""" Load all the pics and sounds. Uses pyo or pygame for the sound library (see prefs.general['audioLib'])"""
	path = os.getcwd() #set path to current directory
	if isinstance(extension,list):
		fileList = []
		for curExtension in extension:
			fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
	else:
		fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
	fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by file names (picture names, sound names)
	for num,curFile in enumerate(fileList):
		fullPath = curFile
		fullFileName = os.path.basename(fullPath)
		stimFile = os.path.splitext(fullFileName)[0]
		if fileType=="image":
			try:
				surface = pygame.image.load(fullPath) #gets height/width of the image
				stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
				(width,height) = (surface.get_width(),surface.get_height())
			except: #no pygame, so don't store the image dimensions
				pass
			stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
			(width,height) = (stim.size[0],stim.size[1])
			fileMatrix[stimFile] = {'stim':stim,'fullPath':fullFileName,'filename':stimFile,'num':num,'width':width, 'height':height}
		elif fileType=="sound":
			fileMatrix[stimFile] = {'stim':sound.Sound(fullPath), 'duration':sound.Sound(fullPath).getDuration()}
 
	#optionally check a list of desired stimuli against those that've been loaded
	if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
		popupError(str(set(stimList).difference(list(fileMatrix.keys()))) + " does not exist in " + path+'\\'+directory) 
	return fileMatrix
	
	
	





			
			
			