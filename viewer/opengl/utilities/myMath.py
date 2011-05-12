#-*- coding: utf-8 -*-

from math import sqrt, pow, acos, pi
import numpy as Numeric

Epsilon = 1.0e-5

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step

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

class Vector():
    """
    """
    
    def __init__(self):
        pass

    def add(self, a, b):
        """ vector a plus vector b = resulting vector """
        result = Point(a.x + b.x, a.y + b.y, a.z + b.z)
        return result

    def subtract(self, a, b):
        """ vector a minus vector b = resulting vector vector """
        result = Point(a.x - b.x, a.y - b.y, a.z - b.z)
        return result

    def multiply(self, scalar, vector):
        """ multiply a vector by a scalar """
        result = [scalar * vector.x, scalar * vector.y, scalar * vector.z]
        return result

    def dotproduct(self, a, b):
        """ take the dot product of two vectors: a . b """
        result = a.x * b.x + a.y * b.y + a.z * b.z
        return result

    def crossproduct(self, a, b):
        """ take the cross product of two vectors: a X b """
        cross = Point(0,0,0)
        cross.x = a.y * b.z - a.z * b.y
        cross.y = a.z * b.x - a.x * b.z
        cross.z = a.x * b.y - a.y * b.x
        result = cross
        return result

    def mag(self, a):
        """ return the magnitude (length) of a vector """
        result = (a.x**2 + a.y**2 + a.z**2)**(0.5)
        return result

    def normalize(self, a):
        """ convert a vector to a unit vector (length of 1) """
        magnitude = self.mag(a)
        result = Point(a.x/magnitude, a.y/magnitude, a.z/magnitude)
        return result

    def angle(self, a, b):
        """ angle in degrees between two vectors """
        result = acos(self.dotproduct(a,b) / (self.mag(a)* self.mag(b))) # radians
        result = result * (180 / pi) # degrees
        return result
    

def sumDot(a, b):
    """
    """
    
    return Numeric.dot(a, b)

def Matrix4fT ():
    """
    """
    
    return Numeric.identity(4, 'f')

def Matrix3fT():
    """
    """
    
    return Numeric.identity(3, 'f')

def Quat4fT():
    """
    """
    
    return Numeric.zeros(4, 'f')

def Vector3fT():
    """
    """
    
    return Numeric.zeros (3, 'f')

def Point2fT(x = 0.0, y = 0.0):
    """
    """
    
    pt = Numeric.zeros (2, 'f')
    pt [0] = x
    pt [1] = y
    return pt

def Vector3fDot(u, v):
    """
    Dot product of two 3f vectors
    """
    
    dotprod = Numeric.dot (u,v)
    return dotprod

def Vector3fCross(u, v):
    """
    Cross product of two 3f vectors
    """
    
    X = 0
    Y = 1
    Z = 2
    cross = Numeric.zeros (3, 'f')
    cross [X] = (u[Y] * v[Z]) - (u[Z] * v[Y])
    cross [Y] = (u[Z] * v[X]) - (u[X] * v[Z])
    cross [Z] = (u[X] * v[Y]) - (u[Y] * v[X])
    
    return cross

def Vector3fLength(u):
    """
    """
    
    mag_squared = sumDot(u,u)
    mag = sqrt (mag_squared)
    return mag
    
def Matrix3fSetIdentity():
    """
    """
    
    return Numeric.identity (3, 'f')

def Matrix3fMulMatrix3f(matrix_a, matrix_b):
    """
    """
    
    return sumDot( matrix_a, matrix_b )

def Matrix4fSVD(NewObj):
    """
    """
    
    X = 0
    Y = 1
    Z = 2
    s = sqrt( 
        ((NewObj [X][X] * NewObj [X][X]) +(NewObj [X][Y] * NewObj [X][Y]) +(NewObj [X][Z] * NewObj [X][Z]) +
        (NewObj [Y][X] * NewObj [Y][X]) +(NewObj [Y][Y] * NewObj [Y][Y]) +(NewObj [Y][Z] * NewObj [Y][Z]) +
        (NewObj [Z][X] * NewObj [Z][X]) +(NewObj [Z][Y] * NewObj [Z][Y]) +(NewObj [Z][Z] * NewObj [Z][Z]) ) / 3.0 )
    return s

def Matrix4fSetRotationScaleFromMatrix3f(NewObj, three_by_three_matrix):
    """
    Modifies NewObj in-place by replacing its upper 3x3 portion from
    the passed in 3x3 matrix.
    
    NewObj = Matrix4fT()
    """
    
    NewObj [0:3,0:3] = three_by_three_matrix
    return NewObj

def Matrix4fSetRotationFromMatrix3f(NewObj, three_by_three_matrix):
    """
    Sets the rotational component(upper 3x3) of this matrix to the
    matrix values in the T precision Matrix3d argument; the other
    elements of this matrix are unchanged; a singular value
    decomposition is performed on this object's upper 3x3 matrix to
    factor out the scale, then this object's upper 3x3 matrix
    components are replaced by the passed rotation components, and
    then the scale is reapplied to the rotational components.
    
    @param three_by_three_matrix T precision 3x3 matrix
    """
    
    scale = Matrix4fSVD(NewObj)

    NewObj = Matrix4fSetRotationScaleFromMatrix3f(NewObj, three_by_three_matrix);
    scaled_NewObj = NewObj * scale # Matrix4fMulRotationScale(NewObj, scale);
    return scaled_NewObj

def Matrix3fSetRotationFromQuat4f(q1):
    """
    Converts the H quaternion q1 into a new equivalent 3x3 rotation
    matrix.
    """
    
    X = 0
    Y = 1
    Z = 2
    W = 3

    NewObj = Matrix3fT()
    n = sumDot(q1, q1)
    s = 0.0
    if(n > 0.0):
        s = 2.0 / n
    xs = q1 [X] * s;  ys = q1 [Y] * s;  zs = q1 [Z] * s
    wx = q1 [W] * xs; wy = q1 [W] * ys; wz = q1 [W] * zs
    xx = q1 [X] * xs; xy = q1 [X] * ys; xz = q1 [X] * zs
    yy = q1 [Y] * ys; yz = q1 [Y] * zs; zz = q1 [Z] * zs
    
    # This math all comes about by way of algebra, complex math, and trig identities.
    # See Lengyel pages 88-92
    NewObj [X][X] = 1.0 - (yy + zz);  NewObj [Y][X] = xy - wz;         NewObj [Z][X] = xz + wy;
    NewObj [X][Y] = xy + wz;          NewObj [Y][Y] = 1.0 -(xx + zz);  NewObj [Z][Y] = yz - wx;
    NewObj [X][Z] = xz - wy;          NewObj [Y][Z] = yz + wx;         NewObj [Z][Z] = 1.0 -(xx + yy)

    return NewObj
