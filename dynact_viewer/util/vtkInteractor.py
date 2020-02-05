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
        self.AddObserver('RightButtonPressEvent',self.RightButtonPressEvent)

    def RightButtonPressEvent(self, obj, event):     
        
        # Get the point picked by the right mouse button
        self.GetInteractor().GetPicker().Pick( self.GetInteractor().GetEventPosition()[0], 
                                               self.GetInteractor().GetEventPosition()[1], 
                                               0, 
                                               self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer() 
                                             )

        point = self.GetInteractor().GetPicker().GetPickPosition()

        # Get the 
        actorList = self.GetInteractor().GetPicker().GetActors()

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

            val = selectEnclosedPoints.IsInsideSurface( point )

            # If the picked point is within the PolyData surface, draw it
            if val :
                print(f'Picking point:  {point}')

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(source.GetOutputPort())

                actor = vtk.vtkActor()
                actor.GetProperty().SetDiffuseColor(1,0,0)
                actor.SetMapper(mapper)

                self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
        
        self.OnRightButtonDown()
        
        return