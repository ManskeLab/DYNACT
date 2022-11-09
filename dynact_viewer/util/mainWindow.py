#----------------------------------------------------- 
# mainWindow.py
#
# Created by:   Michael Kuczynski
# Created on:   31-01-2020
#
# Description: Main Qt4 window that loads and displays
#              a dynamic CT image.
#----------------------------------------------------- 

# System Imports
import os
import time
import logging

# Local Imports
import util

# VTK Imports
import vtk.qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Qt4 Imports
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QGridLayout, QFrame, QPushButton, QAction, QFileDialog, qApp, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QTimer

# Window Icon Image
iconPath = os.path.join(os.path.join(os.getcwd(), 'util'), 'img')
iconPath = os.path.abspath(os.path.join(iconPath, 'hand_logo.png'))

#-----------------------------------------------#
# Main window class to display dynamic CT images
#-----------------------------------------------#
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Temporary file path
        self.filePath = ''

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

        self.buttons = util.Buttons()
        
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
        self.resetPointButtonWidget = QPushButton('Reset All Points')
        self.resetLastPointButtonWidget = QPushButton('Reset Last Point')
        # self.linesButtonWidget = QPushButton('Calculate Distances')
        self.checkAxesWidget = QPushButton('Check SCS Axes')
        self.checkJCSAxesWidget = QPushButton('Check JCS Axes')
        # self.angleButtonWidget = QPushButton('Calculate Joint Angles')
        # self.regButtonWidget = QPushButton('Between Frame Registration')
        self.saveDataButtonWidget = QPushButton('Save Point Data')
        self.clearLogButtonWidget = QPushButton('Clear Log')

        self.buttonLayout.addWidget(self.startStopButtonWidget)
        self.buttonLayout.addWidget(self.resetVTKButtonWidget)
        self.buttonLayout.addWidget(self.resetPointButtonWidget)
        self.buttonLayout.addWidget(self.resetLastPointButtonWidget)
        # self.buttonLayout.addWidget(self.linesButtonWidget)
        self.buttonLayout.addWidget(self.checkAxesWidget)
        self.buttonLayout.addWidget(self.checkJCSAxesWidget)
        # self.buttonLayout.addWidget(self.angleButtonWidget)
        # self.buttonLayout.addWidget(self.regButtonWidget)
        self.buttonLayout.addWidget(self.saveDataButtonWidget)
        self.buttonLayout.addWidget(self.clearLogButtonWidget)

        self.startStopButtonWidget.clicked.connect(self.buttons.startStopButton)
        self.resetVTKButtonWidget.clicked.connect(self.buttons.resetVTKButton)
        self.resetPointButtonWidget.clicked.connect(self.buttons.resetPointButton)
        self.resetLastPointButtonWidget.clicked.connect(self.buttons.resetLastPointButton)
        # self.linesButtonWidget.clicked.connect(self.buttons.linesButton)
        self.checkAxesWidget.clicked.connect(self.buttons.checkAxesButton)
        self.checkJCSAxesWidget.clicked.connect(self.buttons.checkJCSAxesButton)
        # self.angleButtonWidget.clicked.connect(self.buttons.angleButton)
        # self.regButtonWidget.clicked.connect(self.buttons.regButton)
        self.saveDataButtonWidget.clicked.connect(self.buttons.saveDataButton)
        self.clearLogButtonWidget.clicked.connect(self.buttons.clearLogButton)

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

        # pointPicker = vtk.vtkPointPicker()

        # Pass necessary parameters to the button class
        self.buttons.setParamters(self.title, self.vtkWidget.GetRenderWindow().GetInteractor(), self.currentVolume,
                                    self.log, self.logTextBox, self.volTimer, self.volCB, self.volumes, self.filePath)


        # Create a mapper and actor (only allow one volume at a time)
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        # self.iren.SetPicker(pointPicker)
 
        self.ren.ResetCamera()
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)

        # Initialize the interactor before creating a timer callback
        self.iren.Initialize()
        self.iren.Start()

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

                # Smooth the surface
                smoothPoly = vtk.vtkSmoothPolyDataFilter()
                smoothPoly.SetInputConnection(imageReader.GetOutputPort())
                smoothPoly.SetNumberOfIterations(50)
                smoothPoly.SetRelaxationFactor(0.2)
                smoothPoly.FeatureEdgeSmoothingOff()
                smoothPoly.BoundarySmoothingOn()
                smoothPoly.Update()

                fillHolesFilter = vtk.vtkFillHolesFilter()
                fillHolesFilter.SetInputData(smoothPoly.GetOutput())
                fillHolesFilter.SetHoleSize(1.0)
                fillHolesFilter.Update()

                # Calculate normals for triangle strips
                normals = vtk.vtkPolyDataNormals()
                normals.SetInputConnection(fillHolesFilter.GetOutputPort())
                normals.ComputePointNormalsOn()
                normals.ComputeCellNormalsOn()
                normals.ConsistencyOn()
                normals.Update()
                
                colors = {}
                colors = {'skin':(0.90, 0.76, 0.6), 
                        'bone':(0.89, 0.855, 0.788)}

                # Create a mapper and actor (only allow one volume at a time)
                mapper = vtk.vtkPolyDataMapper()
                actor = vtk.vtkActor()

                # Create a mapper
                mapper.SetInputConnection( normals.GetOutputPort() )
                mapper.ScalarVisibilityOff()
        
                # Create an actor
                # Make the actor colour close to bone
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor( colors['bone'] )
                actor.GetProperty().SetOpacity( 1.0 )
                # actor.GetProperty().SetDiffuse( 0.90 )
                # actor.GetProperty().SetSpecular( 0.40 )
        
                # Save each volume to a list to display later
                tempVolData = util.VolumeData()
                tempVolData.volPoly = smoothPoly.GetOutput()
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
        # Remove any old volumes from memory
        del self.volumes[:]

        imageFileFilter = 'Images (*.vtk *.stl)'
        self.filePath = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), imageFileFilter)
        
        # In Python 3.6 we need to split the file path differently than Python < 3.6
        # For Python 3.6 and PyQt5:
        # filePath[0] = full path to selected image
        # filePath[1] = imageFileFilter (i.e. "Images (*.vtk *.stl)" in this case)
        #
        # For Python 3.5 and PyQt4:
        # filePath = full path to image
        path = self.filePath[0]
        basename = os.path.splitext( os.path.basename( path ) )[0]
        self.buttons.filePath = path
        self.buttons.fileName = path

        # Make sure the user selected something
        if not path :
            self.log.createLogMsg(2, 'No file or directory selected.')
            return

        # Make sure the user selected a valid file
        if not self.filePath[1]:
            if not os.path.isfile( path ):
                print('Error: Invalid file selected.')
                self.log.createLogMsg(3, 'Invalid file selected.')
                return
        
        self.log.createLogMsg(1, 'Reading file: {}'.format(self.filePath))

        imageReader = vtk.vtkPolyDataReader()
        imageReader.SetFileName( path )
        imageReader.Update()

        # Remove any duplicate points.
        cleanFilter = vtk.vtkCleanPolyData()
        cleanFilter.SetInputConnection(imageReader.GetOutputPort())
        cleanFilter.Update()
        
        # Filter to smooth the surface
        self.log.createLogMsg(1, 'Smoothing PolyData.')

        smoothImg = vtk.vtkSmoothPolyDataFilter()
        smoothImg.SetInputConnection(cleanFilter.GetOutputPort())
        smoothImg.SetNumberOfIterations(5)
        smoothImg.SetRelaxationFactor(0.2)
        smoothImg.FeatureEdgeSmoothingOff()
        smoothImg.BoundarySmoothingOn()
        smoothImg.Update()

        self.log.createLogMsg(1, '{}'.format(smoothImg))
        
        # Calculate normals for triangle strips
        self.log.createLogMsg(1, 'Computing normals.')

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(smoothImg.GetOutputPort())
        normals.ComputePointNormalsOn()
        normals.ComputeCellNormalsOn()
        normals.ConsistencyOn()
        normals.Update()

        # create a dict of preset colors (i.e. bone, skin, blood, etc)
        colors = {}
        colors = {'skin':(0.90, 0.76, 0.6), 
                  'bone':(0.89, 0.855, 0.788)}

        # Create a mapper
        self.mapper.SetInputConnection(normals.GetOutputPort())
        self.mapper.ScalarVisibilityOff()

        # Create an actor
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetOpacity(1.0)
        self.actor.GetProperty().SetColor(colors['bone'])

        # Add the new volume to the volume array
        tempVolData = util.VolumeData()
        tempVolData.volPoly = normals.GetOutput()
        tempVolData.volActor = self.actor
        tempVolData.volNum = 0
        tempVolData.name = basename
        self.volumes.append(tempVolData)

        # Delete all actors in the renderer
        actorCollection = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()
        while actorCollection.GetNumberOfItems() > 0 :
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( actorCollection.GetLastActor() )

        # Empty the list of points so lines aren't drawn again
        for i in range (0, len(self.volumes)) :
            del self.volumes[i].tPoints[:]

        # Render the first volume
        self.ren.AddActor(self.actor)

        self.ren.ResetCamera()

        # Reset the rendered volume
        self.iren.Render()