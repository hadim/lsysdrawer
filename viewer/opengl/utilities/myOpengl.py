#-*- coding: utf-8 -*-

from math import pi, cos, sin
from myMath import *
from OpenGL.GL import *

import numpy as np

def genCylinder(radius, length, slices = 20, top_and_bottom = False):
    """
    """

    vertices = []

    # Cylinder "Cover"
    for i in xfrange(0, 360, (360.0 / slices)):
        a = i * pi / 180.0
        vertices.append(Point(radius * cos(a), radius * sin(a), 0.0))
        vertices.append(Point(radius * cos(a), radius * sin(a), length))

    vertices.append(Point(radius * cos(a), radius * sin(a), 0.0))
    vertices.append(Point(radius * cos(0), radius * sin(0), length))
    vertices.append(Point(radius * cos(0), radius * sin(0), 0.0))
    
    return vertices

def translation(points, vector):
    """
    """

    newPoints = []

    transMat = np.array( [ [ 1, 0, 0, vector.x ],
                           [ 0, 1, 0, vector.y ],
                           [ 0, 0, 1, vector.z ],
                           [ 0, 0, 0, 1        ], ], dtype = 'float32' )

    for p in points:
        mat = np.array([ [p.x], [p.y], [p.z], [1.0] ], dtype = 'float32') 
        
        newP = np.dot(transMat, mat)
        newPoints.append(Point(newP[0][0], newP[1][0], newP[2][0]))

    return newPoints

def rotation(points, vector, angle):
    """
    """

    newPoints = []
    a = pi * angle / 180.0
    vec = normalizeVector(vector)

    transMat = np.array( [ [ (vec.x * vec.x)*(1-cos(a)) + cos(a), (vec.x * vec.y)*(1-cos(a)) - vec.z * sin(a),
                             (vec.x * vec.z)*(1-cos(a)) + vec.y * sin(a), 0 ],
                           [ (vec.x * vec.y)*(1-cos(a)) + vec.z * sin(a), (vec.y * vec.y)*(1-cos(a)) + cos(a),
                             (vec.y * vec.z)*(1-cos(a)) - vec.x * sin(a), 0 ],
                           [ (vec.x * vec.z)*(1-cos(a)) - vec.y * sin(a), (vec.z * vec.y)*(1-cos(a)) + vec.x * sin(a),
                             (vec.z * vec.z)*(1-cos(a)) + cos(a), 0 ],
                           [ 0, 0, 0, 1        ], ] )

    for p in points:
        mat = np.array([ [p.x], [p.y], [p.z], [1.0] ])
        
        newP = np.dot(transMat, mat)
        newPoints.append(Point(newP[0][0], newP[1][0], newP[2][0]))

    return newPoints

def normalizeVector(vector):
    """
    """

    length = sqrt( vector.x ** 2.0 + vector.y ** 2.0 + vector.z ** 2.0 )

    if length != 0:
        return Point(vector.x / length, vector.y / length, vector.z / length)


def setupLights():
    """
    """
    
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    light_position = [10., -10., 200., 0.]
    light_ambient = [.2, .2, .2, 1.]
    light_diffuse = [.6, .6, .6, 1.]
    light_specular = [2., 2., 2., 0.]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glEnable(GL_LIGHT0)

    mat_ambient = [.2, .2, 1.0, 1.0]
    mat_diffuse = [.2, .8, 1.0, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    high_shininess = 3.

    mat_ambient_back = [.5, .2, .2, 1.0]
    mat_diffuse_back = [1.0, .2, .2, 1.0]

    glMaterialfv(GL_FRONT, GL_AMBIENT,   mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR,  mat_specular);
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess);

    glMaterialfv(GL_BACK, GL_AMBIENT,   mat_ambient_back);
    glMaterialfv(GL_BACK, GL_DIFFUSE,   mat_diffuse_back);
    glMaterialfv(GL_BACK, GL_SPECULAR,  mat_specular);
    glMaterialfv(GL_BACK, GL_SHININESS, high_shininess);
