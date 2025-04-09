from matplotlib import pyplot as plt
from stellarobject import StellarObject
from matplotlib.animation import FuncAnimation
import util

HOST = StellarObject(1.989E30, [0, 0], [0,0], "SUN")
# Set initial position at periapsis and a high velocity for high eccentricity
SATELITE = StellarObject(5.972E24, [75E9, 0], [0, 50000], "EARTH")  # High initial velocity
#SATELITE = StellarObject(5.972E24, [148.17E9, 0], [0, 29780], "EARTH")  # Correct initial velocity
DT = 60 * 60  # 1 hour
TOTALITERS = 24*365
areas = []
positionSets = []
area = 0
curr = 0

while SATELITE.position[1] >= 0:
    curr += 1
    SATELITE.step(DT, [HOST])


for i in range(curr):
    SATELITE.step(DT, [HOST])

average_x = sum([p[0] * util.magnitude(v) for p, v in zip(SATELITE.pastPositions,SATELITE.pastVelocities)]) / (len(SATELITE.pastPositions)* sum([util.magnitude(v) for v in SATELITE.pastVelocities])/ len(SATELITE.pastVelocities))
print(average_x)

xs = [p[0] for p in SATELITE.pastPositions]
ys = [p[1] for p in SATELITE.pastPositions]

distances = [util.calcDistance([2*average_x, 0], p) + util.calcDistance([0,0], p) for p in SATELITE.pastPositions]
# get the average of the distances
average_distance = sum(distances) / len(distances)
# get the differences between the average distance and the distances
differences = [d - average_distance for d in distances]
# get the average of the absolute value of the differences
average_difference = sum([abs(d) for d in differences]) / len(differences)
print(average_difference)
print(average_difference/average_distance)
def animate(i):
    # Begins by clearing all previous information from the graph
    plt.cla()

    plt.plot(xs[i % len(xs)], ys[i % len(xs)], 'bo')

    plt.plot([0, xs[i % len(xs)], 2 * average_x], [0, ys[i % len(xs)], 0], 'black')

    plt.text(xs[i % len(xs)], ys[i % len(xs)], f"Distance : {distances[i % len(xs)]:.2e}")

    plt.plot(xs, ys)

    # plot the average x position as the center of orbit
    plt.plot([average_x], [0], 'ro')
    # plot the sun
    plt.plot([0], [0], 'yo')
    # plot the other focus of the orbit which is on the other side of the average x than the sun
    plt.plot([2*average_x], [0], 'go')

    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title('Ellipse checker high eccentricity')

    plt.grid(True)
    plt.axis('equal')
    plt.legend(['Planet','Distances','Orbit', 'Center of Orbit', 'Sun', 'Other Focus'], loc='upper left')

ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.show()


