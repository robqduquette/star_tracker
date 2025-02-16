import matplotlib.pyplot as plt
import numpy as np
import sys
from util import Vector3, import_starmap

args = sys.argv
if len(args) != 2:
    print("Invalid arguments. Usage: vis_map.py MAP_FILE.txt")
    exit()

starmap = import_starmap(args[1])
dist = 5 # distance of stars from origin

X = []
Y = []
Z = []
for star in starmap:
    pos = star[0] * (dist * 2)
    X.append(pos.x)
    Y.append(pos.y)
    Z.append(pos.z)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1.0, 1.0, 1.0])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')


# plot stars
ax.scatter(X,Y,Z,c='r')

# draw earth
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v) * dist
y = np.sin(u)*np.sin(v) * dist
z = np.cos(v) * dist
ax.plot_wireframe(x, y, z, color="b", alpha=0.5)



plt.show()