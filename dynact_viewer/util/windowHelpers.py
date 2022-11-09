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

def distanceMapping(self):
    return
    # scalarRange = [0] * 2
    # curvaturesFilter = vtk.vtkCurvatures()
    # curvaturesFilter.SetInputConnection(imageReader.GetOutputPort())
    # curvaturesFilter.SetCurvatureTypeToGaussian()
    # # curvaturesFilter.SetCurvatureTypeToMean()
    # curvaturesFilter.Update()
    # curvaturesFilter.GetOutput().GetScalarRange(scalarRange)


    # rh = vtk.vtkParametricRandomHills()
    # rhFnSrc = vtk.vtkParametricFunctionSource()
    # rhFnSrc.SetParametricFunction(rh)

    # vertexGlyphFilter = vtk.vtkVertexGlyphFilter()
    # vertexGlyphFilter.AddInputData(curvaturesFilter.GetOutput())
    # vertexGlyphFilter.Update()

    # polyData = vertexGlyphFilter.GetOutput()


    # bounds = polyData.GetBounds()
    # rangee = [0] * 3
    # for i in range(3):
    #     rangee[i] = bounds[2 * i + 1] - bounds[2 * i]
    
    # sampleSize = polyData.GetNumberOfPoints() * .00005
    # if sampleSize < 10:
    #     sampleSize = 50
    
    # distance = vtk.vtkSignedDistance()
    # if polyData.GetPointData().GetNormals():
    #     print('using normals')
    #     distance.SetInputData(polyData)
    
    # else:
    #     print('estimating normals')
    #     normals = vtk.vtkPCANormalEstimation()
    #     normals.SetInputData(polyData)
    #     normals.SetSampleSize(sampleSize)
    #     normals.SetNormalOrientationToGraphTraversal()
    #     normals.FlipNormalsOn()
    #     distance.SetInputConnection(normals.GetOutputPort())
    
    # dimension = 256
    # radius = max(max(rangee[0], rangee[1]), rangee[2]) / float(dimension) * 4

    # distance.SetRadius(radius)
    # distance.SetDimensions(dimension, dimension, dimension)
    # distance.SetBounds(bounds[0] - rangee[0] * .1, bounds[1] + rangee[0] * .1, bounds[2] - rangee[1] * .1, bounds[3] + rangee[1] * .1, bounds[4] - rangee[2] * .1, bounds[5] + rangee[2] * .1)

    # surface = vtk.vtkExtractSurface()
    # surface.SetInputConnection(distance.GetOutputPort())
    # surface.HoleFillingOn()
    # surface.SetRadius(radius)
    # surface.Update()

    # fillHolesFilter = vtk.vtkFillHolesFilter()
    # fillHolesFilter.SetInputData(imageReader.GetOutput())
    # fillHolesFilter.SetHoleSize(10000000.0)
    # fillHolesFilter.Update()

    # tri = vtk.vtkTriangleFilter()
    # tri.SetInputConnection(fillHolesFilter.GetOutputPort())
    # tri.Update()

    # cleaner = vtk.vtkCleanPolyData()
    # cleaner.SetInputConnection(tri.GetOutputPort())
    # # cleaner.SetTolerance(0.005)
    # cleaner.Update()


    # colors = vtk.vtkNamedColors()

    # # Colour transfer function
    # ctf = vtk.vtkColorTransferFunction()
    # ctf.SetColorSpaceToDiverging()
    # p1 = [0.0] + list(colors.GetColor3d("MidnightBlue"))
    # p2 = [1.0] + list(colors.GetColor3d("Red"))
    # ctf.AddRGBPoint(*p1)
    # ctf.AddRGBPoint(*p2)
    # cc = list()
    # for i in range(256):
    #     cc.append(ctf.GetColor(float(i) / 255.0))

    # # Lookup table
    # lut = vtk.vtkLookupTable()
    # lut.SetNumberOfColors(256)
    # for i, item in enumerate(cc):
    #     lut.SetTableValue(i, item[0], item[1], item[2], 1.0)
    # lut.SetRange(-1,1)
    # lut.Build()

    # curvatures = vtk.vtkCurvatures()
    # curvatures.SetCurvatureTypeToMean()
    # curvatures.SetInputConnection(cleaner.GetOutputPort())


    # scalarRange = [-10, 10]
    # scheme = 1
    # print(scalarRange)

    # curvaturesFilter = vtk.vtkCurvatures()
    # curvaturesFilter.SetInputConnection(imageReader.GetOutputPort())
    # curvaturesFilter.SetCurvatureTypeToGaussian()
    # curvaturesFilter.SetCurvatureTypeToMean()
    # curvaturesFilter.Update()
    # curvaturesFilter.GetOutput().GetScalarRange(scalarRange)

    # colorSeries = vtk.vtkColorSeries()
    # colorSeries.SetColorScheme(scheme)

    # lut = vtk.vtkColorTransferFunction()
    # lut.SetColorSpaceToHSV()

    # numColors = colorSeries.GetNumberOfColors()
    # for i in range(numColors):
    #     color = colorSeries.GetColor(i)
    #     dColor = [0] * 3
    #     dColor[0] = float(color[0]) / 255.0
    #     dColor[1] = float(color[1]) / 255.0
    #     dColor[2] = float(color[2]) / 255.0
    #     t = scalarRange[0] + (scalarRange[1] - scalarRange[0]) / (numColors - 1) * i
    #     lut.AddRGBPoint(t, dColor[0], dColor[1], dColor[2])
    # lut.SetRange(-1,1)
    # lut.Build()