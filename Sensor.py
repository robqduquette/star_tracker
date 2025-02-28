from util import Vector3
from PIL import Image
from typing import List, Tuple
import numpy as np
import transforms3d.euler as txe


def default_sensor():
    params = {
        'noise'         : 0.1,
        'fov'           : (60, 40), # horiz angle, vert angle
        'resolution'    : (120,80), # wide, tall
        'model'         : 'pinhole',
    }
    return params

class Sensor():
    def __init__(self, params = default_sensor()):
        self.params = default_sensor()
        for key in params.keys():
            self.params[ key ] = params[ key ]

        self.noise = self.params['noise']
        self.fov = self.params['fov']
        self.resolution = self.params['resolution']
        self.model = self.params['model']


    def gen_measurements(self, starmap, rpy: Vector3, adjust = 1.0):
        """ Generates measurements from the sensor
        inputs:
            starmap: a List(Tuple(Direction, Brightness))
            rpy: roll pitch yaw 'vector' of the sensor
        output:
            an image 'taken' by the sensor
        """
        # extract starmap data
        map_pos = np.array([star[0].asnp() for star in starmap]).T

        intensity = (np.array([star[1] for star in starmap]) + adjust) / (1.0 + adjust)

        # rotates points from the map frame to the camera frame
        rot_mtx = txe.euler2mat(rpy.x, rpy.y, rpy.z, axes='sxyz').T

        # transform stars to camera frame
        cam_pos = rot_mtx @ map_pos

        # calc camera position
        scale = 1 / cam_pos[0,:]
        u = cam_pos[1,:] * scale
        v = cam_pos[2,:] * scale

        # normalized positions on camera sensor
        width, height = np.tan(np.deg2rad(np.array(self.fov)) / 2)
        sensor_pos = np.array([u / width, v / height]) # horizontal pos, vertical pos

        # filter out any stars not in frame
        in_horiz= np.abs(sensor_pos[0,:]) <= 1.2
        in_vert = np.abs(sensor_pos[1,:]) <= 1.2
        in_front = cam_pos[0,:] > 0
        in_bounds = np.all(np.array([in_horiz, in_vert, in_front]), 0)

        intensity = intensity[in_bounds]
        sensor_pos = sensor_pos[:,in_bounds]
        sensor_pos *= -1 # invert axes for image generation

        # adjust to range of
        sensor_idx = (sensor_pos + 1) / 2 * np.array([self.resolution]).T

        # create the image
        img = np.zeros([*self.resolution]).T
        for star in range(len(sensor_idx[0])):
            x,y = sensor_idx[:,star].round(0)
            pos = sensor_idx[:,star].round(0)

            # verify position is in the image matrix
            if pos[0] < 0.0 or pos[0] >= self.resolution[0] or pos[1] < 0.0 or pos[1] >= self.resolution[1]:
                continue
            img[int(pos[1]),int(pos[0])] = intensity[star]

        # create the image
        image = Image.fromarray(np.uint8(img * 255))
        return image

