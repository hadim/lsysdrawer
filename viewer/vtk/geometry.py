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

    def __eq__(self, p):
        """
        """

        if p.x == self.x and p.y == self.y and p.z == self.z:
            return True
        else:
            return False


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
        

    def __eq__(self, line):
        """
        """

        if (line.p1 == self.p1 and line.p2 == self.p2):

            if line.radius == self.radius:

                if self.color[0] == line.color[0] and \
                   self.color[1] == line.color[1] and \
                   self.color[2] == line.color[2]:

                    return True

        return False
