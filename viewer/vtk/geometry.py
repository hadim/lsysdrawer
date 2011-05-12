#-*- coding: utf-8 -*-

from math import *

class Point():
    """
    """

    def __init__(self, x, y, z):
        """
        """
        
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, p):
        """
        """

        return Point(self.x + p.x, self.y + p.y, self.z + p.z)

    def __str__(self):
        """
        """

        return str([self.x, self.y, self.z])


class Line():
    """
    """

    def __init__(self, p1, p2, color = (1,0,1), radius = 0.05):
        """
        """

        self.p1 = p1
        self.p2 = p2
        self.color = (color[0]/255.0, color[1]/255.0, color[2]/255.0)
        self.radius = radius

        self.vector = Point(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

        self.height = sqrt(self.vector.x ** 2 + self.vector.y ** 2 + self.vector.z ** 2)
        

    def getTransformation(self):
        """
        """

        # This is the default direction for the cylinders to face in OpenGL
        z = Point(0, 0, 1)

        # Get diff between two points you want cylinder along
        p = Point((self.p1.x - self.p2.x), (self.p1.y - self.p2.y),
                  (self.p1.z - self.p2.z))
    
        dist = sqrt( pow(self.p1.x - self.p2.x, 2) +
                     pow(self.p1.y - self.p2.y, 2) +
                     pow(self.p1.z - self.p2.z, 2) )

        # Get cross product (the axis of rotation)
        t = Point( (z.y*p.z - z.z*p.y),
                   (z.z*p.x - z.x*p.z),
                   (z.x*p.y - z.y*p.x) )
        
        # Get angle. length is magnitude of the vector
        angle = 180 / pi * acos(((z.x*p.x) +
                                 (z.y*p.y) +
                                 (z.z*p.z)) / dist)

        return self.p2, angle, t
    
        # glTranslatef(point.x, point.y, point.z);
        # glRotatef(angle, t.x, t.y, t.z);
        # glScalef(0.1, 0.1, 0.1);
    
        # GLUquadric* params;
        # params = gluNewQuadric();

        # gluQuadricOrientation(params, GLU_OUTSIDE);
        # gluCylinder(params, diam, diam, dist*10, BOUND_QUA, BOUND_QUA);
        
