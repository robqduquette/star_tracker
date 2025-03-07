import numpy as np

class ParticleFilter():
    def __init__(self, sensor_model_fun, action_model_fun, x_init, estimate_fun = None, num_particles=50):
        """
        A particle filter algorithm for estimating the state of a dynamical system.

        Parameters:
            sensor_model(state, observation): a function handle that takes a state and observation and returns the 'score' of a particle.
            action_model(state, action): a function handle that updates the state of a system given an action.
            x_init: the initial state of the system.
            estimate_fun: the function used to estimate the state of the system from the list of particles. Defaults to an average of the particles states.
            num_particles: the number of particles in the filter

        Returns:
            A particle filter with the specified parameters.

        """
        self.num_particles = num_particles
        self.sensor_model = sensor_model_fun
        self.action_model = action_model_fun
        if estimate_fun == None:
            # weighted sum of states
            estimate_fun = lambda x: np.sum(np.array([self.weights]*len(x[0])).T * x,0)
        self.estimation = estimate_fun
        self.current_estimate = None

        # assign initial particles
        self.states = np.array([x_init] * num_particles)
        self.weights = [1 / num_particles] * num_particles

    def update(self, observation, action = None):
        """
        Updates the filter based on an observation and optionally an action

        parameters:
            observation: a measurement of the system to be used in the sensor model
            action: the known action applied to the system

        returns:
            the estimated state of the system
        """
        if action != None:
           self.resample()
        self.action(action)
        self.sensor(observation)
        return self.calc_estimate_state()


    def resample(self):
        """
        Resamples the particles based on their weights. Uses a low-variance resampling method.

        parameters:
            None

        returns:
            A resampled set of particles.

        """
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
            while u > cum_sum[i] and i < self.num_particles-1:
                i += 1
            new_particles.append(self.states[i])
        self.states = new_particles
        return new_particles


    def action(self, action):
        """
        Applies the action model to each particle in the filter.

        parameters:
            action: the applied action to the system.

        returns:
            None

        """
        for i in range(self.num_particles):
            particle = self.states[i]
            particle = self.action_model(particle, action)
            self.states[i] = particle


    def sensor(self, observation):
        """
        Updates the particle weights based on sensor measurements.

        parameters:
            observation: the measurement of the system to assess fit of each particle.

        returns:
            None
        """
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

    def calc_estimate_state(self):
        """
        Calculates the estimated state of the system.

        parameters:
            None

        returns:
            The current estimate of the system.
        """
        self.current_estimate = self.estimation(self.states)
        return self.current_estimate

    # return the estimated state
    def get_state(self):
        """
        Gets the currently estimated state from the filter. Generates the estimate if does not yet exzist

        parameters:
            None

        returns:
            the current state estimate
        """
        if self.current_estimate == None:
            self.calc_estimate_state()
        return self.current_estimate

    def get_particles(self):
        """
        Returns a numpy array of the states of each particle.

        parameters;
            None

        returns:
            a numpy array of particle states
        """
        return self.states

    def set_particles(self, particles, weights = None):
        """
        Sets the particles to a provided distribution of states and weights.

        parameters:
            particles: A numpy array of state variables that is the length of the set number of particles
            weights: the corresponding weights of the particles. If not set, this defaults to an even weight distribution.

        returns:
            None
        """
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
