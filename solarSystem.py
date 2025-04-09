import matplotlib.pyplot as plt
from stellarobject import StellarObject

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

DT = 60 * 5  # Time step in seconds (5 minutes)
STEPS = 365 * 24 * 12  # 1 year

# Initialize data storage for plotting
positions = {planet.name: ([], []) for planet in PLANETS}

# Simulation loop
for _ in range(STEPS):
    for planet in PLANETS:
        planet.step(DT, [HOST] + PLANETS)
        positions[planet.name][0].append(planet.position[0])
        positions[planet.name][1].append(planet.position[1])

# Plotting the results
plt.figure(figsize=(10, 10))
for planet in PLANETS:
    plt.plot(positions[planet.name][0], positions[planet.name][1], label=planet.name)

plt.scatter([0], [0], color='yellow', marker='*', s=200, label='SUN')  # Sun at the center with star icon
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.title('Solar System Simulation')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
