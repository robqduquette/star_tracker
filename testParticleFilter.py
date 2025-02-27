from particle_filter import ParticleFilter
import numpy as np
import random
import matplotlib.pyplot as plt

# basic pendulum example system
gl = 9.81 / 9.87 # g/l
gl_est = 9.81 / 10
damping = 0.2

def pendulum_action(x, u, dt):
    """action model for pendulum particle filter"""
    theta = x[0]
    thetadot = x[1]
    u += u * np.random.normal(0,0.05) # introduce gaussian noise to actuator
    dx = np.array([thetadot, u - gl * 0.9 * np.sin(theta)]) * dt
    x = x + dx + np.random.normal(0,0.2,np.size(x))
    return x

def pendulum_sensor(particle_state, obs):
    """returns the likeliness of a state given an observation"""
    theta, thetadot = particle_state
    return 1.0 / (np.abs(obs - theta) + 0.01)

def pendulum_model(x,u):
    """ 'real' pendulum model """
    theta = x[0]
    thetadot = x[1]
    dx = np.array([thetadot, u - gl * np.sin(theta) - damping * thetadot])
    return dx

# noise & disturbance parameters
p_disturbance = 0.2 # disturbances 20% of the time
mag_dist = 5 # max magnitude of disturbances
sensor_noise = 0.05  # 5% error in readings
actuator_noise = 0.1 # 10% error in actuator output

# simulation setup
x_init = np.array([2,0.0]) # theta, thetadot
u = np.array([0] * 10 + [0.1] * 25 + [0.0] * 300)
dt = 0.1
x = np.zeros([2,len(u)])
x[:,0] = x_init
time = np.array([t*dt for t in range(len(u))])

# make pfs with varying num particles
n_particles = [25,100,250]
x_hat = np.zeros([len(n_particles), 2, len(u)])
pfs = []
for n in n_particles:
    pf = ParticleFilter(pendulum_sensor, lambda x,u: pendulum_action(x,u,dt), x_init, None, n)
    pfs.append(pf)

# simulate
for step in range(len(u)-1):
    # extract the state estimate from the particle filters
    for i in range(len(pfs)):
        pf = pfs[i]
        x_hat[i, :, step] = pf.calc_estimate_state()

    t = step * dt

    # generate a random disturbance to the pendulum sometimes
    dist = 0
    if np.random.random() > p_disturbance:
        dist = (np.random.random() - 0.5) * mag_dist

    # update the pendulum's state
    x[:,step+1] = x[:,step] + dt * pendulum_model(x[:,step], u[step] + dist)

    # feed noisy position information into the particle filters
    for pf in pfs:
        state = x[0,step] * np.random.normal(1,sensor_noise) # 5% error in measurement
        pf.update(state, u[step] * np.random.normal(1,actuator_noise))

# final filter estimate
for i in range(len(pfs)):
    pf = pfs[i]
    x_hat[i, :, -1] = pf.calc_estimate_state()

# plot
fig, ax = plt.subplots()
plt.plot(time,x[0,:],c='r',linewidth=2)
names = ['theta']
for i in range(len(pfs)):
    pf = pfs[i]
    plt.plot(time,x_hat[i,0,:], '--')
    names.append("n=" + str(n_particles[i]))
plt.plot(time,x[0,:],c='r',linewidth=2)
ax.set_xlabel('t (s)')
ax.set_ylabel('theta (rad)')
ax.legend(names)
ax.set_ylim([-4,4])
plt.grid(True)
fig.suptitle("Particle Filter tracking pendulum with disturbances and noise")
plt.show()