from stellarObjectCollidable import StellarObjectCollide
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from stellarobject import StellarObject
from random import randint, uniform
import util

NUMBER_OF_PLANETS = 30  # Number of planets to generate
DT = 60 * 5  # Time step in seconds (5 minutes)
STEPSPERFRAME = 30  # Number of steps to simulate per frame
USE_HOST = True
DELETE_PLANET_BOUNDARY = 1E11  # Distance from the host at which to delete the planet
REGENERATE_PLANETS = True # If True, planets will be regenerated if they go out of bounds
USE_NAMES = False

NAMES = open("names.txt", "r").readlines()

def random_planet():
    # make a random planet with a mass between earth and jupiter and a random position and a random velocity ~ to earths velocity
    mass = uniform(5.972E24, 1.898E27)  # Mass between Earth and Jupiter
    position = [uniform(-1E11, 1E11), uniform(-1E11, 1E11)]  # Random position within a range
    velocity = [uniform(-1E4, 1E4), uniform(-1E4, 1E4)]  # Random velocity within a range
    
    return StellarObjectCollide(mass, position, velocity, NAMES[randint(0, len(NAMES)-1)].strip() if USE_NAMES else None)  # Random name from the list
PLANETS = [random_planet() for _ in range(NUMBER_OF_PLANETS)]  # Generate random planets
# Host = the sun
HOST = StellarObject(1.989E30, [0, 0], [0, 0], "SUN")

def handle_collisions(PLANETS):
    for i in range(len(PLANETS)):
        if PLANETS[i] is None: continue
        collisions = PLANETS[i].check_collisions(PLANETS)
        for obj in collisions:
            index = PLANETS.index(obj)

            PLANETS[i].mass += PLANETS[index].mass * 0.94
            PLANETS[i].velocity = [(PLANETS[i].mass * PLANETS[i].velocity[0] + PLANETS[index].mass * PLANETS[index].velocity[0]) / (PLANETS[i].mass + PLANETS[index].mass),
                                   (PLANETS[i].mass * PLANETS[i].velocity[1] + PLANETS[index].mass * PLANETS[index].velocity[1]) / (PLANETS[i].mass + PLANETS[index].mass)]

            PLANETS[i].radius = StellarObjectCollide.calc_radius(PLANETS[i].mass)
            PLANETS[index] = None

def step_planets(PLANETS, DT):
    for planet in PLANETS:
        if planet is None: continue
        planets = [HOST] + PLANETS if USE_HOST else PLANETS
        planet.step(DT, [PLANET for PLANET in planets if PLANET is not None and PLANET != planet])
        if util.calcDistance(planet.position, [0, 0]) > DELETE_PLANET_BOUNDARY:
            PLANETS[PLANETS.index(planet)] = random_planet() if REGENERATE_PLANETS else None
    handle_collisions(PLANETS)

def graph_planets(PLANETS):
    plt.cla()
    for planet in PLANETS:
        if planet is None: continue
        
        plt.plot(planet.pastPositions[-1][0], planet.pastPositions[-1][1], label=planet.name, marker='o', markersize=planet.radius * 1E-7)
        xs = [pos[0] for pos in planet.pastPositions]
        ys = [pos[1] for pos in planet.pastPositions]
        plt.plot(xs[max(-len(xs), -330):-1], ys[max(-len(xs), -330):-1], alpha=0.5)
    if USE_HOST:
        plt.scatter([0], [0], color='yellow', marker='*', s=200, label='SUN')

    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title('Random Planet Collisions Respawn')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')

def animate(i):
    for _ in range(STEPSPERFRAME):
        step_planets(PLANETS, DT)
    graph_planets(PLANETS)

ani = FuncAnimation(plt.gcf(), animate, interval=10, cache_frame_data=False )
plt.show()