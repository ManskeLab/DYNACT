#----------------------------------------------------- 
# mainWindow.py
#
# Created by:   Michael Kuczynski
# Created on:   31-01-2020
#
# Description: Main Qt5 window that loads and displays
#              a dynamic CT image.
#----------------------------------------------------- 

# System Imports
import os
import time
import logging

# Local Imports
import util

# SimnpleITK Imports
import SimpleITK as sitk

# VTK Imports
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Qt5 Imports
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QGridLayout, QFrame, QPushButton, QAction, QFileDialog, qApp, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QTimer

# Window Icon Image
iconPath = os.path.join(os.path.join(os.getcwd(), 'util'), 'img')
iconPath = os.path.join(iconPath, 'hand_logo.png')

#-----------------------------------------------#
# Main window class to display dynamic CT images
#-----------------------------------------------#
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.volumes = []
        self.points = []
        self.currentVolume = 0

        # Main Qt layout is grid
        self.mainLayout = QGridLayout()

        # New vertical layout for buttons
        self.buttonLayout = QVBoxLayout()

        # Window properties
        self.title = 'DYNACT Image Viewer'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600

        self.frame = QFrame()
        self.volTimer = QTimer()
        self.log = util.LogMessage()
        
        # Initialize the window
        self.initUI()

    #-----------------------------------------------#
    # Initialize the UI
    #-----------------------------------------------#
    def initUI(self):
        # Main VTK window widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.mainLayout.addWidget(self.vtkWidget, 0, 0)

        # Log widget for errors, status, messages, etc.
        self.logTextBox = util.LogWidget(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)
        self.mainLayout.addWidget(self.logTextBox.widget, 1, 0, 1, 2)

        # Button widgets
        self.startStopButtonWidget = QPushButton('Start/Stop Animation')
        self.resetVTKButtonWidget = QPushButton('Reset VTK Window')
        self.resetPointButtonWidget = QPushButton('Reset Points')
        self.linesButtonWidget = QPushButton('Calculate Distances')
        self.angleButtonWidget = QPushButton('Calculate Joint Angles')
        self.regButtonWidget = QPushButton('Between Frame Registration')
        self.saveDataButtonWidget = QPushButton('Save Data to CSV')
        self.clearLogButtonWidget = QPushButton('Clear Log')

        self.buttonLayout.addWidget(self.startStopButtonWidget)
        self.buttonLayout.addWidget(self.resetVTKButtonWidget)
        self.buttonLayout.addWidget(self.resetPointButtonWidget)
        self.buttonLayout.addWidget(self.linesButtonWidget)
        self.buttonLayout.addWidget(self.angleButtonWidget)
        self.buttonLayout.addWidget(self.regButtonWidget)
        self.buttonLayout.addWidget(self.saveDataButtonWidget)
        self.buttonLayout.addWidget(self.clearLogButtonWidget)

        self.startStopButtonWidget.clicked.connect(self.startStopButton)
        self.resetVTKButtonWidget.clicked.connect(self.resetVTKButton)
        self.resetPointButtonWidget.clicked.connect(self.resetPointButton)
        self.linesButtonWidget.clicked.connect(self.linesButton)
        self.angleButtonWidget.clicked.connect(self.angleButton)
        self.regButtonWidget.clicked.connect(self.regButton)
        self.saveDataButtonWidget.clicked.connect(self.saveDataButton)
        self.clearLogButtonWidget.clicked.connect(self.clearLogButton)

        self.mainLayout.addLayout(self.buttonLayout, 0, 1)

        # Initialize the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centreWindow()
        self.setWindowIcon(QIcon(iconPath))       

        # Initialize the menu bar
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        openImageAct = QAction(QIcon('open.png'), '&Open Image', self)
        openImageAct.setShortcut('Ctrl+I')
        openImageAct.setStatusTip('Open a single file')
        openImageAct.triggered.connect(self.showDialogImage)

        openSeriesAct = QAction(QIcon('open.png'), '&Open Series', self)
        openSeriesAct.setShortcut('Ctrl+S')
        openSeriesAct.setStatusTip('Open a series of files')
        openSeriesAct.triggered.connect(self.showDialogSeries)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openImageAct)
        fileMenu.addAction(openSeriesAct)
        fileMenu.addAction(exitAct)

        # Setup the renderer in the vtkWidget
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.renWindow = self.vtkWidget.GetRenderWindow()

        # Setup the timer callbacks
        self.volCB = util.VolumeQTimerCallback()
        self.volCB.setParameters(self.iren, self.volumes, self.currentVolume)
        self.volTimer.timeout.connect(self.volCB.execute)
        self.volCB.volTimer = self.volTimer

        # Custom interactor
        self.irenStyle = util.MyInteractorStyle()
        self.irenStyle.setParameters(self.volumes, self.currentVolume, self.volCB, self.volTimer, self.log)
        self.iren.SetInteractorStyle(self.irenStyle)

        pointPicker = vtk.vtkPointPicker()

        # Create a mapper and actor (only allow one volume at a time)
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.iren.SetPicker(pointPicker)
 
        self.ren.ResetCamera()
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)

        # Initialize the interactor before creating a timer callback
        self.iren.Initialize()

        # Display the window and scene
        self.show()


    #-----------------------------------------------#
    # Centres the application window on the screen
    #-----------------------------------------------#
    def centreWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    #-----------------------------------------------#
    # Clear the render window
    #-----------------------------------------------#
    def clearRenderWindow(self):
        # When clearing the render window, delete any stored volumes

        # Delete all actors in the renderer
        actorCollection = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()

        while actorCollection.GetNumberOfItems() > 0 :
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( actorCollection.GetLastActor() )

        self.currentVolume = 0
        self.volCB.currentVolume = 0
        del self.volumes[:]
        del self.points[:]

        # Render the empty window
        self.iren.GetRenderWindow().Render()

        self.log.createLogMsg(1, 'Render window successfully cleared.')

    def startStopButton(self):
        self.currentVolume = self.volCB.currentVolume
        self.volCB.startStop()

    def resetVTKButton(self):
        # When resetting the render window, do not delete stored volumes

        # Delete all actors in the renderer
        actorCollection = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()

        while actorCollection.GetNumberOfItems() > 0 :
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( actorCollection.GetLastActor() )

        # Reset the volume actor to the first volume in the sequence
        self.currentVolume = 0
        self.volCB.currentVolume = 0
        self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( self.volumes[self.currentVolume].volActor )

        # Empty the list of points so lines aren't drawn again
        del self.points[:]

        # Render the initial scene
        self.iren.GetRenderWindow().Render()

        self.log.createLogMsg(1, 'Render window successfully reset.')

    def resetPointButton(self):
        return

    def linesButton(self):
        # Draw lines and calculate distances between points
        # Only draw a line between points if we have an even number of points
        # self.points = self.irenStyle.points
        self.numPoints = len(self.volumes[self.currentVolume].tPoints)
        
        if ( self.numPoints % 2  == 0) and ( self.numPoints > 0 ):
            # Even number of points
            # Draw a line between each sequential set of points
            for i in range(0, self.numPoints, 2) :
                # Get the coordinates of each point
                coord1 = self.volumes[self.currentVolume].tPoints[i]
                coord2 = self.volumes[self.currentVolume].tPoints[i + 1]

                lineActor = util.drawLine(self, coord1, coord2)

                self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( lineActor )
        else :
            if self.numPoints <= 0 :
                # No points selected
                self.log.createLogMsg(3, 'No points selected. Cannot draw lines.')
            else :
                # Odd number of points
                self.log.createLogMsg(3, 'Odd number of points selected. Please add more points before drawing lines.')

    def angleButton(self):
        return

    def regButton(self):
        return

    def saveDataButton(self):
        return

    def clearLogButton(self):
        self.logTextBox.clear()

    #-----------------------------------------------#
    # Shows a dialog box to select a series of input files
    #-----------------------------------------------#
    def showDialogSeries(self):
        imageFileFilter = 'Images (*.vtk *.stl)'
        userSelection = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), imageFileFilter)

        # Make sure the user selected something
        if not userSelection[0] and not userSelection[1] :
            self.log.createLogMsg(2, 'No file or directory selected.')
            return

        # Get the directory path and the general file name
        selectedDirectory = os.path.dirname(userSelection[0])
        selectedFile = os.path.basename(userSelection[0])
        selectedExtension = os.path.splitext(selectedFile)[1].lower()
        
        numActors = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors().GetNumberOfItems()
        if (numActors > 0) :
            self.clearRenderWindow()

        # Make sure the user selected a valid file
        if selectedDirectory and os.path.isdir(selectedDirectory) :
            i = 0
            for file in os.listdir(selectedDirectory) :
                # Get the next file
                filename = os.fsdecode(file)

                # Get the next file's extension
                extension = os.path.splitext(filename)[1].lower()

                # Skip files that are not the type we want to read
                if extension != selectedExtension :
                    i = i + 1
                    continue

                self.log.createLogMsg(1, 'Reading file: {}'.format(filename))

                fname = os.path.join( selectedDirectory, filename )

                imageReader = vtk.vtkPolyDataReader()
                imageReader.SetFileName( fname )
                imageReader.Update()

                # Create a mapper and actor (only allow one volume at a time)
                mapper = vtk.vtkPolyDataMapper()
                actor = vtk.vtkActor()

                # Create a mapper
                mapper.SetInputConnection( imageReader.GetOutputPort() )
                mapper.ScalarVisibilityOff()
        
                # Create an actor
                # Make the actor colour close to bone
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor( 0.75, 0.75, 0.75 )
                actor.GetProperty().SetOpacity( 1.0 )
                actor.GetProperty().SetDiffuse( 0.90 )
                actor.GetProperty().SetSpecular( 0.40 )
        
                # Save each volume to a list to display later
                tempVolData = util.VolumeData()
                tempVolData.volPoly = imageReader.GetOutput()
                tempVolData.volActor = actor
                tempVolData.volNum = i
                self.volumes.append(tempVolData)

                i = i + 1

        # Render the first volume
        self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(self.volumes[0].volActor)

        self.ren.ResetCamera()
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)

        # Reset the rendered volume
        self.iren.ReInitialize()

        # Render the scene
        self.iren.GetRenderWindow().Render()

    #-----------------------------------------------#
    # Shows a dialog box to select one input file
    #-----------------------------------------------#
    def showDialogImage(self):
        imageFileFilter = 'Images (*.vtk *.stl)'
        filePath = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), imageFileFilter)

        # Make sure the user selected something
        # filePath[0] = full path to selected image
        # filePath[1] = imageFileFilter (i.e. "Images (*.vtk *.stl)" in this case)
        if not filePath[0] and not filePath[1] :
            self.log.createLogMsg(2, 'No file or directory selected.')
            return

        # Make sure the user selected a valid file
        if not filePath[0]:
            if not os.path.isfile(filePath[0]):
                print('Error: Invalid file selected.')
                self.log.createLogMsg(3, 'Invalid file selected.')
                return
        
        self.log.createLogMsg(1, 'Reading file: {}'.format(filePath[0]))

        imageReader = vtk.vtkPolyDataReader()
        imageReader.SetFileName( filePath[0] )
        imageReader.Update()

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


        scalarRange = [-10, 10]
        scheme = 1
        print(scalarRange)

        curvaturesFilter = vtk.vtkCurvatures()
        curvaturesFilter.SetInputConnection(imageReader.GetOutputPort())
        curvaturesFilter.SetCurvatureTypeToGaussian()
        # curvaturesFilter.SetCurvatureTypeToMean()
        curvaturesFilter.Update()
        # curvaturesFilter.GetOutput().GetScalarRange(scalarRange)

        colorSeries = vtk.vtkColorSeries()
        colorSeries.SetColorScheme(scheme)

        lut = vtk.vtkColorTransferFunction()
        lut.SetColorSpaceToHSV()

        numColors = colorSeries.GetNumberOfColors()
        for i in range(numColors):
            color = colorSeries.GetColor(i)
            dColor = [0] * 3
            dColor[0] = float(color[0]) / 255.0
            dColor[1] = float(color[1]) / 255.0
            dColor[2] = float(color[2]) / 255.0
            t = scalarRange[0] + (scalarRange[1] - scalarRange[0]) / (numColors - 1) * i
            lut.AddRGBPoint(t, dColor[0], dColor[1], dColor[2])
        # lut.SetRange(-1,1)
        # lut.Build()


        # Create a mapper
        self.mapper.SetInputConnection( curvaturesFilter.GetOutputPort() )
        self.mapper.SetLookupTable(lut)
        self.mapper.SetScalarRange(scalarRange)

        # Create an actor
        self.actor.SetMapper(self.mapper)

        # Render the first volume
        self.ren.AddActor(self.actor)

        self.ren.ResetCamera()
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)

        # Reset the rendered volume
        self.iren.ReInitialize()
        self.iren.GetRenderWindow().Render()