import util

G = 6.67430E-11

class StellarObject:
    def __init__(self, mass : float, position : list, velocity : list, name = None):
        self.name = name
        self.mass = mass
        self.position = position
        self.pastPositions = [position]
        self.velocity = velocity
        self.pastVelocities = [velocity]
        self.acceleration = [0, 0]
        self.force = [0, 0]
    
    def step(self, dt, objects : list):
        for obj in objects:
            if obj != self:
                self.force = util.addVec(self.force, self.calculate_force(obj))
        self.acceleration = util.multiplyVec(self.force, 1/self.mass)
        self.velocity = util.addVec(self.velocity, util.multiplyVec(self.acceleration, dt))  # Correctly update velocity
        self.position = util.addVec(self.position, util.multiplyVec(self.velocity, dt))
        self.pastPositions.append(self.position)
        self.pastVelocities.append(self.velocity)
        self.force = [0, 0]

    def calculate_force(self, obj : 'StellarObject'):
        distance = util.calcDistance(self.position, obj.position)
        forceTotal = G*self.mass*obj.mass/(distance**2)
        force = util.multiplyVec(util.normalizeVec(util.subVec(obj.position, self.position)), forceTotal)
        return force

