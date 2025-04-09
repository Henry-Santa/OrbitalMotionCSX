import matplotlib.pyplot as plt
from stellarobject import StellarObject
from matplotlib.animation import FuncAnimation

# Define the Sun and planets with their initial conditions
HOST = StellarObject(1.989E30, [0, 0], [0, 0], "SUN")
PLANETS = [
    StellarObject(3.285E23, [57.91E9, 0], [0, 47400], "MERCURY"),
    StellarObject(4.867E24, [108.2E9, 0], [0, 35020], "VENUS"),
    StellarObject(5.972E24, [149.597E9, 0], [0, 29784.8], "EARTH"),
    StellarObject(6.39E23, [227.94E9, 0], [0, 24070], "MARS"),
    StellarObject(1.898E27, [778.57E9, 0], [0, 13070], "JUPITER"),
    StellarObject(5.683E26, [1.434E12, 0], [0, 9680], "SATURN"),
    StellarObject(8.681E25, [2.871E12, 0], [0, 6800], "URANUS"),
    StellarObject(1.024E26, [4.495E12, 0], [0, 5430], "NEPTUNE"),
]

# Add Earth's moon
MOON = StellarObject(7.342E22, [PLANETS[2].position[0] + 384400000, 0], [0, 29780 + 1022], "MOON")  # Moon's initial position and velocity relative to Earth
PLANETS.append(MOON)

DT = 60 * 5  # 1 hour 
STEPS = 365 * 24 * 12  # 1 year

# Initialize data storage for plotting
positions = {planet.name: ([], []) for planet in PLANETS}
# Enable interactive zooming and panning
plt.gca().set_aspect('equal', adjustable='datalim')
plt.gca().set_navigate(True)
# Simulation loop
def animate(i):
    for i in range(100):
        for planet in PLANETS:
            planet.step(DT, [HOST] + PLANETS)
            positions[planet.name][0].append(planet.position[0])
            positions[planet.name][1].append(planet.position[1])
    plt.cla()

    # Plotting the results
    #plt.figure(figsize=(10, 10))
    for planet in PLANETS:
        plt.plot(positions[planet.name][0], positions[planet.name][1], label=planet.name)
        if planet == MOON:
            plt.plot(planet.position[0], planet.position[1], label=planet.name, marker='o', markersize=2) 
        else:
            plt.plot(planet.position[0], planet.position[1], label=planet.name, marker='o', markersize=5) 

    plt.scatter([0], [0], color='yellow', marker='*', s=200, label='SUN')  # Sun at the center with star icon
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title('Solar System Simulation')
    # legend goes top right
    plt.legend(loc='upper right')
    #plt.grid(True)
    
    #plt.axes().set_aspect('equal', adjustable='box')
    
    # makes axes log

for planet in PLANETS:
    plt.plot(planet.position[0], planet.position[1], label=planet.name, marker='o', markersize=5)


ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.show()
