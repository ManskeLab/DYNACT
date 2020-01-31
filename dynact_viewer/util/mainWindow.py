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

# VTK Imports
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Qt5 Imports
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
     QAction, QFileDialog, QApplication, qApp, QDesktopWidget)
from PyQt5.QtGui import QIcon

# Window Icon Image
iconPath = os.path.join(os.path.join(os.getcwd(), "util"), "img")
iconPath = os.path.join(iconPath, "hand_logo.png")

#-----------------------------------------------#
# Main window class to display dynamic CT images
#-----------------------------------------------#
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.frame = QtWidgets.QFrame()

        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.title = "DYNACT Image Viewer"
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

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)


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
 
        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
 
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
 
        self.ren.ResetCamera()
 
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)


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
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())

        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)