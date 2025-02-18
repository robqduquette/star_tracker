import numpy as np

class ParticleFilter():
    def __init__(self, sensor_model, action_model, x_init = None, num_particles=5):
        self.num_particles = num_particles
        self.sensor_model = sensor_model
        self.action_model = action_model
        self.states = [x_init] * num_particles
        self.weights = [1 / num_particles] * num_particles
        self.estimate = x_init

    def update(self, observation, action = None):
        if action != None:
           self.resample()
        self.action(action)
        self.sensor(observation)
        self.estimate_state()


    def resample(self):
        for i in range(self.num_particles):
            ...


    def action(self, action):
        """ Applies the action model to each particle in the filter. """
        for i in range(self.num_particles):
            particle = self.states[i]
            particle = self.action_model(particle, action)
            self.states[i] = particle

    def sensor(self, observation):
        """ Updates the particle weights based on sensor measurements. """
        total_weight = 0.0

        # calculate weights using the sensor model
        for i in range(self.num_particles):
            particle = self.states[i]
            weight = self.sensor_model(particle, observation)
            self.weights[i] = weight
            total_weight += weight

        # normalize weights to sum to 1.0
        for i in range(self.num_particles):
            self.weights[i] /= total_weight

    def estimate_state(self):
        ...

    # return the esimated state
    def get_state(self):
        return self.estimate



p = ParticleFilter(1,2,(3,4))



