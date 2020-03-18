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

# Local Imports
import util

# SimnpleITK Imports
import SimpleITK as sitk

# VTK Imports
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Qt5 Imports
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QHBoxLayout, QFrame,
     QSplitter, QStyleFactory ,QAction, QFileDialog, QApplication, qApp, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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

        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.title = 'DYNACT Image Viewer'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
        self.initUI()

    def initUI(self):
        #-----------------------------------------------#
        # Initialize the window
        #-----------------------------------------------#
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centreWindow()
        self.setWindowIcon(QIcon(iconPath))       

        #-----------------------------------------------#
        # Initialize the menu bar
        #-----------------------------------------------#
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        openAct = QAction(QIcon('open.png'), '&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open a file')
        openAct.triggered.connect(self.showDialog)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)
        fileMenu.addAction(exitAct)


        #-----------------------------------------------#
        # Render and display the VTK object
        #-----------------------------------------------#
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # glob.renWindow = self.vtkWidget.GetRenderWindow()
        
        # Custom interactor
        self.irenStyle = util.MyInteractorStyle()
        self.iren.SetInteractorStyle(self.irenStyle)

        pointPicker = vtk.vtkPointPicker()

        # Create a mapper and actor (only allow one volume at a time)
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.iren.SetPicker(pointPicker)
 
        self.ren.ResetCamera()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        #-----------------------------------------------#
        # Setup the timer callback
        #-----------------------------------------------#
        self.cb = util.MyTimerCallback()
        self.cb.volumes = self.volumes
        self.iren.AddObserver('TimerEvent', self.cb.execute)

        #-----------------------------------------------#
        # Display the window and scene
        #-----------------------------------------------#
        self.show()
        self.iren.Initialize()



    #-----------------------------------------------#
    # Centres the application window on the screen
    #-----------------------------------------------#
    def centreWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    #-----------------------------------------------#
    # Shows a dialog box to select input files
    #-----------------------------------------------#
    def showDialog(self):
        imageFileFilter = 'Images (*.vtk *.stl)'
        filePath = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), imageFileFilter)

        # Make sure the user selected something
        if not filePath[0] and  not filePath[1] :
            print('Error: No file or directory selected.')
            return
        
        # Get the directory path and the general file name
        [path, name] = filePath[0].rsplit('/', 1)

        # Make sure the user selected a valid file
        if filePath[0]:
            if os.path.isfile(filePath[0]):
                for i in range(19) :
                    if i < 10 :
                        fname = os.path.join( path, 'V0' + str(i) + '_MESH.vtk' )
                    else:
                        fname = os.path.join( path, 'V' + str(i) + '_MESH.vtk' )

                    imageReader = vtk.vtkPolyDataReader()
                    imageReader.SetFileName( fname )
                    imageReader.Update()

                    # Create a mapper
                    self.mapper.SetInputConnection( imageReader.GetOutputPort() )
                    self.mapper.ScalarVisibilityOff()
            
                    # Create an actor
                    # Make the actor colour close to bone
                    self.actor.SetMapper(self.mapper)
                    self.actor.GetProperty().SetColor( 0.75, 0.75, 0.75 )
                    self.actor.GetProperty().SetOpacity( 1.0 )
                    self.actor.GetProperty().SetDiffuse( 0.90 )
                    self.actor.GetProperty().SetSpecular( 0.40 )
            
                    # Save each volume to a list to display later
                    self.volumes.append(self.actor)

                # Render the first volume
                self.ren.AddActor(self.actor)
        
                self.ren.ResetCamera()
                self.frame.setLayout(self.vl)
                self.setCentralWidget(self.frame)

                # Reset the rendered volume
                self.iren.GetRenderWindow().Render()
                