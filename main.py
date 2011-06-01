#-*- coding: utf-8 -*-

from lsystem.lsystem import *
from viewer.viewer import *

from viewer.vtk.vviewer import *

import sys

if __name__ == '__main__':

    fname = 'data/dragon.ls'
    
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    lsys = Lsystem(fname)
    print lsys

    viewer = Viewer(lsys)
    visualViewer = VViewer(lsys, timer = None)
    visualViewer.execute()
    
