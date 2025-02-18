import matplotlib.pyplot as plt
import numpy as np
import sys
from util import Vector3, import_starmap
import WebMercator

args = sys.argv
if len(args) < 2:
    print("Invalid arguments. Usage: vis_map.py MAP_FILE.txt [plot_types]")
    exit()

plot_types = {'3d':False, 'mercator': False}

# default
if len(args) == 2:
    print('no args provided',args)
    plot_types['3d'] = True # sets default plot types

# check plot type arguments
for arg in args[2:]:
    if not arg in plot_types:
        raise ValueError("\'" + arg + "\' is not a valid options for plot type. Valid options: " + str(list(plot_types.keys())))
    plot_types[arg] = True


# import starmap data
starmap = import_starmap(args[1])
dist = 5 # distance of stars from origin

X = []
Y = []
Z = []
for star in starmap:
    pos = star[0]
    X.append(pos.x)
    Y.append(pos.y)
    Z.append(pos.z)

if plot_types['3d']:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    lims = [-2.1 * dist, 2.1 * dist]
    ax.set_xlim(*lims)
    ax.set_ylim(*lims)
    ax.set_zlim(*lims)

    # plot stars
    ax.scatter(X * (dist * 2),Y * (dist * 2),Z * (dist * 2),c='r')

    # draw earth
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v) * dist
    y = np.sin(u)*np.sin(v) * dist
    z = np.cos(v) * dist
    ax.plot_wireframe(x, y, z, color="b", alpha=0.5)

    fig.suptitle('3D starmap')
    plt.show()

if plot_types['mercator']:
    # convert 3d coords to lat-lon
    inc = np.arccos(Z)
    azm = ...
    raise NotImplementedError('TODO')
    ...