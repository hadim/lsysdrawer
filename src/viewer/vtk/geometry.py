#-*- coding: utf-8 -*-

# geometry.py

# Copyright (c) 2011, see AUTHORS
# All rights reserved.

# This file is part of Lsysdrawer.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the ProfileExtractor nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

    def __mul__(self, f):
        """
        """

        f = float(f)
        return Point(self.x * f, self.y * f, self.z * f)

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

        if ((line.p1 == self.p1 and line.p2 == self.p2) or (line.p1 == self.p2 and line.p2 == self.p1)):

            if line.radius == self.radius:

                if self.color[0] == line.color[0] and \
                   self.color[1] == line.color[1] and \
                   self.color[2] == line.color[2]:

                    return True

        return False
