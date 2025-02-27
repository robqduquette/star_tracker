import matplotlib.pyplot as plt
import numpy as np
import sys
from util import Vector3, import_starmap
import WebMercator

args = sys.argv
if len(args) < 2:
    print("Invalid arguments. Usage: vis_map.py MAP_FILE.txt [plot_types]")
    exit()

plot_types = {'3d':False, 'latlon': False}

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

X = np.array([])
Y = np.array([])
Z = np.array([])
for star in starmap:
    pos = star[0]
    X = np.append(X, pos.x)
    Y = np.append(Y, pos.y)
    Z = np.append(Z, pos.z)

if plot_types['3d']:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


    # plot stars
    ax.scatter(X * (dist * 2),Y * (dist * 2),Z * (dist * 2), c='r')

    # draw earth
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v) * dist
    y = np.sin(u)*np.sin(v) * dist
    z = np.cos(v) * dist
    ax.plot_wireframe(x, y, z, color="b", alpha=0.5)

    fig.suptitle('3D starmap\n'+str(args[1]))
    lims = [-2.1 * dist, 2.1 * dist]
    ax.set_xlim(*lims)
    ax.set_ylim(*lims)
    ax.set_zlim(*lims)

    plt.show()

if plot_types['latlon']:
    # convert 3d coords to lat-lon
    r = np.sqrt(X**2 + Y**2 + Z**2)
    inc = np.arcsin(Z/r) * 180.0 / np.pi # angle from equator (x-y plane)
    azm = np.arctan2(Y,X) * 180.0 / np.pi # angle around z axis from x axis

    fig, ax = plt.subplots()
    plt.scatter(azm, inc)

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90,90)
    ax.set_xlabel('azimuth (deg)')
    ax.set_ylabel('inclination (deg)')
    ax.grid(True)
    fig.suptitle('Lat-Lon starmap\n'+str(args[1]))
    plt.show()
