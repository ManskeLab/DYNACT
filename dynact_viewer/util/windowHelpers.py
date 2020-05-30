#----------------------------------------------------- 
# windowHelpers.py
#
# Created by:   Michael Kuczynski
# Created on:   29-05-2020
#
# Description: Helper functions for the main window.
#----------------------------------------------------- 

import vtk
from .volumeData import VolumeData

def drawLine(self, point1, point2):
    # Create a line
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1( point1 )
    lineSource.SetPoint2( point2 )
    lineSource.Update()

    # Create an actor for the line
    lineMapper = vtk.vtkPolyDataMapper()
    lineMapper.SetInputConnection( lineSource.GetOutputPort() )

    lineActor = vtk.vtkActor()
    lineActor.GetProperty().SetDiffuseColor( 1, 0, 0 )  # R, G, B
    lineActor.SetMapper( lineMapper )

    return lineActor

# Check to make sure obj is a valid list of type Volume Data
def checkVolType(obj):
    return bool(obj) and isinstance(obj, list) and all(isinstance(elem, VolumeData) for elem in obj)

def icpRegVolumes(self, _volumes):
    if checkVolType(_volumes):
        source = _volumes[0].volPoly
    
        for i in _volumes:
            target = _volumes[i].volPoly

            icp = vtk.vtkIterativeClosestPointTransform()
            icp.SetSource(source)
            icp.SetTarget(target)
            icp.SetMaximumNumberOfIterations(30)
            icp.GetLandmarkTransform().SetModeToRigidBody()
            icp.StartByMatchingCentroidsOn()
            icp.CheckMeanDistanceOn()
            icp.Update()

            _volumes[i].tMat = icp

def transform(self, _volumes):
    if checkVolType(_volumes):
        return