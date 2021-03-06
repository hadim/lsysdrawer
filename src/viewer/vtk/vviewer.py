#-*- coding: utf-8 -*-

# vviewer.py

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

from vtk.util import colors
import vtk

from viewer.viewer import *
from viewer.vtk.geometry import *

from graphml.GraphMLExporter import *

from utils import *

from math import *

class VViewer(Viewer):
    """
    """

    def __init__(self, lsystem, disp_info = True, timer = 1000):
        """
        """

        self.viewer_type = "3D VTK viewer"

        self.lsystem = lsystem
        self.ratio = float(self.lsystem.ratio)
        self.debug = False
        self.is_disp_info = disp_info
        self.iterIsOver = False
        self.idText = None
        self.dt = timer

        # Text to display
        self.toDisp = []

        self.renderTime = 50
        self.nbranches = 0
        self.tubeActors = []
        self.lines = []
        self.t = []

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

        # VTK init
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetSize(800, 600)
        self.renWin.SetWindowName("L-System : " + self.lsystem.name + " ( " + self.viewer_type + " )")

        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)

        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)

        # Branch initial parameters
        self.radius = self.lsystem.radius
        self.length = self.lsystem.width
        self.angle = self.lsystem.angle

    def execute(self, dt = 1000):
        """
        """

        self.rend = vtk.vtkRenderer()
        self.rend.SetBackground(0, 0, 0)

        self.renWin.AddRenderer(self.rend)

        self.iren.Initialize()

        self.iren.AddObserver("ModifiedEvent", self.update_text)

        if self.dt:
            self.iren.AddObserver("TimerEvent", self.advance)
            self.iren.CreateRepeatingTimer(self.dt)
        else:
            self.iren.AddObserver("KeyReleaseEvent", self.advance)

        self.rend.GetActiveCamera().SetPosition(0, 0, -4)
        
        self.disp_info()
        #self.draw_axis()
        self.advance()
        self.render_window()

        self.iren.Start()

    def render_window(self, widget = None, string = None):
        """
        """

        self.renWin.Render()

    def advance(self, widget = None, string = None):
        """
        """
        
        key = self.iren.GetKeySym()

        if key == 'space' and not self.iterIsOver:

            try:
                self.iterIsOver
                state = self.lsystem.next()

                i = int(self.lsystem.current_iter)
                print "Step n. %i" % i
                print self.lsystem.previous_state

                self.draw(state, i)
                self.disp_info()
                
                self.rend.ResetCamera()
                self.render_window()

            except StopIteration :
                self.iterIsOver = True
                self.disp_info()

        elif key == 'g':

            exporter = GraphMLExporter(self.t)
            exporter.write()

    def draw(self, state, step = -1):
        """
        """

        # Init curve
        self.vector = Point(self.length, 0, 0)
        self.pos = Point(0, 0, 0)

        drawed_state = ""

        # Compute lines to be drawing
        i = 0
        for s in state:

            letter = s['letter']

            symbol = self.lsystem.get_symbol(letter)
            drawed_state += symbol

            # Set color
            self.set_color(symbol)

            # Execute symbol
            self.execute_symbol(symbol, s['params'])

            progress(i*100.0/len(state))
            i += 1

        progress(-1)
        self.check_objects(drawed_state)

    def execute_symbol(self, symbol, params):
        """
        """

        if symbol in self.draw_forward:
            """
            Draw forward
            """

            if len(params) == 0:
                radius = self.radius
                vector = self.vector
            elif len(params) == 1:
                radius = float(params[0])
                vector = self.vector
            elif len(params) == 2:
                radius = float(params[0])
                vector = self.vector * float(params[1])

            self.draw_line( Line(p1 = self.pos,
                                 p2 = self.pos + vector,
                                 color = self.color,
                                 radius = radius) )

            self.t.append(Line(p1 = self.pos,
                               p2 = self.pos + vector))
            
            self.pos = self.pos + vector

        elif symbol in self.move_forward:
            """
            Move forward
            """

            self.pos = self.pos + self.vector
            self.line = Point(self.pos)


        elif symbol in self.rotation:
            """
            Rotation
            """

            if len(params) == 0:
                angle = self.angle
            elif len(params) == 1:
                angle = float(params[0])

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

    def draw_line(self, l):
        """
        """

        if l in self.lines:
            return
        self.lines.append(l)

        line = vtk.vtkLineSource()
        line.SetPoint1(l.p1.x, l.p1.y, l.p1.z)
        line.SetPoint2(l.p2.x, l.p2.y, l.p2.z)

        # lineMapper = vtk.vtkPolyDataMapper()
        # lineMapper.SetInputConnection(line.GetOutputPort())
        # lineActor = vtk.vtkActor()
        # lineActor.SetMapper(lineMapper)

        tubeFilter = vtk.vtkTubeFilter()
        tubeFilter.SetInputConnection(line.GetOutputPort())
        tubeFilter.SetRadius(l.radius)
        tubeFilter.SetNumberOfSides(10)
        tubeFilter.Update()

        tubeMapper = vtk.vtkPolyDataMapper()
        tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
        
        tubeActor = vtk.vtkActor()
        tubeActor.SetMapper(tubeMapper)
        tubeActor.GetProperty().SetColor(l.color[0], l.color[1], l.color[2])

        self.rend.AddActor(tubeActor)
        self.tubeActors.append(tubeActor)
        #self.rend.AddActor(lineActor)

    def disp_info(self):
        """
        """

        if not self.is_disp_info:
            return

        # Remove previous text object
        for t in self.toDisp:
            if t['object']:
                self.rend.RemoveActor(t['object'])

        self.toDisp = []

        # Display lsystem name
        self.disp_text("L-System : " + self.lsystem.name + " ( " + self.viewer_type + " )",
                       posx = 'left', posy = 'up')

        # Display current step number
        prefix = ""
        if self.iterIsOver:
            prefix = str(self.lsystem.iteration) + " ( lsystem loop is done ) "
        else:
            prefix = str(self.lsystem.current_iter)
            
        self.disp_text("Step : " + prefix,
                       posx = 'left', posy = 'down')

        # Display lsystem name
        self.disp_text("Number of branches : %d" % self.nbranches,
                       posx = 'right', posy = 'down')

    def update_text(self, widget = None, string = None):
        """
        """

        for t in self.toDisp:

            if t['object']:
                self.rend.RemoveActor(t['object'])

            if isinstance(t['posx'], str):

                size = self.renWin.GetSize()
                
                if t['posx'] == 'left':
                    posx = t['border']

                elif t['posx'] == 'right':
                    posx = size[0] - t['border'] - len(t['string']) * 10

                elif t['posx'] == 'center':
                    posx = size[0] / 2.0 - 65

                if t['posy'] == 'down':
                    posy = t['border']

                elif t['posy'] == 'up':
                    posy = size[1] - t['border']

                elif t['posy'] == 'middle':
                    posy = size[1] / 2.0

            t['object'] = vtk.vtkTextActor()
            t['object'].GetTextProperty().SetFontSize(t['size'])
            t['object'].SetInput(t['string'])
            t['object'].GetTextProperty().SetColor(t['color'][0], t['color'][1], t['color'][2])
            t['object'].SetPosition(posx, posy)

            self.rend.AddActor2D(t['object'])

    def disp_text(self, string, posx = 0, posy = 0, color = (1,1,1), size = 21, border = 35):
        """
        """

        text = { 'string' : string,
                 'posx' : posx,
                 'posy' : posy,
                 'color' : color,
                 'size' : size,
                 'border' : border,
                 'object' : None,
                 'id' : len(self.toDisp) }
        
        self.toDisp.append(text)
        self.update_text()

        return len(self.toDisp)

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

    def draw_axis(self):
        """
        """

        xaxis = vtk.vtkLineSource()
        xaxis.SetPoint1(0,0,0)
        xaxis.SetPoint2(1,0,0)

        xmapper = vtk.vtkPolyDataMapper()
        xmapper.SetInputConnection(xaxis.GetOutputPort())

        xactor = vtk.vtkActor()
        xactor.SetMapper(xmapper)
        xactor.GetProperty().SetColor(1,0,0)

        yaxis = vtk.vtkLineSource()
        yaxis.SetPoint1(0,0,0)
        yaxis.SetPoint2(0,1,0)

        ymapper = vtk.vtkPolyDataMapper()
        ymapper.SetInputConnection(yaxis.GetOutputPort())

        yactor = vtk.vtkActor()
        yactor.SetMapper(ymapper)
        yactor.GetProperty().SetColor(0,1,0)

        zaxis = vtk.vtkLineSource()
        zaxis.SetPoint1(0,0,0)
        zaxis.SetPoint2(0,0,1)

        zmapper = vtk.vtkPolyDataMapper()
        zmapper.SetInputConnection(zaxis.GetOutputPort())

        zactor = vtk.vtkActor()
        zactor.SetMapper(zmapper)
        zactor.GetProperty().SetColor(0,0,1)

        self.rend.AddActor(xactor)
        self.rend.AddActor(yactor)
        self.rend.AddActor(zactor)

    def pause(self):
        """
        """

        pass

    def set_color(self, s):
        """
        """

        if s == 'F':
            self.color = (255, 255, 255)
        elif s == 'B':
            self.color = (0, 0, 255)
        elif s == 'G':
            self.color = (0, 255, 0)
        elif s == 'R':
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)

    def check_objects(self, state):
        """
        """

        self.nbranches = len(self.tubeActors)

        
