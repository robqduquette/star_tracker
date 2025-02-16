from util import Vector3
import random
import sys

args = sys.argv
if len(args) != 2:
    print("Incorrect number of arguments. Usage: gen_starmap.py NUM_STARS")
    exit()

num_stars = int(args[1])
random.seed(num_stars) # make generating tests deterministic on input parameters

def rand_pos():
    """ Generate a random float between -1 and 1 """
    return 2 * random.random() - 1

stars = []
for i in range(num_stars):
    direction = Vector3(*[rand_pos() for _ in range(3)]).unit()
    brightness = random.random()
    stars.append((direction, brightness))

file = "maps/map_" + str(num_stars) + "_stars.txt"
with open(file, 'w') as f:
    f.write("num_stars " + str(num_stars) + "\n") # metadata of number of stars

    for star in stars:
        f.write(str(star[0].x) + " ")
        f.write(str(star[0].y) + " ")
        f.write(str(star[0].z) + " ")
        f.write(str(star[1]) + "\n")

    print("Wrote map to",file)


