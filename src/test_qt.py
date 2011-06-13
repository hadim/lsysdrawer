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
