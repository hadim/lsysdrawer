#-*- coding: utf-8 -*-

from lsystem.lsystem import *
from viewer.viewer import *

from viewer.visual.viewer2d import *
from viewer.visual.viewer3d import *
from viewer.visual.kidneyviewer import *
from viewer.opengl.glviewer3d import *
from viewer.vtk.vviewer import *

import sys

if __name__ == '__main__':

    fname = 'data/dragon.ls'
    
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    lsys = Lsystem(fname)
    print lsys

    viewer = Viewer(lsys)

    #visualViewer = KidneyViewer(lsys)
    #visualViewer = Viewer2D(lsys)
    visualViewer = Viewer3D(lsys, True)
    #visualViewer = GLViewer3D(lsys)
    
    for s in lsys:
        
        print "Step n. %i" % (int(lsys.current_iter))
        viewer.draw(s)

    visualViewer.draw(s)
    
