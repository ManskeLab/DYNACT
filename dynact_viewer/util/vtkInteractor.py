#----------------------------------------------------- 
# mainWindow.py
#
# Created by:   Michael Kuczynski
# Created on:   03-02-2020
#
# Description: Custom VTK interactor for DYNACT Viewer.
#----------------------------------------------------- 

import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        # Initialize observers
        self.AddObserver('KeyPressEvent', self.KeyPressEvent)

        self.volumes = []
        self.currentVolume = 0
        self.volCB = None
        self.timer = None
        self.log = None

    def setParameters(self, _volumes, _currentVolume, _volCB, _timer, _log):
        self.volumes = _volumes
        self.currentVolume = _currentVolume
        self.volCB = _volCB
        self.timer = _timer
        self.log = _log

    def KeyPressEvent(self, obj, event):
        self.iren = self.GetInteractor()

        keyPressed = self.iren.GetKeySym()

        if keyPressed == 'z' :
            # Get cursor position
            x, y = self.iren.GetEventPosition()

            nextActor = self.volumes[self.currentVolume].volActor # Get the next actor

            # Determine the cursor position
            cellPicker = vtk.vtkCellPicker()
            cellPicker.PickFromListOn()
            cellPicker.AddPickList(nextActor)
            cellPicker.SetTolerance(0.00001)
            cellPicker.Pick(x, y, 0, self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer())

            points = cellPicker.GetPickedPositions()
            numPoints = points.GetNumberOfPoints()
            if numPoints < 1:
                return
            i, j, k = points.GetPoint(0)

            # Look for an existing point near the cursor position and remove it if it exists
            count = 0
            for point in self.volumes[self.currentVolume].tPoints :
                # Get the center of the point actor
                posn = point.GetCenter()

                if round(i, 0) == round(posn[0], 0) or ( round(i, 0)-1 ) == round(posn[0], 0) or ( round(i, 0)+1 ) == round(posn[0], 0) :
                    if round(j, 0) == round(posn[1], 0) or ( round(j, 0)-1 ) == round(posn[1], 0) or ( round(j, 0)+1 ) == round(posn[1], 0) :
                        self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(self.volumes[self.currentVolume].tPoints[count])
                        self.iren.Render()

                        del self.volumes[self.currentVolume].tPoints[count]
                count = count + 1

        elif keyPressed == 'p' :
            # Get the cursor position
            x, y = self.iren.GetEventPosition()

            nextActor = self.volumes[self.currentVolume].volActor # Get the next actor
        
            # determine where the cursor is when 'p' is pressed
            cellPicker = vtk.vtkCellPicker()
            cellPicker.PickFromListOn()
            cellPicker.AddPickList(nextActor)
            cellPicker.SetTolerance(0.0001)
            cellPicker.Pick(x, y, 0, self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer())
            
            points = cellPicker.GetPickedPositions()
            numPoints = points.GetNumberOfPoints()
            if numPoints < 1:
                return()
            i, j, k = points.GetPoint(0)
            newPoint = [i, j, k]
            
            # create a sphere at the location of the mouse cursor
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(0.5)
            res = 20
            sphere.SetThetaResolution(res)
            sphere.SetPhiResolution(res)
            sphere.SetCenter(newPoint)
            
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphere.GetOutputPort())
            
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(1, 0, 0)
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( actor )

            self.log.createLogMsg(1, 'Picking point: {}'.format(newPoint))
            self.volumes[self.currentVolume].tPoints.append(actor)
            
            self.iren.Render()      

        return