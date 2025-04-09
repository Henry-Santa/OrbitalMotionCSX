# define the sun, the earth, and the cube law earth
from stellarobject import StellarObject
from stellarObjectCubeLaw import StellarObjectCubeLaw
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

HOST = StellarObject(1.989E30, [0, 0], [0, 0], "SUN")
PLANETS = [
    StellarObjectCubeLaw(5.972E24, [149.597E9, 0], [0, 29784.8], "EARTH CUBE LAW"),
    StellarObject(5.972E24, [149.597E9, 0], [0, 29784.8], "EARTH"),
]
DT = 60 * 5  # Time step in seconds (5 minutes)
STEPSPERFRAME = 30

def animate(i):
    plt.cla()
    for _ in range(STEPSPERFRAME):
        for planet in PLANETS:
            planet.step(DT, [HOST])
    for planet in PLANETS:
        plt.plot(planet.pastPositions[-1][0], planet.pastPositions[-1][1], label=planet.name, marker='o')
        xs = [pos[0] for pos in planet.pastPositions]
        ys = [pos[1] for pos in planet.pastPositions]
        plt.plot(xs, ys, label=planet.name, alpha=0.5)
    plt.scatter([0], [0], color='yellow', marker='*', s=200, label='SUN')  # Sun at the center with star icon
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title('Solar System Simulation Cube Law')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.xlim(-2E11, 2E11)
    plt.ylim(-2E11, 2E11)


ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.show()
