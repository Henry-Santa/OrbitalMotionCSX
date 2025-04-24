from stellarobject import StellarObject
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutKeyboardFunc, glutMouseWheelFunc
from OpenGL.GLUT import *
import math
import random

colorMap = {
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0, 0.0, 1.0),
    'yellow': (1.0, 1.0, 0.0),
    'cyan': (0.0, 1.0, 1.0),
    'magenta': (1.0, 0.0, 1.0),
    'white': (1.0, 1.0, 1.0),
    'black': (0.0, 0.0, 0.0)
}


class ThreeDGrapher:
    def __init__(self, stellarObjects, colors, glows, trails=False):
        self.stellarObjects = stellarObjects
        self.colors = colors
        self.glows = glows
        self.trails = trails
        self.dt = 5 * 60 * 60 # 5 hours in seconds

    def plot_body(self, stellarObject : StellarObject, trail=False, color='green', glow=False):
        radius = max((stellarObject.mass ** (1/4)) * 1e3, 5e6)  # Ensure minimum radius for visibility
        glPushMatrix()
        x, y, z = stellarObject.position
        glTranslatef(x, y, z)
        c = colorMap[color]
        mat_ambient = [c[0]*0.3, c[1]*0.3, c[2]*0.3, 1.0]
        mat_diffuse = [c[0],    c[1],    c[2],    1.0]
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, radius, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()

    def plot_bodies(self):
        for i, stellarObject in enumerate(self.stellarObjects):
            self.plot_body(stellarObject, trail=self.trails, color=self.colors[i], glow=self.glows[i])

    def plot_axises(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3fv(colorMap['red'])
        glVertex3f(1e13, 0, 0)
        glVertex3f(-1e13, 0, 0)
        glColor3fv(colorMap['green'])
        glVertex3f(0, 1e13, 0)
        glVertex3f(0, -1e13, 0)
        glColor3fv(colorMap['blue'])
        glVertex3f(0, 0, 1e13)
        glVertex3f(0, 0, -1e13)
        glEnd()
        glEnable(GL_LIGHTING)

    def step_system(self):
        for stellarObject in self.stellarObjects:
            stellarObject.step(self.dt, self.stellarObjects)
    
    def init_gl(self):
        glClearColor(0, 0, 0, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 800.0/600.0, 1e9, 1e13)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)


        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)


        ambient = [0.2, 0.2, 0.2, 1.0]
        diffuse = [0.8, 0.8, 0.8, 1.0]
        position = [1.0, 1.0, 1.0, 0.0] 
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, position)

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(1600, 1200)
        glutCreateWindow(b"3D Astronomical Scale")
        self.init_gl()
        self.camera_controls()
        glutDisplayFunc(self.animate)
        glutIdleFunc(self.animate)
        glutMainLoop()

    def camera_controls(self):
        # scrolling the mouse zooms in and out at 1 percent of the distance to the origin
        # qaws keys move the camera around origin rotationally 
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.camera_distance = 1.496e11

        def keyboard(key, x, y):
            print(key)
            if key == b'q': 
                self.camera_angle_x += 5
            elif key == b'a':  
                self.camera_angle_x -= 5
            elif key == b'w':  
                self.camera_angle_y += 5
            elif key == b's': 
                self.camera_angle_y -= 5

        def mouse_wheel(button, direction, x, y):
            print(direction)
            if direction > 0:  # Scroll up
                self.camera_distance *= 0.99
            elif direction < 0:  # Scroll down
                self.camera_distance *= 1.01

        glutKeyboardFunc(keyboard)
        glutMouseWheelFunc(mouse_wheel)

        def update_camera():
            glLoadIdentity()
            gluLookAt(self.camera_distance * math.sin(math.radians(self.camera_angle_x)) * math.cos(math.radians(self.camera_angle_y)),
                      self.camera_distance * math.cos(math.radians(self.camera_angle_x)),
                      self.camera_distance * math.sin(math.radians(self.camera_angle_x)) * math.sin(math.radians(self.camera_angle_y)),
                      0.0, 0.0, 0.0,
                      0.0, 1.0, 0.0)

        self.update_camera = update_camera

        

    def animate(self):
        self.step_system()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.update_camera()
        self.plot_bodies()
        self.plot_axises()
        glutSwapBuffers()


def change_orbit_plane(stellarObject):
    angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    # Rotate position vector
    x, y, z = stellarObject.position
    stellarObject.position = [
        cos_angle * x - sin_angle * z,
        y,
        sin_angle * x + cos_angle * z
    ]

    # Rotate velocity vector
    vx, vy, vz = stellarObject.velocity
    stellarObject.velocity = [
        cos_angle * vx - sin_angle * vz,
        vy,
        sin_angle * vx + cos_angle * vz
    ]

if __name__ == "__main__":
    # Example usage
    mode = input("Enter mode (1 for default, 2 for random): ")
    if mode == '1':
        sun = StellarObject(1.989e30, [0, 0, 0], [0, 0, 0], name="Sun")
        earth = StellarObject(5.972e24, [1.496e11, 0, 0], [0, 29780, 0], name="Earth")
        stellarObjects = [sun, earth]
        colors = ['yellow', 'blue']
        glows = [True, False]
    elif mode == '2':
        # use the solar system as a base and randomly change the orbits of the planets
        HOST = StellarObject(1.989E30, [0, 0, 0], [0, 0, 0], "SUN")
        PLANETS = [
            StellarObject(3.285E23, [57.91E9, 0, 0], [0, 47400, 0], "MERCURY"),
            StellarObject(4.867E24, [108.2E9, 0, 0], [0, 35020, 0], "VENUS"),
            StellarObject(5.972E24, [149.597E9, 0, 0], [0, 29784.8, 0], "EARTH"),
            StellarObject(6.39E23, [227.94E9, 0, 0], [0, 24070, 0], "MARS"),
            StellarObject(1.898E27, [778.57E9, 0, 0], [0, 13070, 0], "JUPITER"),
            StellarObject(5.683E26, [1.434E12, 0, 0], [0, 9680, 0], "SATURN"),
            StellarObject(8.681E25, [2.871E12, 0, 0], [0, 6800, 0], "URANUS"),
            StellarObject(1.024E26, [4.495E12, 0, 0], [0, 5430, 0], "NEPTUNE"),
        ]
        stellarObjects = [HOST] + PLANETS
        colors = [
            'yellow', 'white', 'red', 'green', 'red', 'yellow', 'magenta', 'cyan', 'blue'
        ]
        glows = [True] + [False] * (len(PLANETS) + 1)
        for planet in PLANETS:
            change_orbit_plane(planet)
    if stellarObjects == None:
        raise ValueError("No stellar objects provided.")    

    grapher = ThreeDGrapher(stellarObjects, colors, glows)
    grapher.start()