import random
import os
import pandas

seed = 10


def split_and_reverse(lst):
    """Reverse each half of an even-length list, preserving the two-block structure."""
    if len(lst) % 2 != 0:
        raise ValueError("List length must be even to split evenly in half.")

    mid = len(lst) // 2
    first_half = lst[:mid][::-1]
    second_half = lst[mid:][::-1]

    return first_half + second_half


def handle_reverse_ordering(trial_list_element, reverse_order_block, reverse_order_list):
    """Handle within-block reversal and/or full-list reversal."""
    if reverse_order_block == "base_rev":
        if reverse_order_list == "rev":
            return split_and_reverse(trial_list_element)[::-1]
        return split_and_reverse(trial_list_element)

    if reverse_order_list == "rev":
        return trial_list_element[::-1]
    return trial_list_element


def reorder_by_indices(lst, indices):
    """Apply a shared trial-order permutation to any length-12 trial-level list."""
    return [lst[i] for i in indices]


def make_lab_order(lab_number, cur_seed, trial_num_set):
    """
    Create one within-block shuffled order for a lab.

    The fribble block and fractal block are shuffled separately, using different
    incrementing seeds. This keeps fribbles together and fractals together while
    still giving each lab a different base trial order.

    With cur_seed=10:
      lab1 uses fribble_seed=10, fractal_seed=11
      lab2 uses fribble_seed=12, fractal_seed=13
      lab3 uses fribble_seed=14, fractal_seed=15
    """
    fribble_seed = cur_seed + (lab_number - 1) * 2
    fractal_seed = fribble_seed + 1

    fribble_indices = list(range(trial_num_set))
    fractal_indices = list(range(trial_num_set, trial_num_set * 2))

    random.Random(fribble_seed).shuffle(fribble_indices)
    random.Random(fractal_seed).shuffle(fractal_indices)

    return fribble_indices + fractal_indices, fribble_seed, fractal_seed


def generate_trials(cur_seed=seed, num_labs=3):
    # define trial parameters
    familiarization_time_sets = [[5, 10, 15], [10, 15, 5], [15, 5, 10]]
    reverse_order_block = ["base_block", "base_rev"]
    reverse_order_list = ["base", "rev"]
    familiar_role = [0, 1]
    test_time = 5
    trial_num_set = 6
    trial_num = 12

    fribble_dict = {
        'set_1': [["Tripod", "Diamond"], ["SimsDiamond", "Cylinder"], ["Pyramid", "Bowtie"], ["Pacman", "Arrow"], ["Crinkle", "Pumpkin"], ["Bowl", "Gumdrop"]],
        'set_2': [["Pacman", "Cylinder"], ["Bowtie", "Arrow"], ["Tripod", "Bowl"], ["Crinkle", "Diamond"], ["Pyramid", "Gumdrop"], ["SimsDiamond", "Pumpkin"]]
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

    rel_image_path = 'stimuli/images/'
    img_ext = ".png"

    cur_test_familiar_location = "loc_order_1"
    cur_fribble_set = "set_1"

    trial_lists_root = os.path.join(os.getcwd(), 'trial_lists')
    os.makedirs(trial_lists_root, exist_ok=True)

    for lab_number in range(1, num_labs + 1):
        lab_name = f"lab{lab_number}"
        lab_dir = os.path.join(trial_lists_root, lab_name)
        os.makedirs(lab_dir, exist_ok=True)

        lab_order, fribble_seed, fractal_seed = make_lab_order(
            lab_number=lab_number,
            cur_seed=cur_seed,
            trial_num_set=trial_num_set
        )

        print(f"{lab_name}: fribble_seed={fribble_seed}, fractal_seed={fractal_seed}, lab_order={lab_order}")

        trial_list_id = 1

        # for cur_test_familiar_location in test_familiar_locations:
        # for cur_fribble_set in fribble_sets:
        for cur_fractal_set in fractal_sets:
            for cur_reverse_order_block in reverse_order_block:
                for cur_complexity_order in complexity_orders:
                    for cur_reverse_order_list in reverse_order_list:
                        for cur_familiarization_time_set in familiarization_time_sets:
                            for cur_familiar_role in familiar_role:
                                print(lab_name, trial_list_id)

                                # handle familiarization_times
                                fam_time_1 = cur_familiarization_time_set[0]
                                fam_time_2 = cur_familiarization_time_set[1]
                                fam_time_3 = cur_familiarization_time_set[2]
                                fam_time_list = [fam_time_2, fam_time_3, fam_time_1, fam_time_1, fam_time_3, fam_time_2,
                                                 fam_time_1, fam_time_3, fam_time_2, fam_time_3, fam_time_2, fam_time_1]

                                # create complexity and test location order lists
                                cur_complexity_list = complexity_order_dict[cur_complexity_order]
                                cur_complexity_list_1 = cur_complexity_list[:trial_num_set]
                                cur_complexity_list_2 = cur_complexity_list[trial_num_set:]
                                cur_test_familiar_location_list = test_familiar_location_dict[cur_test_familiar_location]

                                # handle familiar items
                                cur_familiar_fribble_items = [pair[cur_familiar_role] for pair in fribble_dict[cur_fribble_set]]
                                cur_familiar_fractal_items = [pair[cur_familiar_role] for pair in fractal_dict[cur_fractal_set]]
                                cur_familiar_items = cur_familiar_fribble_items + cur_familiar_fractal_items

                                # convert to image names
                                cur_familiar_fribble_images = [
                                    cur_familiar_fribble_items[i] + "_" + cur_complexity_list_1[i].capitalize()
                                    for i in range(len(cur_familiar_fribble_items))
                                ]
                                cur_familiar_fractal_images = [
                                    "fractal_" + cur_complexity_list_2[i] + "_" + cur_familiar_fractal_items[i] + "_bright"
                                    for i in range(len(cur_familiar_fractal_items))
                                ]
                                cur_familiar_images = cur_familiar_fribble_images + cur_familiar_fractal_images

                                # handle novel items
                                if cur_familiar_role == 0:
                                    cur_novel_role = 1
                                else:
                                    cur_novel_role = 0

                                cur_novel_fribble_items = [pair[cur_novel_role] for pair in fribble_dict[cur_fribble_set]]
                                cur_novel_fractal_items = [pair[cur_novel_role] for pair in fractal_dict[cur_fractal_set]]
                                cur_novel_items = cur_novel_fribble_items + cur_novel_fractal_items

                                # convert to image names
                                cur_novel_fribble_images = [
                                    cur_novel_fribble_items[i] + "_" + cur_complexity_list_1[i].capitalize()
                                    for i in range(len(cur_novel_fribble_items))
                                ]
                                cur_novel_fractal_images = [
                                    "fractal_" + cur_complexity_list_2[i] + "_" + cur_novel_fractal_items[i] + "_bright"
                                    for i in range(len(cur_novel_fractal_items))
                                ]
                                cur_novel_images = cur_novel_fribble_images + cur_novel_fractal_images

                                # First apply the lab-specific within-block shuffle.
                                # Then apply the existing reverse-ordering manipulations.
                                shuffled_cur_complexity_list = reorder_by_indices(cur_complexity_list, lab_order)
                                shuffled_cur_test_familiar_location_list = reorder_by_indices(cur_test_familiar_location_list, lab_order)
                                shuffled_fam_time_list = reorder_by_indices(fam_time_list, lab_order)
                                shuffled_cur_familiar_items = reorder_by_indices(cur_familiar_items, lab_order)
                                shuffled_cur_familiar_images = reorder_by_indices(cur_familiar_images, lab_order)
                                shuffled_cur_novel_items = reorder_by_indices(cur_novel_items, lab_order)
                                shuffled_cur_novel_images = reorder_by_indices(cur_novel_images, lab_order)

                                ordered_cur_complexity_list = handle_reverse_ordering(shuffled_cur_complexity_list, cur_reverse_order_block, cur_reverse_order_list)
                                ordered_cur_test_familiar_location_list = handle_reverse_ordering(shuffled_cur_test_familiar_location_list, cur_reverse_order_block, cur_reverse_order_list)
                                switched_ordered_cur_test_familiar_location_list = [
                                    "right" if x == "left" else "left"
                                    for x in ordered_cur_test_familiar_location_list
                                ]
                                ordered_fam_time_list = handle_reverse_ordering(shuffled_fam_time_list, cur_reverse_order_block, cur_reverse_order_list)
                                timeout_ordered_fam_time_list = [2 * t for t in ordered_fam_time_list]
                                ordered_cur_familiar_items = handle_reverse_ordering(shuffled_cur_familiar_items, cur_reverse_order_block, cur_reverse_order_list)
                                ordered_cur_familiar_images = handle_reverse_ordering(shuffled_cur_familiar_images, cur_reverse_order_block, cur_reverse_order_list)
                                ordered_cur_novel_items = handle_reverse_ordering(shuffled_cur_novel_items, cur_reverse_order_block, cur_reverse_order_list)
                                ordered_cur_novel_images = handle_reverse_ordering(shuffled_cur_novel_images, cur_reverse_order_block, cur_reverse_order_list)

                                ordered_cur_familiar_images_path = [rel_image_path + im + img_ext for im in ordered_cur_familiar_images]
                                ordered_cur_novel_images_path = [rel_image_path + im + img_ext for im in ordered_cur_novel_images]

                                left_image_path_1 = [
                                    familiar_item if fam_location == "left" else novel_item
                                    for familiar_item, novel_item, fam_location in zip(
                                        ordered_cur_familiar_images_path,
                                        ordered_cur_novel_images_path,
                                        ordered_cur_test_familiar_location_list
                                    )
                                ]
                                right_image_path_1 = [
                                    familiar_item if fam_location == "right" else novel_item
                                    for familiar_item, novel_item, fam_location in zip(
                                        ordered_cur_familiar_images_path,
                                        ordered_cur_novel_images_path,
                                        ordered_cur_test_familiar_location_list
                                    )
                                ]
                                left_image_path_2 = [
                                    familiar_item if fam_location == "left" else novel_item
                                    for familiar_item, novel_item, fam_location in zip(
                                        ordered_cur_familiar_images_path,
                                        ordered_cur_novel_images_path,
                                        switched_ordered_cur_test_familiar_location_list
                                    )
                                ]
                                right_image_path_2 = [
                                    familiar_item if fam_location == "right" else novel_item
                                    for familiar_item, novel_item, fam_location in zip(
                                        ordered_cur_familiar_images_path,
                                        ordered_cur_novel_images_path,
                                        switched_ordered_cur_test_familiar_location_list
                                    )
                                ]

                                cur_data = {
                                    "trial_number": range(1, trial_num + 1),
                                    "familiar_stimulus": ordered_cur_familiar_images,
                                    "novel_stimulus": ordered_cur_novel_images,
                                    "familiar_stimulus_item": ordered_cur_familiar_items,
                                    "novel_stimulus_item": ordered_cur_novel_items,
                                    "complexity_condition": ordered_cur_complexity_list,
                                    "familiarization_time": ordered_fam_time_list,
                                    "familiar_stimulus_path": ordered_cur_familiar_images_path,
                                    "novel_stimulus_path": ordered_cur_novel_images_path,
                                    "familiar_location_1": ordered_cur_test_familiar_location_list,
                                    "familiar_location_2": switched_ordered_cur_test_familiar_location_list,
                                    "left_image_path_1": left_image_path_1,
                                    "right_image_path_1": right_image_path_1,
                                    "left_image_path_2": left_image_path_2,
                                    "right_image_path_2": right_image_path_2,
                                    "test_time_1": [test_time] * trial_num,
                                    "test_time_2": [test_time] * trial_num,
                                    "familiarization_time_timeout": timeout_ordered_fam_time_list,
                                    "lab": [lab_name] * trial_num,
                                    "fribble_shuffle_seed": [fribble_seed] * trial_num,
                                    "fractal_shuffle_seed": [fractal_seed] * trial_num
                                }
                                cur_df = pandas.DataFrame(cur_data)
                                cur_df.to_csv(
                                    os.path.join(lab_dir, 'mb5_trial_list_' + str(trial_list_id) + '.csv'),
                                    index=False
                                )

                                trial_list_id += 1

    return True


if __name__ == '__main__':
    generate_trials()
