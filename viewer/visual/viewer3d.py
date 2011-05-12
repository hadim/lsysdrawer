#-*- coding: utf-8 -*-

from visual import *
from visual.controls import *

from viewer.viewer import *

class Viewer3D(Viewer):
    """
    """

    def __init__(self, lsystem, disp_info = True):
        """
        """

        self.viewer_type = "3D viewer"

        self.lsystem = lsystem
        self.ratio = float(self.lsystem.ratio)
        self.debug = False
        self.stepPanel = None
        self.titlePanel = None
        self.is_disp_info = disp_info

        self.init()

    def init(self):
        """
        """

        # Symbol behaviour initialisation
        self.draw_forward = ['F', 'B', 'G', 'R']
        self.move_forward = ['M']
        self.rotation = ['+', '-', '&', '^', '<', '>', '|']
        self.push_pop = ['[', ']']
        self.do_nothing = ['X']

        # Init heap / stack to remember position
        self.saved_pos = []
        self.saved_vector = []
        

        # Visual initialisation
        self.scene = display(title = "L-System name : " + self.lsystem.name + " ( " + self.viewer_type + " )",
                             x = 0,
                             y = 0,
                             width = 1024,
                             height = 768,
                             show_rendertime = True,
                             center = (0,0,0),
                             background = (0,0,0),
                             autocenter = True)
        rate(50)
        self.line = curve( pos = (0, 0, 0) )
        self.color = color.white
        self.tree = frame()
        self.draw_axis()

        # Branch initial parameters
        self.radius = 0.05
        self.length = 2
        self.angle = self.lsystem.angle

    def draw(self, state, step = -1):
        """
        """
    
        # Remove previous curve
        self.line.visible = False

        # Init curve
        self.vector = vector(1, 0, 0)
        self.pos = vector(0, 0, 0)
        self.line = curve( pos = (0, 0, 0),
                           color = self.color,
                           radius = self.radius,
                           frame = self.tree)

        # Debug stuff
        self.sphere = None

        # Draw curve
        for s in state:

            symbol = self.lsystem.get_symbol(s)

            # Set color
            self.set_color(symbol)
            
            self.execute_symbol(symbol)

            ## Debug info
            if self.debug:
                if self.sphere:
                    self.sphere.visible = False
                self.sphere = sphere(pos = self.pos, color = color.red, radius = 0.25)

        self.disp_info()
        self.pause()

    def execute_symbol(self, symbol):
        """
        """

        if symbol in self.draw_forward:
            """
            Draw forward
            """

            #self.pos = self.pos + self.vector
            self.line = curve( pos = [self.pos, self.pos + self.vector],
                               color = self.color,
                               radius = self.radius,
                               frame = self.tree)
            
            self.pos = self.pos + self.vector
            #self.line.append( pos = self.pos, color = self.color )

        if symbol in self.move_forward:
            """
            Move forward
            """

            self.pos = self.pos + self.vector
            self.line = curve( pos = self.pos,
                               color = self.color,
                               radius = self.radius,
                               frame = self.tree)

        elif symbol in self.rotation:
            """
            Rotation
            """

            angle = self.angle

            if symbol == '+':
                x, y, z = self.rotate(self.vector, angle, 'U')
                self.vector = vector(x, y, z)

            elif symbol == '-':
                x, y, z = self.rotate(self.vector, -angle, 'U')
                self.vector = vector(x, y, z)

            elif symbol == '&':
                x, y, z = self.rotate(self.vector, angle, 'L')
                self.vector = vector(x, y, z)

            elif symbol == '^':
                x, y, z = self.rotate(self.vector, -angle, 'L')
                self.vector = vector(x, y, z)

            elif symbol == '<':
                x, y, z = self.rotate(self.vector, angle, 'H')
                self.vector = vector(x, y, z)

            elif symbol == '>':
                x, y, z = self.rotate(self.vector, -angle, 'H')
                self.vector = vector(x, y, z)

            elif symbol == '|':
                x, y, z = self.rotate(self.vector, 180, 'U')
                self.vector = vector(x, y, z)

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

                self.line = curve( pos = self.pos,
                                   color = self.color,
                                   radius = self.radius)

        elif symbol in self.do_nothing:
            """
            Do nothing
            """

            pass

    def disp_info(self):
        """
        """

        if self.is_disp_info:
            step = int(self.lsystem.current_iter)
            self.disp_step(step)
            self.disp_title()
            
        else:
            if self.stepPanel:
               self.stepPanel.visible = None
               
            if self.titlePanel:
               self.titlePanel.visible = None 

    def disp_title(self):
        """
        """

        if self.titlePanel:
            self.titlePanel.visible = False

        self.titlePanel = label(pos = self.stepPanel.pos,
                                text = "L-System name : " + self.lsystem.name + " ( " + self.viewer_type + " )",
                                xoffset = 0,
                                yoffset = 40,
                                line = False)

    def disp_step(self, step = -1):
        """
        """

        if self.stepPanel:
            self.stepPanel.visible = False
            
        #dist = ((self.lsystem.current_iter + 2.0) ** 2.0) / 4.5
        dist = 8

        tmpPos = vector(self.scene.center.x,
                        self.scene.center.y + dist,
                        self.scene.center.z)

        self.stepPanel = label(pos = tmpPos, text = "Step : " + str(step),
                               xoffset = 5, yoffset = 5, height = 10,
                               border = 6, font = 'sans', line = False)

    def draw_axis(self):
        """
        """

        radius = 0.001
        step = 1

        arrow(pos=(0,0,0), axis=(step,0,0), color = color.red, shaftwidth=radius)
        arrow(pos=(0,0,0), axis=(0,step,0), color = color.green, shaftwidth=radius)
        arrow(pos=(0,0,0), axis=(0,0,step), color = color.blue, shaftwidth=radius)

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

        if not self.scene.mouse.clicked:
            self.scene.mouse.getclick()

    def set_color(self, s):
        """
        """

        if s == 'F':
            self.color = color.white
        elif s == 'B':
            self.color = color.blue
        elif s == 'G':
            self.color = color.green
        elif s == 'R':
            self.color = color.red
        else:
            self.color = color.white
            
