from Situation import Situation
from util import Vector3, import_starmap
from solution import solution
from Sensor import Sensor

file = 'maps/map_500_stars.txt' #'maps/map_id.txt'

starmap = import_starmap(file)
params = {'fov': (100,80),
            'resolution': (400,300)}
sensor = Sensor(params)

#problem = Situation(starmap, [], solution)


sensor.gen_measurements(starmap, Vector3(0,-1.5,0), 1).save("output.png")


# make a gif of rotating through one axis
frames = []
n = 1
for i in range(360//n):
    frames.append(sensor.gen_measurements(starmap, Vector3(0,i * n,i*n) * 3.1415 / 180, 0))

frames[0].save("gif.gif", save_all = True, append_images= frames[1:], dration=5, loop = 0)
""""""