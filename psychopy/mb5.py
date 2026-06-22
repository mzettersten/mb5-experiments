from psychopy import prefs
prefs.general['measureFrameRate'] = False
prefs.hardware['disableVideoSyncTest'] = True
from psychopy import core, visual, event
import random
import sys
import copy
import socket
import webbrowser as web
from useful_functions_python3 import getKeyboardResponse, showText, setAndPresentStimulus, createDirectories, openOutputFile, printHeader, importTrialsWithHeader, calculateRectangularCoordinates, loadFiles, popupError, getRunTimeVars, evaluateLists, writeToFile
# from generateTrials import *
from psychopy.hardware import keyboard


from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

expName='mb5'

class Exp:

	def __init__(self):

		while True:
			runTimeVarOrder = ['subjCode','trial_list','method','num_screens','tv_screen','exp_screen','side_screen','image_size','keyboard']
			runTimeVars = getRunTimeVars({'subjCode':'', 'trial_list': 1, 'method':["contingent","fixed"],'keyboard': ["default","event"],'num_screens': 3,'tv_screen': 2,'exp_screen': 0,'side_screen': 1,'image_size': 0.65,'fam_audio': ["audio","no audio"]},runTimeVarOrder,expName)
			if runTimeVars['subjCode']=='':
				popupError('Subject code is blank')
			elif 'Choose' in list(runTimeVars.values()):
				popupError('Need to choose a value from a dropdown box')
			else:
				try:
					createDirectories(['data','trials'])
					self.outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_familiarization')
					self.testOutputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_test')
					if self.outputFile and self.testOutputFile: #files were opened for writing
						break
				except:
					popupError('Output file(s) could not be opened for writing')

		# generateTrials(runTimeVars, runTimeVarOrder)
		# (self.header,self.trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_trials.csv', separator=',')
		(self.header,self.trialInfo) = importTrialsWithHeader('trials/mb5_trial_list_'+str(runTimeVars['trial_list'])+'.csv', separator=',')
		self.trialInfo = evaluateLists(self.trialInfo) #needed because the choices field is a list

		self.complete_header = runTimeVarOrder + self.header
		self.win = visual.Window(fullscr=True,allowGUI=True, color="#808080", units='height',screen=int(runTimeVars['tv_screen']))
		screenWidth = self.win.size[0]
		screenHeight = self.win.size[1]
		print(screenWidth)
		print(screenHeight)
		#create psychopy window for experimenter
		self.win2 = visual.Window([800,800], color="black", allowGUI=True,units='pix',screen=int(runTimeVars['exp_screen']))
		self.win2.flip()
		self.num_screens = int(runTimeVars['num_screens'])
		if self.num_screens == 3:
			#creating third screen
			#create psychopy window for tracking trials
			self.win3 = visual.Window(fullscr=True, color="black", allowGUI=True,units='pix',screen=int(runTimeVars['side_screen']))
			self.win3.flip()

		#visual.TextStim(win=self.win,text="Loading stimuli...").draw()
		#self.win.flip()
		self.pics =  loadFiles('stimuli/images','.png','image', win=self.win)
		self.sounds = loadFiles('stimuli/audio','.wav','sound', win=self.win)
		self.cf_movie_path = "stimuli/movies/ag_no_audio_grey.mp4"
		self.cf = visual.MovieStim(win=self.win,filename = self.cf_movie_path,units = "height",size=(None,0.4),loop=True,color="#808080")
		self.cf_still=visual.ImageStim(self.win, 'stimuli/images/ag_no_audio_grey.png',units = "height",size=(0.7111112,0.4),mask=None,interpolate=True)
		self.cf_still.setPos((0,0))
		self.cf_duration = .75
		self.cf_max_duration = 5
		self.ag_movie_path = "stimuli/movies/laughing_baby_no_audio_grey.mp4"
		self.ag = visual.MovieStim(win=self.win,filename = self.ag_movie_path,units = "height",size=(None,0.75),loop=True)
		self.ag_still=visual.ImageStim(self.win, 'stimuli/images/laughing_baby_no_audio_grey.png',units = "height",size=(1.333334,0.75),mask=None,interpolate=True)
		self.ag_still.setPos((0,0))
		self.ag_movie_border = visual.Rect(win=self.win,units="height",size=(1.333334,0.75),pos=(0.0,0.0),lineWidth=10, lineColor = "#808080",fillColor=None)
		self.ag_duration = 2
		self.ag_max_duration = 10
		#self.sounds =  loadFiles('stimuli/sounds','.wav','sound', win=self.win)

		self.preFixationDelay = .75
		self.postFixationDelay = 0

		self.position = {'left': (-0.5,0), 'right': (0.5,0), 'center':(0,0)}
		self.size = float(runTimeVars['image_size'])
		self.inputDevice = "keyboard"
		self.validResponses = {'z':'left','slash':'right'} #change to whatever keys you want to use
		self.validKeys = ['space','escape']
		self.method = runTimeVars['method']
		self.fam_audio=runTimeVars['fam_audio']
		self.keyboard = runTimeVars['keyboard']
		if self.keyboard == "default":
			self.kb = keyboard.Keyboard()
		else:
			self.kb = None

		self.runtime_vars_list = [runTimeVars[runtime_var_name] for runtime_var_name in runTimeVarOrder]
		
		self.instructions_text = "Welcome to the ManyBabies 5 demo!\n\nWhen you see the laughing baby, hit space to advance to the next trial.\n\nDuring familiarization, for contingent trials, press the right arrow key when the infant is looking to the screen and the left arrow key when they look away. Otherwise, for fixed durations, the experiment will proceed at the end of the familiarization time.\n\nAfter the familiarization, a central fixation will appear. Hit the space bar to advance (once the infant is looking). The second central fixation in between the two test trial phases advances automatically.\n\nHit q to start the experiment! Press esc at any time to quit."
		
	def check_for_quit(self):
		# Allows the experimenter to quit cleanly with esc from any active loop.
		if 'escape' in event.getKeys(keyList=['escape']):
			#close windows
			self.win.close()
			self.win2.close()
			if self.num_screens == 3:
				self.win3.close()
			#explicitly close files
			self.outputFile.close()
			self.testOutputFile.close()
			core.quit()
		if self.kb is not None:
			if self.kb.getKeys(keyList=['escape'], clear=True):
				#close windows
				self.win.close()
				self.win2.close()
				if self.num_screens == 3:
					self.win3.close()
				#explicitly close files
				self.outputFile.close()
				self.testOutputFile.close()
				core.quit()

	def quit_experiment(self):
		#close windows
		self.win.close()
		self.win2.close()
		if self.num_screens == 3:
			self.win3.close()
		#explicitly close files
		self.outputFile.close()
		self.testOutputFile.close()
		core.quit()

	def wait_with_quit(self, duration):
		# Replacement for core.wait() when we want esc to remain active.
		wait_timer = core.Clock()
		wait_timer.reset()
		while wait_timer.getTime() < duration:
			self.check_for_quit()
			core.wait(.01)
		
	# may need to remove the /2 when running on the lab computer. Retina screen resolution issue..
	def create_placeholder(self,lineColor="black", fillColor="white",size=None,pos=(0,0)):
		if size is None:
			size = (self.size + 0.01, self.size + 0.01)
		return visual.Rect(win=self.win,size=size, pos=pos, lineColor=lineColor, fillColor=fillColor, lineWidth=3)

	def show_instructions(self,text):
		#self.win.flip()
		#visual.TextStim(win=self.win,text=text,color="white",height=40,pos=(0,0),wrapWidth=1000).draw()
		image=visual.ImageStim(self.win, 'stimuli/images/bunnies.png',size=(None,1),mask=None,interpolate=True)
		image.setPos((0,0))
		image.draw()
		self.win.flip()
		keys = event.waitKeys(keyList=['q','escape'])
		if keys and keys[0] == 'escape':
			#close windows
			self.win.close()
			self.win2.close()
			if self.num_screens == 3:
				self.win3.close()
			#explicitly close files
			self.outputFile.close()
			self.testOutputFile.close()
			core.quit()
	
	def show_ag(self,curTrial,gaze_contingent=False,video_still_dur=0.1):

		#preload phase
		#set first frame of video while video loads
		self.ag_still.draw()
		self.ag_movie_border.autoDraw = True
		self.win.flip()
		core.wait(video_still_dur)
		#load movie
		print(self.ag_movie_path)
		self.ag = visual.MovieStim(win=self.win,filename = self.ag_movie_path,units = "height",size=(1.333334,0.75),loop=True)
		
		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial List: " + str(self.runtime_vars_list[1]) +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: AG"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		if self.num_screens == 3:
			trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
			trialInfoStim_3.draw()
		ag_square_skeleton=visual.Rect(self.win2,lineColor="black",fillColor="yellow",size=[300,200])
		ag_square_skeleton.draw()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

		event.clearEvents()
		# present AG
		clock = core.Clock()  # Create a clock to track time
		clock.reset()
		# Play the movie
		self.ag.play()
		self.sounds['laughing_baby']['stim'].play()
		if not gaze_contingent:
			while clock.getTime() < self.ag_duration:  
				self.check_for_quit()
				#self.ag.play()
				self.ag.draw()
				self.win.flip()
		elif gaze_contingent:
			key_pressed = False
			timeout = False
			while (not key_pressed) and (not timeout):
				#self.ag.play()
				self.ag.draw()
				self.win.flip()
				keys = event.getKeys(keyList=self.validKeys)
				if 'escape' in keys:
					self.quit_experiment()
				if 'space' in keys:
					key_pressed = True

				if clock.getTime() >= self.ag_max_duration:
					timeout = True 
					print(clock.getTime())
		
		#stop the movie
		self.ag.stop()
		self.ag.seek(0)
		self.sounds['laughing_baby']['stim'].stop()
		self.ag_movie_border.autoDraw = False


		self.win.flip()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

	def show_cf(self,curTrial,gaze_contingent=False,video_still_dur = 0.1):
		
		#preload phase
		#set first frame of video while video loads
		self.cf_still.draw()
		self.win.flip()
		core.wait(video_still_dur)
		#load movie
		self.cf = visual.MovieStim(win=self.win,filename = self.cf_movie_path,units = "height",size=(0.7111112,0.4),loop=True)

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial List: " + str(self.runtime_vars_list[1]) +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		if gaze_contingent:
			trialInfo+="Phase: CF CONTINGENT"
			stim_color = "yellow"
		else:
			trialInfo+="Phase: CF"
			stim_color="white"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		if self.num_screens == 3:
			trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
			trialInfoStim_3.draw()
		cf_skeleton=visual.Circle(self.win2,lineColor="black",fillColor=stim_color,size=[150,150])
		cf_skeleton.draw()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

		event.clearEvents()
		# present central fixation stimulus
		clock = core.Clock()  # Create a clock to track time
		clock.reset()
		# Play the movie
		self.cf.play()
		self.sounds['ag']['stim'].play()
		if not gaze_contingent:
			#subtract any time waiting to load the video
			while clock.getTime() < (self.cf_duration-video_still_dur):  
				self.check_for_quit()
				self.cf.draw()
				self.win.flip()
		elif gaze_contingent:
			key_pressed = False
			timeout = False
			while (not key_pressed) and (not timeout):
				self.cf.draw()
				self.win.flip()
				keys = event.getKeys(keyList=self.validKeys)
				if 'escape' in keys:
					self.quit_experiment()
				if 'space' in keys:
					key_pressed = True
				if clock.getTime() >= self.cf_max_duration:
					timeout = True 
					print(clock.getTime())
		
		#stop the movie
		self.cf.stop()
		self.cf.seek(0)
		self.sounds['ag']['stim'].stop()
		event.clearEvents()

		self.win.flip()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()
	
	def show_test(self,curTrial,position_type=1):

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial List: " + str(self.runtime_vars_list[1]) +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: TEST"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		if self.num_screens == 3:
			trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
			trialInfoStim_3.draw()
		square_skeleton_1=visual.Rect(self.win2,lineColor="black",fillColor="blue",size=[150,150],pos=(-150,0))
		square_skeleton_2=visual.Rect(self.win2,lineColor="black",fillColor="blue",size=[150,150],pos=(150,0))
		square_skeleton_1.draw()
		square_skeleton_2.draw()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

		#show test trial
		#no longer showing square backgrounds - toggle to bring back white background
		#(pos=self.position['left'],size=self.size+0.01).draw()
		#self.create_placeholder(pos=self.position['right'],size=self.size+0.01).draw()

		#set positions
		if position_type == 1:
			familiar_location = curTrial["familiar_location_1"];
			novel_location = curTrial["familiar_location_2"];
			test_time = int(curTrial['test_time_1'])
		#invert
		else:
			familiar_location = curTrial["familiar_location_2"];
			novel_location = curTrial["familiar_location_1"];
			test_time = int(curTrial['test_time_2'])

		self.pics[curTrial['familiar_stimulus']]['stim'].pos = self.position[familiar_location]
		self.pics[curTrial['novel_stimulus']]['stim'].pos = self.position[novel_location]
		self.pics[curTrial['novel_stimulus']]['stim'].size = self.size
		self.pics[curTrial['familiar_stimulus']]['stim'].size = self.size
		self.pics[curTrial['familiar_stimulus']]['stim'].draw()
		self.pics[curTrial['novel_stimulus']]['stim'].draw()

		overall_test_timer = core.Clock()  # Timer to measure overall elapsed time
		# Start overall timer
		overall_test_timer.reset()

		self.win.flip()
		
        # present for test time
		self.wait_with_quit(test_time)

		self.win.flip()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()
		
		# Get overall elapsed time
		elapsed_test_time = overall_test_timer.getTime()
		
		#write data to output file
		curTrial['header']=self.header
		trial_responses=[curTrial[_] for _ in curTrial['header']]
		test_responses=self.runtime_vars_list+trial_responses
		#write dep variables
		test_responses.extend([
			position_type,
			elapsed_test_time])
		writeToFile(self.testOutputFile,test_responses,writeNewLine=True,separator=",")

	def show_familiarization(self,curTrial, gaze_contingent=False, play_audio=True):

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial List: " + str(self.runtime_vars_list[1]) +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: FAMILIAR"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		if self.num_screens == 3:
			trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
			trialInfoStim_3.draw()
		square_skeleton=visual.Rect(self.win2,lineColor="black",fillColor="red",size=[150,150],pos=(0,0))
		square_skeleton.draw()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

		#show familiarization
		#show size
		self.pics[curTrial['familiar_stimulus']]['stim'].size = self.size
		print(self.pics[curTrial['familiar_stimulus']]['stim'].size)
		#no longer showing square backgrounds - toggle to bring back white background
		#self.create_placeholder(pos=self.position['center'],size=self.size+0.01).draw()
		self.pics[curTrial['familiar_stimulus']]['stim'].pos = self.position['center']
		self.pics[curTrial['familiar_stimulus']]['stim'].draw()

		#play familiarization audio
		if play_audio:
			self.sounds['amelie_rediscovery_ag']['stim'].play()
		
		event.clearEvents()
		overall_timer = core.Clock()  # Timer to measure overall elapsed time
		# Start overall timer
		overall_timer.reset()
		total_held_time = 0  # Accumulated time the infant has been registered as looking to the stimulus
		looks = 0 # how many looks the infant has made to the screen
		keypress_list = [] #list of distinct keypresses
		look_list = [] # list of distinct onscreen looks (looking times)

		self.win.flip()

		print(int(curTrial['familiarization_time']))

		#no gaze contingency
		if not gaze_contingent:

			self.wait_with_quit(int(curTrial['familiarization_time']))
		
		#gaze contingency
		else:
			looking = False  # Track if infant is currently looking
			clock = core.Clock() #clock for tracking individual onscreen look durations
			
			cur_look_length = 0 #keeps track of the length of the current on screen look
			time_left = int(curTrial['familiarization_time'])
			count_down_timer = core.CountdownTimer(time_left) #begins familiarization time count down

			if self.keyboard == "default":
				# Press-and-hold contingent coding (based on key pressed down)
				# holding space = infant is looking; releasing space = infant looked away.
				self.kb.clearEvents()
				self.kb.clock.reset()

				#while loop that continues while:
				#(a) there's still familiarization time left or the infant is not looking
				#(b) and the familiarization max time/ timeout has not yet been reached
				while (count_down_timer.getTime() > 0 or not looking) and overall_timer.getTime()<int(curTrial['familiarization_time_timeout']):
					self.check_for_quit()
					space_down = self.kb.getState('space') #get the current state of the space bar
					print(space_down)

					#what to do if the infant previously wasn't looking and now is registered as looking
					if space_down and not looking:
						clock.reset()
						looking = True
						#update countdown to reflect current time left (and start counting down)
						count_down_timer = core.CountdownTimer(time_left)
						#add a new keypress to the keypress list
						keypress_list.append(('space_down', overall_timer.getTime())) # store timing of keypresses relative to overall time
						print(looking)
						print(time_left)
						looks += 1 #add a new look to the look counter

						#looking: visual feedback on experimenter monitor
						square_skeleton.color = "green"
						trialInfoStim.draw()
						square_skeleton.draw()
						self.win2.flip()
					
					#if the infant was previously looking but now is no longer registered as looking
					if not space_down and looking:
						cur_look_length = clock.getTime()
						clock.reset()
						looking = False
						#update timing parameters of the (now completed) looking period and reset time left (for when countdown timer restarts)
						total_held_time += cur_look_length
						time_left = time_left - cur_look_length #countdown timer to use when the next look begins
						keypress_list.append(('space_up', overall_timer.getTime())) # store timing of keypresses relative to overall time
						print(looking)
						print(time_left)

						#look away: visual feedback on experimenter monitor
						square_skeleton.color = "red"
						trialInfoStim.draw()
						square_skeleton.draw()
						self.win2.flip()

						#store last look
						look_list.append(cur_look_length)

			else:
				# right-left contingent looking coding (based on keypress only)
				# right = infant started looking; left = infant looked away

				#while loop that continues while:
				#(a) there's still familiarization time left or the infant is not looking
				#(b) and the familiarization max time/ timeout has not yet been reached
				while (count_down_timer.getTime() > 0 or not looking) and overall_timer.getTime()<int(curTrial['familiarization_time_timeout']):
					self.check_for_quit()
					responded = event.getKeys(keyList=['right','left'], timeStamped=overall_timer) #store key presses relative to the overall timer
					keypress_list.extend(responded)
					if responded:
						response = responded[0]
						print(response)
					
					#if the the right key is pressed (onscreen look registered) 
					# and the infant was previously NOT looking
					if responded and response[0]=="right" and not looking:
						clock.reset()
						looking = True
						#update countdown to reflect current time left
						count_down_timer = core.CountdownTimer(time_left)
						print(looking)
						print(time_left)
						looks += 1

						#looking: visual feedback on experimenter monitor
						square_skeleton.color = "green"
						trialInfoStim.draw()
						square_skeleton.draw()
						self.win2.flip()
					
					#if the infant was previously looking and now as registered as looking away (left arrow pushed)
					if responded and response[0]=="left" and looking:
						cur_look_length = clock.getTime()
						clock.reset()
						looking = False
						#update timing and reset time left
						total_held_time += cur_look_length
						time_left = time_left - cur_look_length
						print(looking)
						print(time_left)

						#look away: visual feedback on experimenter monitor
						square_skeleton.color = "red"
						trialInfoStim.draw()
						square_skeleton.draw()
						self.win2.flip()

						#store last look
						look_list.append(cur_look_length)
					
					#helps increase reliability of left/right recording a bit
					core.wait(0.001, hogCPUperiod=0)
			
			#clean up and add final look if the infant is still looking when the while loop ends
			if looking:
				#being extra careful here, to also resolve small discrepancies between clock time and time left
				cur_look = min(clock.getTime(), max(0,time_left))
				print(cur_look)
				look_list.append(cur_look)
				#total_held_time += time_left
				total_held_time += cur_look


		# stop audio if playing
		if play_audio:
			self.sounds['amelie_rediscovery_ag']['stim'].stop()

		# Clear screen
		self.win.flip()
		self.win2.flip()
		if self.num_screens == 3:
			self.win3.flip()

		# Get overall elapsed time
		elapsed_time = overall_timer.getTime()

		print(total_held_time)
		print(looks)
		print(elapsed_time)

		#write data to output file
		curTrial['header']=self.header
		trial_responses=[curTrial[_] for _ in curTrial['header']]
		responses=self.runtime_vars_list+trial_responses
		#write dep variables
		responses.extend([
			total_held_time,
			elapsed_time,
			looks,keypress_list,look_list])
		writeToFile(self.outputFile,responses,writeNewLine=True,separator=",")


if __name__ == '__main__':
	exp = Exp()

	#file headers
	train_header = exp.complete_header[:] #assign list by value since we're extending it below and don't want to change the orig header list
	train_header.extend(('total_accumulated_looking_time','elapsed_time','number_of_looks','keypress_list','look_duration_list'))
	printHeader(train_header,headerFile="familiarization_header.txt",separator=",")

	test_header = exp.complete_header[:] 
	test_header.extend(('position_type','elapsed_time'))
	printHeader(test_header,headerFile="test_header.txt",separator=",")

	if exp.method == "contingent":
		fam_contingent = True
	else:
		fam_contingent = False
	
	if exp.fam_audio == 'audio':
		play_fam_audio = True
	else:
		play_fam_audio = False

	exp.show_instructions(exp.instructions_text)
	for i,curTrial in enumerate(exp.trialInfo):
		exp.show_ag(curTrial,gaze_contingent=True)
		exp.show_familiarization(curTrial, gaze_contingent=fam_contingent,play_audio=play_fam_audio)
		exp.show_cf(curTrial,gaze_contingent=True)
		exp.show_test(curTrial,position_type=1)
		exp.show_cf(curTrial)
		exp.show_test(curTrial,position_type=2)
	
	#shut down experiment
	exp.quit_experiment()






