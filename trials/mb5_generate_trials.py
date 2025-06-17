import random
import os
import pandas

#function for reverse ordering blockwise
def split_and_reverse(lst):
    if len(lst) % 2 != 0:
        raise ValueError("List length must be even to split evenly in half.")
    
    mid = len(lst) // 2
    first_half = lst[:mid][::-1]
    second_half = lst[mid:][::-1]
    
    return first_half + second_half

#function for handling both within block reverse ordering and full trial list reverse ordering based on parameters
def handle_reverse_ordering(trial_list_element,reverse_order_block,reverse_order_list):
    # reverse block and reverse order
    if reverse_order_block == "base_rev":
        if reverse_order_list == "rev":
            return split_and_reverse(trial_list_element)[::-1]
        else:
            return split_and_reverse(trial_list_element)
    else:
        if reverse_order_list == "rev":
            return trial_list_element[::-1]
        else:
            return trial_list_element

def generate_trials():
    #define trial parameters
    familiarization_time_sets = [[5,10,15],[10,15,5],[15,5,10]] #familiarization times
    reverse_order_block = ["base_block","base_rev"]
    reverse_order_list = ["base","rev"] # reverse order
    familiar_role = [0,1] # which item in pair is familiar
    test_time = 5
    trial_num_set = 6
    trial_num = 12
    
    fribble_dict = {
		'set_1': [["Tripod","Diamond"],["SimsDiamond","Cylinder"],["Pyramid","Bowtie"],["Pacman","Arrow"],["Crinkle","Pumpkin"],["Bowl","Gumdrop"]],
		'set_2': [["Pacman","Cylinder"],["Bowtie","Arrow"],["Tripod","Bowl"],["Crinkle","Diamond"],["Pyramid","Gumdrop"],["SimsDiamond","Pumpkin"]]
	}
    fribble_sets = ["set_1", "set_2"]

    fractal_dict = {
        'set_1': [["pair1_a", "pair1_b"], ["pair2_a", "pair2_b"], ["pair3_a", "pair3_b"], ["pair4_a", "pair4_b"], ["pair5_a", "pair5_b"], ["pair6_a", "pair6_b"]]
    }
    fractal_sets = ["set_1"]

    complexity_order_dict = {
        'order_1': ["simple", "complex", "complex", "simple", "complex", "simple", "simple", "complex", "complex", "simple", "simple", "complex"],
        'order_2': ["complex", "simple", "simple", "complex", "simple", "complex", "complex", "simple", "simple", "complex", "complex", "simple"]
    }
    complexity_orders = ["order_1", "order_2"]

    test_familiar_location_dict = {
        'loc_order_1': ["left", "right", "right", "left", "left", "right", "left", "right", "left", "left", "right", "right"],
        'loc_order_2': ["right", "left", "left", "right", "right", "left", "right", "left", "right", "right", "left", "left"]
    }
    test_familiar_locations = ['loc_order_1', 'loc_order_2']

    trial_list_id = 1

    
    for cur_test_familiar_location in test_familiar_locations:
        for cur_fribble_set in fribble_sets:
            for cur_fractal_set in fractal_sets:
                for cur_reverse_order_block in reverse_order_block:
                    for cur_complexity_order in complexity_orders:
                        for cur_reverse_order_list in reverse_order_list:
                            for cur_familiarization_time_set in familiarization_time_sets:
                                for cur_familiar_role in familiar_role:
                                    print(trial_list_id)

                                    #handle familiarization_times
                                    fam_time_1 = cur_familiarization_time_set[0]
                                    fam_time_2 = cur_familiarization_time_set[1]
                                    fam_time_3 = cur_familiarization_time_set[2]
                                    fam_time_list = [fam_time_2,fam_time_3,fam_time_1,fam_time_1,fam_time_3,fam_time_2,fam_time_1,fam_time_3,fam_time_2, fam_time_3,fam_time_2,fam_time_1]

                                    #create complexity and test location order lists
                                    cur_complexity_list = complexity_order_dict[cur_complexity_order]
                                    cur_complexity_list_1 = cur_complexity_list[:trial_num_set]
                                    cur_complexity_list_2 = cur_complexity_list[trial_num_set:]
                                    cur_test_familiar_location_list = test_familiar_location_dict[cur_test_familiar_location]

                                    #handle familiar items
                                    cur_familiar_fribble_items = [pair[cur_familiar_role] for pair in fribble_dict[cur_fribble_set]]
                                    cur_familiar_fractal_items = [pair[cur_familiar_role] for pair in fractal_dict[cur_fractal_set]]
                                    cur_familiar_items = cur_familiar_fribble_items + cur_familiar_fractal_items
                                    # convert to image names
                                    cur_familiar_fribble_images = [cur_familiar_fribble_items[i]+"_"+cur_complexity_list_1[i].capitalize() for i in range(len(cur_familiar_fribble_items))]
                                    cur_familiar_fractal_images = ["fractal_"+cur_complexity_list_2[i]+"_"+cur_familiar_fractal_items[i]+"_bright" for i in range(len(cur_familiar_fractal_items))]
                                    cur_familiar_images = cur_familiar_fribble_images + cur_familiar_fractal_images

                                    #handle novel items
                                    if cur_familiar_role == 0:
                                        cur_novel_role = 1
                                    else:
                                        cur_novel_role = 0
                                    cur_novel_fribble_items = [pair[cur_novel_role] for pair in fribble_dict[cur_fribble_set]]
                                    cur_novel_fractal_items = [pair[cur_novel_role] for pair in fractal_dict[cur_fractal_set]]
                                    cur_novel_items = cur_novel_fribble_items + cur_novel_fractal_items
                                    # convert to image names
                                    cur_novel_fribble_images = [cur_novel_fribble_items[i]+"_"+cur_complexity_list_1[i].capitalize() for i in range(len(cur_novel_fribble_items))]
                                    cur_novel_fractal_images = ["fractal_"+cur_complexity_list_2[i]+"_"+cur_novel_fractal_items[i]+"_bright" for i in range(len(cur_novel_fractal_items))]
                                    cur_novel_images = cur_novel_fribble_images + cur_novel_fractal_images

                                    # reverse block and reverse order
                                    ordered_cur_complexity_list = handle_reverse_ordering(cur_complexity_list,cur_reverse_order_block,cur_reverse_order_list)
                                    ordered_cur_test_familiar_location_list = handle_reverse_ordering(cur_test_familiar_location_list,cur_reverse_order_block,cur_reverse_order_list)
                                    switched_ordered_cur_test_familiar_location_list = ["right" if x == "left" else "left" for x in ordered_cur_test_familiar_location_list]
                                    ordered_fam_time_list = handle_reverse_ordering(fam_time_list,cur_reverse_order_block,cur_reverse_order_list)
                                    timeout_ordered_fam_time_list = [2*t for t in ordered_fam_time_list]
                                    ordered_cur_familiar_items = handle_reverse_ordering(cur_familiar_items,cur_reverse_order_block,cur_reverse_order_list)
                                    ordered_cur_familiar_images = handle_reverse_ordering(cur_familiar_images,cur_reverse_order_block,cur_reverse_order_list)
                                    ordered_cur_novel_items = handle_reverse_ordering(cur_novel_items,cur_reverse_order_block,cur_reverse_order_list)
                                    ordered_cur_novel_images = handle_reverse_ordering(cur_novel_images,cur_reverse_order_block,cur_reverse_order_list)
                                    

                                    cur_data = {
                                        "trial_number": range(1,trial_num+1),
                                        "familiar_stimulus": ordered_cur_familiar_images,
                                        "novel_stimulus": ordered_cur_novel_images,
                                        "familiar_stimulus_item": ordered_cur_familiar_items,
                                        "novel_stimulus_item": ordered_cur_novel_items,
                                        "complexity_condition": ordered_cur_complexity_list,
                                        "familiarization_time": ordered_fam_time_list,
                                        "familiar_location_1": ordered_cur_test_familiar_location_list,
                                        "familiar_location_2": switched_ordered_cur_test_familiar_location_list,
                                        "test_time_1": [test_time] * trial_num,
                                        "test_time_2": [test_time] * trial_num,
                                        "familiarization_time_timeout": timeout_ordered_fam_time_list}
                                    cur_df = pandas.DataFrame(cur_data)
                                    cur_df.to_csv(os.path.join(os.getcwd(),'trial_lists','mb5_trial_list_'+str(trial_list_id)+'.csv'), index=False)
                                    #update trial list id
                                    trial_list_id+=1

    return True

if __name__ == '__main__':
    generate_trials()	
