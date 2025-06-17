from psychopy import core, visual, prefs, event
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
			runTimeVarOrder = ['subjCode','trial_list','method','tv_screen','side_screen','exp_screen','image_size',]
			runTimeVars = getRunTimeVars({'subjCode':'mb5_', 'trial_list': 1, 'method':["fixed","contingent"],'tv_screen': 2,'side_screen': 1,'exp_screen': 0,'image_size': 512},runTimeVarOrder,expName)
			if runTimeVars['subjCode']=='':
				popupError('Subject code is blank')
			elif 'Choose' in list(runTimeVars.values()):
				popupError('Need to choose a value from a dropdown box')
			else:
				try:
					createDirectories(['data','trials'])
					self.outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_familiarization')
					if self.outputFile: #files were opened for writing
						break
				except:
					popupError('Output file(s) could not be opened for writing')

		# generateTrials(runTimeVars, runTimeVarOrder)
		# (self.header,self.trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_trials.csv', separator=',')
		(self.header,self.trialInfo) = importTrialsWithHeader('trials/mb5_trial_list_'+str(runTimeVars['trial_list'])+'.csv', separator=',')
		self.trialInfo = evaluateLists(self.trialInfo) #needed because the choices field is a list

		self.complete_header = runTimeVarOrder + self.header
		self.win = visual.Window(fullscr=True,allowGUI=True, color="black", units='pix',screen=int(runTimeVars['tv_screen']))
		#self.win = visual.Window([1500,900],allowGUI=True, color="black", units='pix',screen=2)
		
		#create psychopy window for experimenter
		self.win2 = visual.Window([800,800], color="black", allowGUI=True,units='pix',screen=int(runTimeVars['exp_screen']))
		self.win2.flip()
		
		#create psychopy window for tracking trials
		self.win3 = visual.Window(fullscr=True, color="black", allowGUI=True,units='pix',screen=int(runTimeVars['side_screen']))
		self.win3.flip()

		visual.TextStim(win=self.win,text="Loading stimuli...").draw()
		#self.win.flip()
		self.pics =  loadFiles('stimuli/images','.png','image', win=self.win)
		self.sounds = loadFiles('stimuli/audio','.wav','sound', win=self.win)
		self.cf_movie_path = "stimuli/movies/ag_no_audio.mp4"
		self.cf = visual.MovieStim(win=self.win,filename = self.cf_movie_path,size=(640,360),loop=True)
		self.cf_duration = .75
		self.cf_max_duration = 5
		self.ag_movie_path = "stimuli/movies/laughing_baby_no_audio.mp4"
		self.ag = visual.MovieStim(win=self.win,filename = self.ag_movie_path,size=(640,360),loop=True)
		self.ag_duration = 2
		self.ag_max_duration = 10
		#self.sounds =  loadFiles('stimuli/sounds','.wav','sound', win=self.win)
		self.waitForTarget = visual.TextStim(win=self.win,text="",color="black",height=40)
		self.fixationCross = visual.TextStim(win=self.win,text="+",color="black",height=40)

		self.preFixationDelay = .75
		self.postFixationDelay = 0
		#self.fam_timeout = 15

		self.position = {'left': (-500,0), 'right': (500,0), 'center':(0,0)}
		self.size = runTimeVars['image_size']

		self.inputDevice = "keyboard"
		self.validResponses = {'z':'left','slash':'right'} #change to whatever keys you want to use
		self.validKeys = ['space']
		self.method = runTimeVars['method']

		self.runtime_vars_list = [runTimeVars[runtime_var_name] for runtime_var_name in runTimeVarOrder]
		
		self.instructions_text = "Welcome to the ManyBabies 5 demo!\n\nWhen you see the laughing baby, hit space to advance to the next trial.\n\nDuring familiarization, for contingent trials, press the right arrow key when the infant is looking to the screen and the left arrow key when they look away. Otherwise, for fixed durations, the experiment will proceed at the end of the familiarization time.\n\nAfter the familiarization, a central fixation will appear. Hit the space bar to advance (once the infant is looking). The second central fixation in between the two test trial phases advances automatically.\n\nHit q to start the experiment!"
		
	# may need to remove the /2 when running on the lab computer. Retina screen resolution issue..
	def create_placeholder(self,lineColor="black", fillColor="white",size=(525,525),pos=(0,0)):
	 	return visual.Rect(win=self.win,size=size, pos=pos, lineColor=lineColor, fillColor=fillColor, lineWidth=3)

	def show_instructions(self,text):
		self.win.flip()
		#visual.TextStim(win=self.win,text=text,color="white",height=40,pos=(0,0),wrapWidth=1000).draw()
		image=visual.ImageStim(self.win, 'stimuli/images/bunnies.png',mask=None,interpolate=True)
		image.setPos((0,0))
		image.draw()
		self.win.flip()
		event.waitKeys(keyList=['q'])
	
	def show_ag(self,curTrial,gaze_contingent=False):
		
		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: AG"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
		trialInfoStim_3.draw()
		ag_square_skeleton=visual.Rect(self.win2,lineColor="black",fillColor="yellow",size=[300,200])
		ag_square_skeleton.draw()
		self.win2.flip()
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
				keys = event.getKeys()
				if keys:
					key = keys[0]
					print(key)
					if key in self.validKeys:
						key_pressed = True  
						print(key_pressed)   
				if clock.getTime() >= self.ag_max_duration:
					timeout = True 
					print(clock.getTime())
		
		#stop the movie
		self.ag.stop()
		self.ag.seek(0)
		self.sounds['laughing_baby']['stim'].stop()


		self.win.flip()
		self.win2.flip()

	def show_cf(self,curTrial,gaze_contingent=False):

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		if gaze_contingent:
			trialInfo+="Phase: CF CONTINGENT"
			stim_color = "yellow"
		else:
			trialInfo+="Phase: CF"
			stim_color="white"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
		trialInfoStim_3.draw()
		cf_skeleton=visual.Circle(self.win2,lineColor="black",fillColor=stim_color,size=[150,150])
		cf_skeleton.draw()
		self.win2.flip()
		self.win3.flip()

		event.clearEvents()
		# present central fixation stimulus
		clock = core.Clock()  # Create a clock to track time
		clock.reset()
		# Play the movie
		self.cf.play()
		self.sounds['ag']['stim'].play()
		if not gaze_contingent:
			while clock.getTime() < self.cf_duration:  
				#self.cf.play()
				self.cf.draw()
				self.win.flip()
		elif gaze_contingent:
			key_pressed = False
			timeout = False
			while (not key_pressed) and (not timeout):
				#self.ag.play()
				self.cf.draw()
				self.win.flip()
				keys = event.getKeys()
				if keys:
					key = keys[0]
					print(key)
					if key in self.validKeys:
						key_pressed = True  
						print(key_pressed)   
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
	
	def show_test(self,curTrial,position_type=1):

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: TEST"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
		trialInfoStim_3.draw()
		square_skeleton_1=visual.Rect(self.win2,lineColor="black",fillColor="blue",size=[150,150],pos=(-150,0))
		square_skeleton_2=visual.Rect(self.win2,lineColor="black",fillColor="blue",size=[150,150],pos=(150,0))
		square_skeleton_1.draw()
		square_skeleton_2.draw()
		self.win2.flip()
		self.win3.flip()

		#show test trial
		self.create_placeholder(pos=self.position['left'],size=self.size+10).draw()
		self.create_placeholder(pos=self.position['right'],size=self.size+10).draw()

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
		self.win.flip()
		
        # present for test time
		core.wait(test_time)

		self.win.flip()
		self.win2.flip()

	def show_familiarization(self,curTrial, gaze_contingent=False):

		########build and present text screen for hand coding######
		trialInfo="Experiment: " + expName +"\n"
		trialInfo+="Participant: " + self.runtime_vars_list[0] +"\n"
		trialInfo+="Trial Number: " + str(curTrial["trial_number"]) + "\n"
		trialInfo+="Phase: FAMILIAR"

		trialInfoStim=visual.TextStim(self.win2,text=trialInfo,color="white",height=30,wrapWidth=1200,pos=(0,-200))
		trialInfoStim.draw()
		trialInfoStim_3=visual.TextStim(self.win3,text=trialInfo,color="white",height=60,wrapWidth=1200,pos=(0,0))
		trialInfoStim_3.draw()
		square_skeleton=visual.Rect(self.win2,lineColor="black",fillColor="red",size=[150,150],pos=(0,0))
		square_skeleton.draw()
		self.win2.flip()
		self.win3.flip()

		#show familiarization
		#show size
		self.pics[curTrial['familiar_stimulus']]['stim'].size = self.size
		print(self.pics[curTrial['familiar_stimulus']]['stim'].size)
		self.create_placeholder(pos=self.position['center'],size=self.size+10).draw()
		self.pics[curTrial['familiar_stimulus']]['stim'].pos = self.position['center']
		self.pics[curTrial['familiar_stimulus']]['stim'].draw()
		
		event.clearEvents()
		overall_timer = core.Clock()  # Timer to measure overall elapsed time
		# Start overall timer
		overall_timer.reset()
		total_held_time = 0  # Accumulated time the infant has been registered as looking to the stimulus
		looks = 0
		keypress_list = []
		look_list = []

		self.win.flip()

		print(int(curTrial['familiarization_time']))

		#no gaze contingency
		if not gaze_contingent:

			core.wait(int(curTrial['familiarization_time']))
		
		else:
			#procedure for gaze contingency
			looking = False  # Track if infant is currently looking
			clock = core.Clock()
			# while total_held_time < int(curTrial['familiarization_time']) and overall_timer.getTime()<self.fam_timeout:
			# 	responded = event.getKeys(keyList=['right','left'], timeStamped=overall_timer)
			# 	look_list.extend(responded)
			# 	if responded:
			# 		response = responded[0]
			# 		print(response)

			# 	if responded and response[0]=="right" and not looking:
			# 		clock.reset()
			# 		looking = True
			# 		print(looking)
			# 		looks += 1

			# 	if looking:
			# 		total_held_time += clock.getTime()
			# 		clock.reset()

			# 	if responded and response[0]=="left":
			# 		looking = False
			# 		print(looking)
			cur_look_length = 0
			time_left = int(curTrial['familiarization_time'])
			count_down_timer = core.CountdownTimer(time_left)
			while (count_down_timer.getTime() > 0 or not looking) and overall_timer.getTime()<int(curTrial['familiarization_time_timeout']):
				responded = event.getKeys(keyList=['right','left'], timeStamped=clock)
				keypress_list.extend(responded)
				if responded:
					response = responded[0]
					print(response)

				if responded and response[0]=="right" and not looking:
					clock.reset()
					time_left = time_left - cur_look_length
					count_down_timer = core.CountdownTimer(time_left)
					looking = True
					print(looking)
					print(time_left)
					looks += 1

					#looking: visual feedback on experimenter monitor
					square_skeleton.color = "green"
					trialInfoStim.draw()
					square_skeleton.draw()
					self.win2.flip()

				# if looking:
				# 	total_held_time += clock.getTime()
				# 	clock.reset()

				if responded and response[0]=="left":
					clock.reset()
					looking = False
					cur_look_length = response[1]
					total_held_time += cur_look_length
					print(looking)

					#look away: visual feedback on experimenter monitor
					square_skeleton.color = "red"
					trialInfoStim.draw()
					square_skeleton.draw()
					self.win2.flip()

					#store last look
					look_list.append(cur_look_length)

		
			if looking:
				total_held_time += time_left
				cur_look = clock.getTime()
				print(cur_look)
				look_list.append(cur_look)

		# Clear screen
		self.win.flip()
		self.win2.flip()

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

	train_header = exp.complete_header[:] #assign list by value since we're extending it below and don't want to change the orig header list
	train_header.extend(('total_accumulated_looking_time','elapsed_time','looks','keypress_list','look_list'))
	printHeader(train_header,headerFile="familiarization_header.txt",separator=",")

	if exp.method == "contingent":
		fam_contingent = True
	else:
		fam_contingent = False

	exp.show_instructions(exp.instructions_text)
	for i,curTrial in enumerate(exp.trialInfo):
		exp.show_ag(curTrial,gaze_contingent=True)
		exp.show_familiarization(curTrial, gaze_contingent=fam_contingent)
		exp.show_cf(curTrial,gaze_contingent=True)
		exp.show_test(curTrial,position_type=1)
		exp.show_cf(curTrial)
		exp.show_test(curTrial,position_type=2)






