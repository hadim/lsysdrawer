#-*- coding: utf-8 -*-

# kidneyviewer.py

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

from visual import *
from viewer.visual.viewer2d import *

import math as m

class KidneyViewer(Viewer2D):
    """
    """

    def __init__(self, lsystem):
        """
        """

        self.viewer_type = "kidney viewer"

        self.lsystem = lsystem
        self.alpha = float(self.lsystem.alpha)
        self.debug = False

        self.init()

    def init(self):
        """
        """

        # Symbol behaviour initialisation
        self.draw_forward = ['F']
        self.move_forward = ['M']
        self.rotation = ['+', '-']
        self.push_pop = ['[', ']']
        self.do_nothing = ['X']

        # Init heap / stack to remember position
        self.saved_pos = []
        self.saved_vector = []
        

        # Visual initialisation
        self.scene = display(title = "L-System name : " + self.lsystem.name + " ( " + self.viewer_type + " )",
                             x = 0, y = 0, width = 1024, height = 768,
                             center = (0,0,0), background = (0,0,0),
                             autocenter = True)
        rate(50)
        self.line = curve( pos = (0,0) )
        self.color = color.green
        #self.draw_axis()

        # Branch initial parameters
        self.radius = 0.1
        self.length = 2
        self.angle = self.lsystem.angle
        
        self.saved_radius = [self.radius]
        self.saved_length = [self.length]
        self.saved_angleRatio = [1]
        self.parents = {}

        # Calculate ratios
        self.computeRadius()
        self.computeLength()
        self.computeAngle()
        self.d1 = True

    def draw(self, state):
        """
        """
    
        # Remove previous curve
        self.line.visible = False

        # Init curve
        self.vector = vector(1, 0)
        self.pos = vector(0,0)
        self.line = curve( pos = (0,0),
                           color = self.color,
                           radius = self.radius)

        # Debug stuff
        self.sphere = None

        # Draw curve
        for s in state:

            symbol = self.lsystem.get_symbol(s)
            self.execute_symbol(symbol)

            ## Debug info
            if self.debug:
                if self.sphere:
                    self.sphere.visible = False
                self.sphere = sphere(pos = self.pos, color = color.red, radius = 0.25)

    def execute_symbol(self, symbol):
        """
        """

        if symbol in self.draw_forward:
            """
            Draw forward
            """

            self.old = self.pos
            self.pos = self.pos + self.vector * self.saved_length[-1]

            self.line = curve( pos = [self.old, self.pos],
                               color = self.color,
                               radius = self.saved_radius[-1] )

        if symbol in self.move_forward:
            """
            Move forward
            """

            self.pos = self.pos + self.vector * self.saved_length[-1]
            self.line = curve( pos = self.pos,
                               color = self.color,
                               radius = self.radius)

        elif symbol in self.rotation:
            """
            Rotation
            """

            angle = float(symbol + str(self.angle))

            x, y = self.rotate(self.vector, radians(angle) * self.saved_angleRatio[-1])
            self.vector = vector(x, y)

        elif symbol in self.push_pop:
            """
            Save current position or restore it
            """

            if symbol == '[':
                self.saved_pos.append(self.pos)
                self.saved_vector.append(self.vector)

                if self.d1:
                    self.saved_length.append(self.saved_length[-1] * self.lengthRatio1)
                    self.saved_radius.append(self.saved_radius[-1] * self.radiusRatio1)
                    self.saved_angleRatio.append(self.angleRatio1)
                else:
                    self.saved_length.append(self.saved_length[-1] * self.lengthRatio2)
                    self.saved_radius.append(self.saved_radius[-1] * self.radiusRatio2)
                    self.saved_angleRatio.append(self.angleRatio2)
                    
                
            elif symbol == ']':

                self.pos = self.saved_pos.pop()
                self.vector = self.saved_vector.pop()
                self.saved_radius.pop()
                self.saved_length.pop()
                self.saved_angleRatio.pop()

                self.d1 = not self.d1

                self.line = curve( pos = self.pos,
                                   color = color.green,
                                   radius = self.radius)

        elif symbol in self.do_nothing:
            """
            Do nothing
            """

            pass

    def computeRadius(self):
        """
        """

        self.radiusRatio1 = 1.0 / m.pow( (1.0 + m.pow(self.alpha, 3.0)), 1.0/3)
        self.radiusRatio2 = self.alpha / m.pow( (1.0 + m.pow(self.alpha, 3.0)), 1.0/3)

    def computeLength(self):
        """
        """

        self.lengthRatio1 = self.radiusRatio1
        self.lengthRatio2 = self.radiusRatio2

    def computeAngle(self):
        """
        """

        a = self.alpha

        self.angleRatio1 = m.acos(( (1 + a**3.0)**(4/3.0) + 1 - a**4.0 ) / ( 2.0 * ( 1 + a ** 3.0) ** (2/3.0)))
        self.angleRatio2 = m.acos(( (1 + a**3.0)**(4/3.0) + a**4.0 - 1 ) / ( 2.0 * a**2 * ( 1 + a ** 3.0) ** (2/3.0)))

    def rotate(self, vec, radian):
        """
        """

        x = vec.x * cos(radian) - vec.y * sin(radian)
        y = vec.x * sin(radian) + vec.y * cos(radian)

        return x, y
