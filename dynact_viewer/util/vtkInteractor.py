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

        # Keep a list of all points selected
        self.points = []

    def RightButtonPressEvent(self, obj, event):     
        print(glob.test)
        # Get the point picked by the right mouse button
        self.GetInteractor().GetPicker().Pick( self.GetInteractor().GetEventPosition()[0], 
                                               self.GetInteractor().GetEventPosition()[1], 
                                               0, 
                                               self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer() 
                                             )

        point = self.GetInteractor().GetPicker().GetPickPosition()

        # Get the collection of actors that intersect the selected point (should be one)
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

            # Boolean - true if point is enclosed by PolyData, false otherwise
            isEnclosed = selectEnclosedPoints.IsInsideSurface( point )

            # If the picked point is within the PolyData surface, draw it
            if isEnclosed :
                print(f'Picking point:  {point}')

                self.points.append(point)

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection( source.GetOutputPort() )

                actor = vtk.vtkActor()
                actor.GetProperty().SetDiffuseColor( 1, 0, 0 )  # R, G, B
                actor.SetMapper( mapper )

                self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( actor )
        
        self.OnRightButtonDown()
        return
        

    def KeyPressEvent(self, obj, event):
        keyPressed = self.GetInteractor().GetKeySym()

        if keyPressed == 'l' :
            # Draw lines and calculate distances between points
            # Only draw a line between points if we have an even number of points
            self.numPoints = len(self.points)
            
            if ( self.numPoints % 2  == 0) and ( self.numPoints > 0 ):
                # Even number of points
                self.DrawLines()
            else :
                # TO-DO: Send message to Qt GUI
                if numPoints <= 0 :
                    # No points selected
                    print('Error: No points selected. Cannot draw lines.')
                else :
                    # Odd number of points
                    print('Error: Odd number of points selected. Please add more points before drawing lines.')
                
                return
        
        elif keyPressed == 'r' :
            # Reset picked points
            actorCollection = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()

            # Delete all actors in the renderer except for the scan volume (i.e. actor #1)
            while actorCollection.GetNumberOfItems() > 1 :
                self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( actorCollection.GetLastActor() )

            # Empty the list of points so lines aren't drawn again
            del self.points[:]

        # elif keyPressed == 'p' :
        #     # Print data to CSV file
        #     return

        elif keyPressed == 'z' :
            # Start the animation
            self.GetInteractor().CreateRepeatingTimer( 200 )
            # self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( volumes[10] )

        # elif keyPressed == 'x' :
        #     # Stop the animation
        #     return

        return


    def DrawLines(self):
        # Draw a line between each sequential set of points
        for i in range(0, self.numPoints, 2) :
            # Get the coordinates of each point
            coord1 = self.points[i]
            coord2 = self.points[i + 1]

            # Create a line
            lineSource = vtk.vtkLineSource()
            lineSource.SetPoint1( coord1 )
            lineSource.SetPoint2( coord2 )
            lineSource.Update()

            # Create an actor for the line
            lineMapper = vtk.vtkPolyDataMapper()
            lineMapper.SetInputConnection( lineSource.GetOutputPort() )

            lineActor = vtk.vtkActor()
            lineActor.GetProperty().SetDiffuseColor( 1, 0, 0 )  # R, G, B
            lineActor.SetMapper( lineMapper )

            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( lineActor )

        return
