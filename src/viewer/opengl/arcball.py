#-*- coding: utf-8 -*-
        
import copy

from utilities.myMath import *

class ArcBallT:
    """
    """
    
    def __init__(self, NewWidth, NewHeight):
        """
        """
        
        self.m_StVec = Vector3fT()
        self.m_EnVec = Vector3fT()
        self.m_AdjustWidth = 1.0
        self.m_AdjustHeight = 1.0
        self.setBounds(NewWidth, NewHeight)

    def __str__(self):
        """
        """
        
        str_rep = ""
        str_rep += "StVec = " + str(self.m_StVec)
        str_rep += "\nEnVec = " + str(self.m_EnVec)
        str_rep += "\n scale coords %f %f" %(self.m_AdjustWidth, self.m_AdjustHeight)
        return str_rep

    def setBounds(self, NewWidth, NewHeight):
        """
        """
        
        # Set new bounds
        assert(NewWidth > 1.0 and NewHeight > 1.0), "Invalid width or height for bounds."
        
        # Set adjustment factor for width/height
        self.m_AdjustWidth = 1.0 /((NewWidth - 1.0) * 0.5)
        self.m_AdjustHeight = 1.0 /((NewHeight - 1.0) * 0.5)

    def _mapToSphere(self, NewPt):
        """
        """
        
        # Given a new window coordinate, will modify NewVec in place
        X = 0
        Y = 1
        Z = 2

        NewVec = Vector3fT()
        # Copy paramter into temp point
        TempPt = copy.copy(NewPt)
        #print 'NewPt', NewPt, TempPt
        
        # Adjust point coords and scale down to range of [-1 ... 1]
        TempPt [X] =(NewPt [X] * self.m_AdjustWidth) - 1.0
        TempPt [Y] = 1.0 -(NewPt [Y] * self.m_AdjustHeight)
        
        # Compute the square of the length of the vector to the point
        # from the center
        length = sumDot( TempPt, TempPt)
        
        # If the point is mapped outside of the sphere...(length >
        # radius squared)
        if(length > 1.0):
            # Compute a normalizing factor(radius / sqrt(length))
            norm    = 1.0 / sqrt(length);

            # Return the "normalized" vector, a point on the sphere
            NewVec [X] = TempPt [X] * norm
            NewVec [Y] = TempPt [Y] * norm
            NewVec [Z] = 0.0

        # Else it's on the inside
        else:           
            # Return a vector to a point mapped inside the sphere
            # sqrt(radius squared - length)
            NewVec [X] = TempPt [X]
            NewVec [Y] = TempPt [Y]
            NewVec [Z] = sqrt(1.0 - length)

        return NewVec

    def click(self, NewPt):
        """
        Mouse down(Point2fT
        """
        
        self.m_StVec = self._mapToSphere(NewPt)

    def drag(self, NewPt):
        """
        Mouse drag, calculate rotation(Point2fT Quat4fT)
        drag(Point2fT mouse_coord) -> new_quaternion_rotation_vec
        """
        
        X = 0
        Y = 1
        Z = 2
        W = 3

        self.m_EnVec = self._mapToSphere(NewPt)

        # Compute the vector perpendicular to the begin and end
        # vectors Perp = Vector3fT()
        Perp = Vector3fCross(self.m_StVec, self.m_EnVec)

        NewRot = Quat4fT()
        
        # Compute the length of the perpendicular vector
        if(Vector3fLength(Perp) > Epsilon): # if its non-zero
            # We're ok, so return the perpendicular vector as the transform after all
            NewRot[X] = Perp[X]
            NewRot[Y] = Perp[Y]
            NewRot[Z] = Perp[Z]
            
            # In the quaternion values, w is cosine(theta / 2), where theta is rotation angle
            NewRot[W] = Vector3fDot(self.m_StVec, self.m_EnVec)
            
        else: # if its zero
            # The begin and end vectors coincide, so return a quaternion of zero matrix(no rotation)
            NewRot.X = NewRot.Y = NewRot.Z = NewRot.W = 0.0
            
        return NewRot
    
