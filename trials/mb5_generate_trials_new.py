import random
import os

def generate_trials(subj_code,seed):
	separator=","
	
	#set seed
	random.seed(int(seed))
	
	#open trial file and write header
	trial_file = open(os.path.join(os.getcwd(),'trials',subj_code+'_trials.csv'),'w')
	header = separator.join(["subj_code","seed","trial_number","familiar_stimulus","novel_stimulus","complexity_condition","familiarization_time","familiar_location_1","familiar_location_2","test_time_1","test_time_2","familiarization_time_timeout"])
	trial_file.write(header+'\n')
	
	#define trial parameters
	familiarization_times=[5,10,15]
	test_time = 5
	image_name_sep = "_"
	trial_num_set = 6
	sets = ["fribbles","fractals"]
	familiar_location_sets = [["left","right"],["left","right"],["left","right"],["left","right"],["left","right"],["left","right"]]

	#image_ext = ".jpg"
	fribble_dict = {
		'set_1': [["Tripod","Diamond"],["SimsDiamond","Cylinder"],["Pyramid","Bowtie"],["Pacman","Arrow"],["Crinkle","Pumpkin"],["Bowl","Gumdrop"]],
		'set_2': [["Tripod","Bowl"],["SimsDiamond","Pumpkin"],["Pyramid","Gumdrop"],["Pacman","Cylinder"],["Crinkle","Diamond"],["Bowtie","Arrow"]]
	}
	fractal_dict = {
		'set_1': [["pair1_a","pair1_b"],["pair2_a","pair2_b"],["pair3_a","pair3_b"],["pair4_a","pair4_b"],["pair5_a","pair5_b"],["pair6_a","pair6_b"]]
	}

	fribble_complexity_sets = [["Simple","Complex"],["Complex","Simple"],["Simple","Complex"]]
	fractal_complexity_sets = [["simple","complex"],["simple","complex"],["simple","complex"]]

	complexity_order_dict = {
		'order_1': ["simple","complex","complex","simple","complex","simple","simple","complex","complex","simple","simple","complex"],
		'order_2': ["complex","simple","simple","complex","simple","complex","complex","simple","simple","complex","complex","simple"]
	}
	
	#create trials
	trials = []
	for i in range(num_items):
		item = str(i+1)
		for angle in angle_list:
			for match in match_list:
				if match == "same":
					image_name = item+image_name_sep+angle
					correct_response = "z"
				else:
					image_name = item+image_name_sep+angle+image_name_sep+"R"
					correct_response = "m"
				trials.append([subj_code,seed,test_mode,image_name,item,angle,match,correct_response])
	print(trials)
	random.shuffle(trials)
	
	for cur_trial in trials:
		print(cur_trial)
		trial_file.write(separator.join(map(str,cur_trial))+'\n')
	
	trial_file.close()
	return True


if __name__ == '__main__':
	generate_trials("test",100,"practice")	
