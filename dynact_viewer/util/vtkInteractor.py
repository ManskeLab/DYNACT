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
        
        self.GetInteractor().GetPicker().Pick( self.GetInteractor().GetEventPosition()[0], 
                                               self.GetInteractor().GetEventPosition()[1], 
                                               0, 
                                               self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer() 
                                             )

        point = self.GetInteractor().GetPicker().GetPickPosition()

        print(f'Picking point:  {point}')

        # Draw a sphere at the picked point
        source = vtk.vtkSphereSource()
        source.SetRadius(1.0)
        source.SetCenter(point[0], point[1], point[2])

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        actor = vtk.vtkActor()
        actor.GetProperty().SetDiffuseColor(1,0,0)
        actor.SetMapper(mapper)

        self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
        
        self.OnRightButtonDown()
        
        return