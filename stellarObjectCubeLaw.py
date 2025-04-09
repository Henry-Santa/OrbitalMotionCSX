from stellarobject import StellarObject
import util
G = 6.67430E-11  # Gravitational constant in m^3 kg^-1 s^-2
# define a cubelaw stellar object to extend stellar object
class StellarObjectCubeLaw(StellarObject):
    def __init__(self, mass: float, position: list, velocity: list, name=None):
        super().__init__(mass, position, velocity, name)

    def calculate_force(self, obj: 'StellarObject'):
        if obj == self: return [0, 0]
        distance = util.calcDistance(self.position, obj.position)
        forceTotal = G * self.mass * obj.mass / (distance**3)  # Cubic law
        force = util.multiplyVec(util.normalizeVec(util.subVec(obj.position, self.position)), forceTotal)
        return force