import random
import os

fribble_shapes = ["Tripod", "Sims", "Diamond", "Pyramid", "Pumpkin", "Pacman", "Gumdrop", "Diamond", "Cylinder", "Crinkle", "Bowtie","Bowl","Arrow"]
fribble_pairs = {
    "set_1": [["Tripod","Diamond"],["SimsDiamond","Cylinder"],["Pyramid","Bowtie"],["Pumpkin","Crinkle"],["Pacman","Arrow"],["Gumdrop","Bowl"]],
    "set_2": [["Tripod","Bowl"],["SimsDiamond","Pumpkin"],["Pyramid","Gumdrop"],["Cylinder","Pacman"],["Crinkle","Diamond"],["Arrow","Bowtie"]]
}

fractal_shapes = []
fractal_pairs = {}

# factors
complexity = ["simple","complex"] #complexity
familiarization_times = [5,10,15] #familiarization times
reverse_order = ["base","rev"] # reverse order
familiar_role = [0,1] # which item in pair is familiar
which_stims_first = ["fribble_first","fractal_first"] # whether fractals or fribbles come first in the test list
test_locations_familiar = [["left","right"],["right","left"]] # positions of the familiar item at test on the first and second half of the test trial (position flips)

