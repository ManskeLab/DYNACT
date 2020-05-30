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
        self.AddObserver('RightButtonPressEvent', self.RightButtonPressEvent)
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

    def RightButtonPressEvent(self, obj, event): 
        self.iren = self.GetInteractor()

        # Get the point picked by the right mouse button
        self.iren.GetPicker().Pick( self.iren.GetEventPosition()[0], 
                                    self.iren.GetEventPosition()[1], 
                                    0, 
                                    self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer() 
                                  )

        point = self.iren.GetPicker().GetPickPosition()

        # Get the collection of actors that intersect the selected point (should be one)
        actorList = self.iren.GetPicker().GetActors()

        if actorList.GetNumberOfItems() :
            # Get polyData from actor
            nextActor = actorList.GetLastActor() # Get the next actor
            nextMapper = nextActor.GetMapper()   # Get the next actor's PolyData mapper
            polyData = nextMapper.GetInput()     # Get the next actor's PolyData

            # Draw a sphere at the picked point
            source = vtk.vtkSphereSource()
            source.SetRadius(1.0)
            source.SetCenter(point[0], point[1], point[2])

            # Check if the picked point is inside the surface
            selectEnclosedPoints = vtk.vtkSelectEnclosedPoints()
            selectEnclosedPoints.SetInputData( source.GetOutput() )
            selectEnclosedPoints.SetSurfaceData( polyData )
            selectEnclosedPoints.SetTolerance(0.000001)     # Reduce the tolerance so we can pick points easier
            selectEnclosedPoints.Update()

            # Boolean - true if point is enclosed by PolyData, false otherwise
            isEnclosed = selectEnclosedPoints.IsInsideSurface( point )

            # If the picked point is within the PolyData surface, draw it
            if isEnclosed :
                self.log.createLogMsg(1, 'Picking point: {}'.format(point))

                self.volumes[self.currentVolume].tPoints.append(point)

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection( source.GetOutputPort() )

                actor = vtk.vtkActor()
                actor.GetProperty().SetDiffuseColor( 1, 0, 0 )  # R, G, B
                actor.SetMapper( mapper )

                self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( actor )
        
        self.OnRightButtonDown()
        return
        

    def KeyPressEvent(self, obj, event):
        self.iren = self.GetInteractor()

        keyPressed = self.iren.GetKeySym()

        # elif keyPressed == 'p' :
        #     # Print data to CSV file
        #     return

        if keyPressed == 'z' :
            # Start the animation
            self.currentVolume = self.volCB.currentVolume
            self.volCB.startStop()
            return

        return