from matplotlib import pyplot as plt
from stellarobject import StellarObject
import util

HOST = StellarObject(1.989E30, [0, 0], [0,0], "SUN")
# Set initial position at periapsis and a high velocity for high eccentricity
SATELITE = StellarObject(5.972E24, [75E9, 0], [0, 50000], "EARTH")  # High initial velocity
#SATELITE = StellarObject(5.972E24, [148.17E9, 0], [0, 29780], "EARTH")  # Correct initial velocity
DT = 60 * 60  # 1 hour
ITERSFORSWAP = 24*5*2*2
TOTALITERS = 24*320
areas = []
positionSets = []
area = 0

curr = 0

while True:
    curr += 1
    if curr == TOTALITERS: break
    if curr % ITERSFORSWAP == 0:
        areas.append(area)
        positionSets.append(SATELITE.pastPositions)
        SATELITE.pastPositions = [SATELITE.position]
        area = 0
    SATELITE.step(DT, [HOST])
    area += util.areaTriangle(SATELITE.position, SATELITE.pastPositions[-2], HOST.position)

print(areas)

for i in range(len(positionSets)):
    plt.text(positionSets[i][0][0], positionSets[i][0][1], f"area : {areas[i]:.2e}")
    xs = []
    ys = []
    for p in positionSets[i]:
        xs.append(p[0])
        xs.append(0)
        ys.append(p[1])
        ys.append(0)
    plt.plot(xs, ys)
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.title('Area checker high eccentricity')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
plt.show()
