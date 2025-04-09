from stellarobject import StellarObject
import util
G = 6.67430E-11  # Gravitational constant in m^3 kg^-1 s^-2
# define a cubelaw stellar object to extend stellar object
class StellarObjectCollide(StellarObject):
    @staticmethod
    def calc_radius(mass:float):
        # Assuming a spherical object, we can use the formula for the volume of a sphere to estimate the radius
        # Volume = (4/3) * π * r^3 => r = ((3 * Volume) / (4 * π))^(1/3)
        # For simplicity, let's assume a density of 5500 kg/m^3 (similar to Earth's average density)
        density = 5500
        volume = mass / density
        radius = ((3 * volume) / (4 * 3.14159))**(1/3)
        return radius

    def __init__(self, mass: float, position: list, velocity: list, name=None):
        self.radius = StellarObjectCollide.calc_radius(mass)
        super().__init__(mass, position, velocity, name)

    def __check_collision(self, obj: 'StellarObject'):
        distance = util.calcDistance(self.position, obj.position)
        if distance < self.radius + obj.radius:
            return True
        return False
    
    def check_collisions(self, objects: list):
        collisions = []
        for obj in objects:
            if obj == self or obj == None: continue
            if self.__check_collision(obj):
                collisions.append(obj)
        return collisions