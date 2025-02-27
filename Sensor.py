from util import Vector3
from PIL import Image
from typing import List, Tuple
import numpy as np


def default_sensor():
    params = {
        'noise'         : 0.1,
        'fov'           : (60, 40), # horiz angle, vert angle
        'resolution'    : (120,80), # wide, tall
        'model'         : 'pinhole',
    }
    return params

class Sensor():
    def __init__(self, params = None):
        self.params = default_sensor()
        for key in params.keys():
            self.params[ key ] = params[ key ]

        self.noise = params['noise']
        self.fov = params['fov']
        self.resolution = params['resolution']
        self.model = params['model']


def gen_measurements(starmap: List[Tuple[Vector3, float]], orientation: Vector3, sensor = default_sensor()) -> list:
    """ Generates measurements from the startracker """
    img = np.zeros([*sensor['resolution']])
    for star in starmap:

    print(sensor)
    return [0]