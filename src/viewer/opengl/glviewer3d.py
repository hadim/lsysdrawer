#-*- coding: utf-8 -*-

from visual import *
from viewer.viewer import *

from gl_drawer import *
from utilities.myMath import *

class GLViewer3D(Viewer):
    """
    """

    def __init__(self, lsystem):
        """
        """

        self.viewer_type = "3D viewer using OpenGL"

        self.lsystem = lsystem
        self.ratio = float(self.lsystem.ratio)
        self.debug = False

        self.init()

    def init(self):
        """
        """

        # List of line to draw
        self.lines = []

        # Visual initialisation
        self.drawer = GlDrawer(title = "L-System name : " + self.lsystem.name + " ( " + self.viewer_type + " )")
        self.drawer.cylinders = self.lines

        # Symbol behaviour initialisation
        self.draw_forward = ['F', 'B', 'G', 'R']
        self.move_forward = ['M']
        self.rotation = ['+', '-', '&', '^', '<', '>', '|']
        self.push_pop = ['[', ']']
        self.do_nothing = ['X']

        # Init heap / stack to remember position
        self.saved_pos = []
        self.saved_vector = []
        
        self.line = Point(0, 0, 0)
        #self.color = color.white

        # Branch initial parameters
        self.radius = 0.05
        self.length = 2
        self.angle = self.lsystem.angle

    def draw(self, state):
        """
        """

        # Init curve
        self.vector = Point(1, 0, 0)
        self.pos = Point(0, 0, 0)

        # Draw curve
        for s in state:

            # Set color
            self.set_color(s)

            symbol = self.lsystem.get_symbol(s)
            self.execute_symbol(symbol)

        self.drawer.initVBO()
        self.drawer.show()

    def execute_symbol(self, symbol):
        """
        """

        if symbol in self.draw_forward:
            """
            Draw forward
            """

            #self.pos = self.pos + self.vector
            self.lines.append( [self.pos, self.pos + self.vector])
            self.pos = self.pos + self.vector
            #self.line.append( pos = self.pos, color = self.color )

        if symbol in self.move_forward:
            """
            Move forward
            """

            self.pos = self.pos + self.vector
            self.line = Point(self.pos)

        elif symbol in self.rotation:
            """
            Rotation
            """

            angle = self.angle

            if symbol == '+':
                x, y, z = self.rotate(self.vector, angle, 'U')
                self.vector = Point(x, y, z)

            elif symbol == '-':
                x, y, z = self.rotate(self.vector, -angle, 'U')
                self.vector = Point(x, y, z)

            elif symbol == '&':
                x, y, z = self.rotate(self.vector, angle, 'L')
                self.vector = Point(x, y, z)

            elif symbol == '^':
                x, y, z = self.rotate(self.vector, -angle, 'L')
                self.vector = Point(x, y, z)

            elif symbol == '<':
                x, y, z = self.rotate(self.vector, angle, 'H')
                self.vector = Point(x, y, z)

            elif symbol == '>':
                x, y, z = self.rotate(self.vector, -angle, 'H')
                self.vector = Point(x, y, z)

            elif symbol == '|':
                x, y, z = self.rotate(self.vector, 180, 'U')
                self.vector = Point(x, y, z)

        elif symbol in self.push_pop:
            """
            Save current position or restore it
            """

            if symbol == '[':
                self.saved_pos.append(self.pos)
                self.saved_vector.append(self.vector)
                
            elif symbol == ']':
                self.pos = self.saved_pos.pop()
                self.vector = self.saved_vector.pop()

                self.line = self.pos

        elif symbol in self.do_nothing:
            """
            Do nothing
            """

            pass


    def draw_axis(self):
        """
        TODO : draw axis in gl_drawer.py
        """

        pass

    def rotate(self, vec, degree, mode = 'U'):
        """
        """

        alpha = radians(degree)

        if mode == 'U':
            
            x = vec.x * cos(alpha)      + vec.y * sin(alpha) + vec.z * 0
            y = vec.x * sin(alpha) * -1 + vec.y * cos(alpha) + vec.z * 0
            z = vec.x * 0               + vec.y * 0          + vec.z * 1
            
        elif mode == 'L':
            
            x = vec.x * cos(alpha)      + vec.y * 0          + vec.z * -1 * sin(alpha)
            y = vec.x * 0               + vec.y * 1          + vec.z * 0
            z = vec.x * sin(alpha)      + vec.y * 0          + vec.z * cos(alpha)
        
        elif mode == 'H':
            
            x = vec.x * 1               + vec.y * 0          + vec.z * 0
            y = vec.x * 0               + vec.y * cos(alpha) + vec.z * -1 * sin(alpha)
            z = vec.x * 0               + vec.y * sin(alpha) + vec.z * cos(alpha)

        return x, y, z

    def pause(self):
        """
        """

        self.scene.mouse.getclick()

    def set_color(self, s):
        """
        """
        pass
        # if s == 'F':
        #     self.color = color.white
        # elif s == 'B':
        #     self.color = color.blue
        # elif s == 'G':
        #     self.color = color.green
        # elif s == 'R':
        #     self.color = color.red
        # else:
        #     self.color = color.white
        
