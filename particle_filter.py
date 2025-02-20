import numpy as np

class ParticleFilter():
    def __init__(self, sensor_model_fun, action_model_fun, x_init, estimate_fun = None, num_particles=5):
        self.num_particles = num_particles
        self.sensor_model = sensor_model_fun
        self.action_model = action_model_fun
        if estimate_fun == None:
            estimate_fun = lambda x: np.sum(x,0) / len(x)
        self.estimation = estimate_fun
        self.current_estimate = None

        # assign initial particles
        self.states = np.array([x_init] * num_particles)
        self.weights = [1 / num_particles] * num_particles

    def update(self, observation, action = None):
        if action != None:
           self.resample()
        self.action(action)
        self.sensor(observation)
        return self.estimate_state()


    def resample(self):
        """ Resamples the particles based on their weights. """
        new_particles = []
        # generate cumulative sum of weights
        cum_sum = np.cumsum(self.weights)
        total = cum_sum[-1]

        # ensure weights sm to 1.0
        if total != 1.0:
            cum_sum /= total

        # random offset
        r = np.random.uniform(0, 1/self.num_particles)

        i = 0
        for m in range(self.num_particles):
            u = r + m / self.num_particles
            while u > cum_sum[i]:
                i += 1
            new_particles.append(self.states[i])
        self.states = new_particles
        return new_particles


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
        """ Returns the estimated state of the system. """
        self.current_estimate = self.estimation(self.states)
        return self.current_estimate

    # return the esimated state
    def get_state(self):
        if self.current_estimate == None:
            self.estimate_state()
        return self.current_estimate

    def get_particles(self):
        return self.states

    def set_particles(self, particles, weights = None):
        # validate inputs
        if len(particles) != self.num_particles:
            raise ValueError("len(particles) must be equal to set number of particles = "+str(self.num_particles) + ". len(particles) = " + str(len(particles)))
        if weights != None and len(weights) != self.num_particles:
            raise ValueError("len(weights) must be equal to set number of particles = "+str(self.num_particles) + ". len(weights) = " + str(len(weights)))

        self.states = particles
        if weights != None:
            self.weights = weights
        else:
            self.weights = [1/ len(particles)] * len(particles)
