from Situation import Situation, gen_measurements
from util import Vector3, import_starmap
from solution import solution

file = 'maps/map_10_stars.txt'

starmap = import_starmap(file)

#problem = Situation(starmap, [], solution)
print(gen_measurements(starmap, Vector3(0,0,0)))