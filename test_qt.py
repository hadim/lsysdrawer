#-*- coding: utf-8 -*-

import sys

try:
    from PySide import QtCore, QtGui
except ImportError:
    print "Error : This script need Qt libraries for Python."
    print "Please install PySide: http://www.pyside.org/"

from vtk.qt4.QVTKRenderWindowInteractor import *

if __name__ == "__main__":
    
    # app = QtGui.QApplication(sys.argv)
    # main_app = MainWindow()
    # main_app.show()
    # sys.exit(app.exec_())

    # every QT app needs an app
    app = QtGui.QApplication(['QVTKRenderWindowInteractor'])

    # create the widget
    widget = QVTKRenderWindowInteractor()
    widget.Initialize()
    widget.Start()
    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtk.vtkConeSource()
    cone.SetResolution(8)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the widget
    widget.show()
    # start event processing
    app.exec_()
