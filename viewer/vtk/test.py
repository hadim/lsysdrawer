#-*- coding: utf-8 -*-

# This example demonstrates the use of a single streamline and the
# tube filter to create a streamtube.

import vtk
from vtk.util.misc import vtkGetDataRoot
from vtk.util.colors import *
VTK_DATA_ROOT = vtkGetDataRoot()

# We read a data file the is a CFD analysis of airflow in an office
# (with ventilation and a burning cigarette). We force an update so
# that we can query the output for its length, i.e., the length of the
# diagonal of the bounding box. This is useful for normalizing the
# data.
reader = vtk.vtkStructuredGridReader()
reader.SetFileName(VTK_DATA_ROOT + "/Data/office.binary.vtk")
reader.Update()

length = reader.GetOutput().GetLength()

maxVelocity =reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
maxTime = 35.0*length/maxVelocity

points = vtk.vtkPoints()
for i in range(5):
    points.InsertNextPoint(i, i, i)

data = vtk.vtkPolyData()
data.SetPoints(points);

# Now we will generate a single streamline in the data. We select the
# integration order to use (RungeKutta order 4) and associate it with
# the streamer. The start position is the position in world space
# where we want to begin streamline integration; and we integrate in
# both directions. The step length is the length of the line segments
# that make up the streamline (i.e., related to display). The
# IntegrationStepLength specifies the integration step length as a
# fraction of the cell size that the streamline is in.
streamer = vtk.vtkStreamLine()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(0.1, 2.1, 0.5)
streamer.SetMaximumPropagationTime(500)
streamer.SetStepLength(0.5)
streamer.SetIntegrationStepLength(0.05)
streamer.SetIntegrationDirectionToIntegrateBothDirections()

mapStreamLine = vtk.vtkPolyDataMapper()
mapStreamLine.SetInputConnection(streamer.GetOutputPort())
streamLineActor = vtk.vtkActor()
streamLineActor.SetMapper(mapStreamLine)

# The tube is wrapped around the generated streamline. By varying the
# radius by the inverse of vector magnitude, we are creating a tube
# whose radius is proportional to mass flux (in incompressible flow).
streamTube = vtk.vtkTubeFilter()
streamTube.SetInputConnection(streamer.GetOutputPort())
streamTube.SetRadius(0.02)
streamTube.SetNumberOfSides(12)
streamTube.SetVaryRadiusToVaryRadiusByVector()
mapStreamTube = vtk.vtkPolyDataMapper()
mapStreamTube.SetInputConnection(streamTube.GetOutputPort())
mapStreamTube.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())
streamTubeActor = vtk.vtkActor()
streamTubeActor.SetMapper(mapStreamTube)
streamTubeActor.GetProperty().BackfaceCullingOn()

# Now create the usual graphics stuff.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

#ren.AddActor(streamTubeActor)
ren.AddActor(streamLineActor)

ren.SetBackground(slate_grey)

# Here we specify a particular view.
aCamera = vtk.vtkCamera()
aCamera.SetClippingRange(0.726079, 36.3039)
aCamera.SetFocalPoint(2.43584, 2.15046, 1.11104)
aCamera.SetPosition(-4.76183, -10.4426, 3.17203)
aCamera.SetViewUp(0.0511273, 0.132773, 0.989827)
aCamera.SetViewAngle(18.604)
aCamera.Zoom(1.2)

ren.SetActiveCamera(aCamera)
renWin.SetSize(500, 300)

iren.Initialize()
renWin.Render()
iren.Start()
