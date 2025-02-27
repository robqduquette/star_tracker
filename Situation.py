from util import Vector3


class Situation():
    def __init__(self, starmap, orientations, soln, sensor):
        self.starmap = starmap
        self.stars = []
        self.intensity = []
        for star in starmap:
            self.stars.append(star[0])
            self.intensity.append(star[1])
        self.orientations = orientations
        self.soln = soln
        self.sensor = sensor

    def test_soln(self):
        for orientation in self.orientations:
            measurements = self.sensor.gen_measurements(self.starmap, orientation, self.sensor)
            soln_orient = soln(self.starmap, measurements)

