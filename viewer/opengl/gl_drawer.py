#-*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

from numpy import *

import sys
from time import sleep

from arcball import *
from utilities.myOpengl import *

g_Transform = Matrix4fT()
g_LastRot = Matrix3fT()
g_ThisRot = Matrix3fT()

class GlDrawer():
    """
    """

    window = None
    g_isDragging = False
    g_quadratic = None

    def __init__(self, argv = [], title = "", width = 640, height = 480, frameRate = 75):
        """
        """

        # Init some variable
        self.width = width
        self.height = height
        self.frameRate = frameRate

        self.zoom = 5.0
        self.dzoom = 1

        self.title = title

        # List of [Point(), Point] which need to be draw
        self.cylinders = []

        # List of vertices for all cylinders
        self.vertCylinders = []

        # Init camera
        self.g_ArcBall = ArcBallT(self.width, self.height)

        self.initWindow()
        self.initCallbackFunction()
        self.initGL()

    def show(self):
        """
        Start Event Processing Engine
        """
        
        glutMainLoop()

    def initWindow(self):
        """
        """

        # Pass arguments to init
        glutInit(sys.argv)

        # Select type of Display mode:   
        # Double buffer 
        # RGBA color
        # Alpha components supported 
        # Depth buffer
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    
        # get a 640 x 480 window 
        glutInitWindowSize(640, 480)
    
        # the window starts at the upper left corner of the screen 
        glutInitWindowPosition(0, 0)
    
        # Okay, like the C version we retain the window id to use when
        # closing, but for those of you new to Python, remember this
        # assignment would make the variable local and not global if
        # it weren't for the global declaration at the start of main.
        window = glutCreateWindow(self.title)

    def initGL(self):
        """
        We call this right after our OpenGL window is created.
        """

        glShadeModel(GL_SMOOTH)                             # Enables Smooth Color Shading
        glClearColor(0.0, 0.0, 0.0, 1.0)					# This Will Clear The Background Color To Black
        glClearDepth(1.0)									# Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LEQUAL)								# The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)								# Enables Depth Testing
        glShadeModel(GL_FLAT)								# Select Flat Shading(Nice Definition Of Objects)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) 	# Really Nice Perspective Calculations

        #setupLights()

    def initCallbackFunction(self):
        """
        """

        # Register the drawing function with glut, BUT in Python land,
        # at least using PyOpenGL, we need to set the function pointer
        # and invoke a function to actually register the callback,
        # otherwise it would be very much like the C version of the
        # code.
        glutDisplayFunc(self.draw)

        # Uncomment this line to get full screen.
        #glutFullScreen()

        # When we are doing nothing, redraw the scene.
        glutIdleFunc(self.draw)

        # Register the function called when our window is resized.
        glutReshapeFunc(self.resizeGLScene)

        # Register the function called when the keyboard is pressed.
        glutKeyboardFunc(self.keyPressed)

        # GLUT When mouse buttons are clicked in window
        glutMouseFunc(self.uponClick)

        # GLUT When the mouse mvoes
        glutMotionFunc(self.uponDrag)

    def controlFPS(self):
        """
        """

        sleep( 1 / float( self.frameRate ) )
        glutPostRedisplay()

    def resizeGLScene(self, width, height):
        """
        Reshape The Window When It's Moved Or Resized
        """

        self.width = width
        self.height = height

        # Prevent A Divide By Zero If The Window Is Too Small
        if height == 0:                     
            height = 1

        # Reset The Current Viewport And Perspective Transformation
        glViewport(0, 0, self.width, self.height)

        # Select The Projection Matrix
        glMatrixMode(GL_PROJECTION)

        # Reset The Projection Matrix
        glLoadIdentity()
        
        # Field of view, aspect ratio, near and far. This will squash
        # and stretch our objects as the window is resized.  Note that
        # the near clip plane is 1(hither) and the far plane is 1000
        #(yon)
        gluPerspective(45.0, float(self.width)/float(self.height), 0.001, 1000.0)

        # Select The Modelview Matrix
        glMatrixMode(GL_MODELVIEW)
        
        # Reset The Modelview Matrix
        glLoadIdentity()

        # Update mouse bounds for arcball
        self.g_ArcBall.setBounds(self.width, self.height) 

    def keyPressed(self, *args):
        """
        """

        # If escape is pressed, kill everything.
        key = args [0]
        if key == ESCAPE:
            #gluDeleteQuadric(g_quadratic)
            sys.exit()


    def uponDrag(self, cursor_x, cursor_y):
        """
        Mouse cursor is moving

        Glut calls this function(when mouse button is down) and pases
		the mouse cursor postion in window coords as the mouse moves.
        """
        
        global g_isDragging, g_LastRot, g_Transform, g_ThisRot

        if(g_isDragging):
            mouse_pt = Point2fT(cursor_x, cursor_y)

            # Update End Vector And Get Rotation As Quaternion
            ThisQuat = self.g_ArcBall.drag(mouse_pt)

            # Convert Quaternion Into Matrix3fT
            g_ThisRot = Matrix3fSetRotationFromQuat4f(ThisQuat)
            # Use correct Linear Algebra matrix multiplication C = A * B

            # Accumulate Last Rotation Into This One
            g_ThisRot = Matrix3fMulMatrix3f(g_LastRot, g_ThisRot)

            # Set Our Final Transform's Rotation From This One
            g_Transform = Matrix4fSetRotationFromMatrix3f(g_Transform, g_ThisRot)


    def uponClick(self, button, button_state, cursor_x, cursor_y):
        """
        Mouse button clicked.
        
		Glut calls this function when a mouse button is clicked or
		released.
        """
        
        global g_isDragging, g_LastRot, g_Transform, g_ThisRot

        g_isDragging = False
        if(button == GLUT_RIGHT_BUTTON and button_state == GLUT_UP):
            # Right button click
            g_LastRot = Matrix3fSetIdentity()			 # Reset Rotation
            g_ThisRot = Matrix3fSetIdentity()			 # Reset Rotation
            g_Transform = Matrix4fSetRotationFromMatrix3f(g_Transform, g_ThisRot)	# Reset Rotation
            
        elif(button == GLUT_LEFT_BUTTON and button_state == GLUT_UP):
            # Left button released
            g_LastRot = copy.copy(g_ThisRot)        # Set Last Static Rotation To Last Dynamic One
            
        elif(button == GLUT_LEFT_BUTTON and button_state == GLUT_DOWN):
            # Left button clicked down
            g_LastRot = copy.copy(g_ThisRot)        # Set Last Static Rotation To Last Dynamic One
            g_isDragging = True	                     # Prepare For Dragging
            mouse_pt = Point2fT(cursor_x, cursor_y)
            self.g_ArcBall.click(mouse_pt)		     # Update Start Vector And Prepare For Dragging

        # Zoom out
        elif button == 3:
            if self.zoom < 100:
                self.zoom += self.dzoom
        # Zoom int
        elif button == 4:
            if self.zoom > 0.11:
                self.zoom -= self.dzoom

    def initVBO(self):
        """
        """

        self.allVertices = []
        self.nbVerticesByCylinders = []

        for l in self.cylinders:
            vertices = self.createCylinder(l[0], l[1])
            for v in vertices:
                self.allVertices += [ v.x, v.y, v.z ]
            self.nbVerticesByCylinders.append(len(vertices))
        
        self.allVertices = array(self.allVertices, dtype = float32)

        self.pos_vbo = vbo.VBO(data = self.allVertices,
                               usage = GL_DYNAMIC_DRAW,
                               target = GL_ARRAY_BUFFER)
        self.pos_vbo.bind()

    def draw(self):
        """
        """

        # Select The Modelview Matrix
        glMatrixMode(GL_MODELVIEW)

        self.controlFPS()

        # Clear Screen And Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset The Current Modelview Matrix
        glLoadIdentity()
        glTranslatef(0, 0.0, -self.zoom)
        glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 0.0, 0])
        glMultMatrixf(g_Transform)

        glPushMatrix()
        
        # Do the magic with VBO
        self.pos_vbo.bind()
        glVertexPointer(3, GL_FLOAT, 0, self.pos_vbo)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self.allVertices) / 3)
        glDisableClientState(GL_VERTEX_ARRAY)

        glPopMatrix()
        
        # Flush The GL Rendering Pipeline
        glFlush()
        glutSwapBuffers()

    def createCylinder(self, p1, p2, radius = 0.2, slices = 20):
        """
        Create cylinder
        """

        ## Calculate translation and rotation

        # This is the default direction for the cylinders to face in OpenGL
        z = Point(0.0, 0.0, 1.0)

        # Get diff between two points you want cylinder along
        p = Point((p1.x - p2.x), (p1.y - p2.y), (p1.z - p2.z))
    
        length = sqrt( pow(p1.x - p2.x, 2) +
                       pow(p1.y - p2.y, 2) +
                       pow(p1.z - p2.z, 2) )

        # Get cross product (the axis of rotation)
        t = Point( (z.y * p.z - z.z * p.y),
                   (z.z * p.x - z.x * p.z),
                   (z.x * p.y - z.y * p.x) )
    
        # Get angle. length is magnitude of the vector
        angle = 180.0 / pi * acos(((z.x * p.x) +
                                   (z.y * p.y) +
                                   (z.z * p.z)) / length)

        ## Generate cylinder's vertices
        vertices = genCylinder(radius, length, slices)

        ## Apply translation and rotation
        vertices = translation(vertices, p2)
        vertices = rotation(vertices, t, angle)

        return vertices
    

if __name__ == '__main__':

    drawer = GlDrawer()

    drawer.cylinders = [ [ Point(0.000000, 0.000000, 0.000000),  Point(1.000000, 0.000000, 0.000000)],
                         [ Point(1.000000, 0.000000, 0.000000),  Point(0.000000, 0.000000, 0.000000)],
                         [ Point(3.000000, 3.000000, 0.000000),  Point(4.000000, 4.000000, 0.000000)],
                         [ Point(3.000000, 0.000000, 0.000000),  Point(4.000000, 0.000000, 0.000000)],
                         [ Point(4.000000, 0.000000, 0.000000),  Point(5.000000, 0.000000, 0.000000)],
                         [ Point(5.000000, 0.000000, 0.000000),  Point(6.000000, 0.000000, 0.000000)],
                         [ Point(6.000000, 0.000000, 0.000000),  Point(7.000000, 0.000000, 0.000000)],
                         [ Point(7.000000, 0.000000, 0.000000),  Point(8.000000, 0.000000, 0.000000)],
                         [ Point(8.000000, 0.000000, 0.000000),  Point(9.000000, 0.000000, 0.000000)],
                         [ Point(9.000000, 0.000000, 0.000000),  Point(10.000000, 0.000000, 0.000000)],
                         [ Point(10.000000, 0.000000, 0.000000),  Point(11.000000, 0.000000, 0.000000)],
                         [ Point(11.000000, 0.000000, 0.000000),  Point(12.000000, 0.000000, 0.000000)],
                         [ Point(12.000000, 0.000000, 0.000000),  Point(13.000000, 0.000000, 0.000000)],
                         [ Point(13.000000, 0.000000, 0.000000),  Point(14.000000, 0.000000, 0.000000)],
                         [ Point(14.000000, 0.000000, 0.000000),  Point(15.000000, 0.000000, 0.000000)],
                         [ Point(15.000000, 0.000000, 0.000000),  Point(16.000000, 0.000000, 0.000000)],
                         [ Point(16.000000, 0.000000, 0.000000),  Point(16.821394, 0.422618, 0.383022)],
                         [ Point(16.821394, 0.422618, 0.383022),  Point(17.642788, 0.845237, 0.766044)],
                         [ Point(17.642788, 0.845237, 0.766044),  Point(18.464181, 1.267855, 1.149067)],
                         [ Point(18.464181, 1.267855, 1.149067),  Point(19.285575, 1.690473, 1.532089)] ]
    
    drawer.initVBO()
    
    drawer.show()
    
