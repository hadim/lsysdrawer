#-*- coding: utf-8 -*-

# test_qt.py

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

import sys

try:
    from PySide import QtCore, QtGui
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print "Error : This script need Qt libraries for Python."
    print "Please install PySide: http://www.pyside.org/"

from vtk.qt4.QVTKRenderWindowInteractor import *

from ui.ui_mainwindow import *

class MainWindow(QtGui.QWidget, Ui_MainWindow):
    """
    """
    
    def __init__(self, parent = None):
        """
        """
        
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Lsysdrawer - L-System 3D viewer")

        # create the widget
        self.widget = QVTKRenderWindowInteractor()
        self.widget.Initialize()
        self.widget.Start()
        
        ren = vtk.vtkRenderer()
        self.widget.GetRenderWindow().AddRenderer(ren)
    
        cone = vtk.vtkConeSource()
        cone.SetResolution(8)

        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInput(cone.GetOutput())
        
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)

        ren.AddActor(coneActor)

        self.splitter.insertWidget(0, self.widget)

if __name__ == "__main__":

    # every QT app needs an app
    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    window = MainWindow()

    window.show()
    #window.widget.Start()
    sys.exit(app.exec_())
