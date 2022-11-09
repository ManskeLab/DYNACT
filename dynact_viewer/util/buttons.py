#----------------------------------------------------- 
# buttons.py
#
# Created by:   Michael Kuczynski
# Created on:   04-10-2020
#
# Description: Contains custom button definitions.
#-----------------------------------------------------
import os
import math

import vtk

from .volumeData import VolumeData
from .logger import *

class Buttons:
    def __init__(self):
        self.title = ''
        self.iren = None
        self.currentVolume = 0
        self.log = None
        self.logTextBox = None
        self.volTimer = None
        self.volCB = None
        self.volumes = []
        self.filePath = ''
        self.fileName = ''
        self.trpSCS = []
        self.mc1SCS = []

    def setParamters(self, _title, _iren, _currentVolume, _log, _logTextBox, _volTimer, _volCB,  _volumes, _filePath):
        assert type(_title) is str
        assert type(_filePath) is str
        assert type(_currentVolume) is int and (_currentVolume > -1)
        assert type(_volumes) is list

        self.title = _title
        self.iren = _iren
        self.currentVolume = _currentVolume
        self.log = _log
        self.logTextBox = _logTextBox
        self.volTimer = _volTimer
        self.volCB = _volCB
        self.volumes = _volumes
        self.filePath = _filePath

    #-----------------------------------------------#
    # Clear the render window
    #-----------------------------------------------#
    def clearRenderWindowButton(self):
        # # When clearing the render window, delete any stored volumes
        # if not self.volumes :
        #     self.log.createLogMsg(2, 'No volume loaded. Nothing to clear.')
        #     return

        # # Delete all actors in the renderer
        # actorCollection = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()

        # while actorCollection.GetNumberOfItems() > 0 :
        #     self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( actorCollection.GetLastActor() )

        # self.currentVolume = 0
        # self.volCB.currentVolume = 0
        # del self.volumes[:]
        # # del self.points[:]

        # # Render the empty window
        # self.iren.GetRenderWindow().Render()

        # self.log.createLogMsg(1, 'Render window successfully cleared.')
        return

    #-----------------------------------------------#
    # Start/Stop the animation
    #-----------------------------------------------#
    def startStopButton(self):
            # Check if we have more than one volume
        if not self.volumes :
            # No volumes are loaded
            self.log.createLogMsg(3, 'No volumes loaded! Cannot start/stop animation.')
        elif len(self.volumes) == 1 :
            # Only a single volume is loaded
            self.log.createLogMsg(3, 'Only one volume is loaded! Cannot start/stop animation.')
        else :
            # Start the animation
            self.currentVolume = self.volCB.currentVolume
            self.volCB.startStop()
        return

    #-----------------------------------------------#
    # Reset the VTK render window
    #-----------------------------------------------#
    def resetVTKButton(self):
        # Check if anything is loaded
        numActors = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors().GetNumberOfItems()
        if numActors <= 0 :
            self.log.createLogMsg(2, 'No volume loaded. Cannot reset VTK window.')
            return

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
        for i in range (0, len(self.volumes)) :
            del self.volumes[i].tPoints[:]

        # Print a log message
        self.log.createLogMsg(1, 'Render window successfully reset.')
        self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.iren.Render()        

    #-----------------------------------------------#
    # Reset all picked points and lines
    #-----------------------------------------------#
    def resetPointButton(self):
        # Check if we have any points
        if not self.volumes :
            self.log.createLogMsg(2, 'No volume loaded. Cannot compute dot product on empty list.')
            return
        elif not self.volumes[self.currentVolume].tPoints :
            self.log.createLogMsg(2, 'No points to remove.')
            return

        # Remove the point actors from the scene
        for i in range (0, len(self.volumes[self.currentVolume].tPoints)) :
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( self.volumes[self.currentVolume].tPoints[i] )

        # Empty the list of points so lines aren't drawn again
        del self.volumes[self.currentVolume].tPoints[:]

        # Print a log message
        self.log.createLogMsg(1, 'Removed all points successfully.')
        self.iren.Render()

    #-----------------------------------------------#
    # Reset the last picked point
    #-----------------------------------------------#
    def resetLastPointButton(self):
        # Check if we have any points
        if not self.volumes :
            self.log.createLogMsg(2, 'No volume loaded. Cannot compute dot product on empty list.')
            return
        elif not self.volumes[self.currentVolume].tPoints :
            self.log.createLogMsg(2, 'No points to remove.')
            return

        # Remove the last point added to the point array
        removedPoint = self.volumes[self.currentVolume].tPoints.pop()

        # Remove the last point actor from the scene
        self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( removedPoint )

        # Print a log message
        self.log.createLogMsg(1, 'Removed last point successfully.')
        self.iren.Render()

    #-----------------------------------------------#
    # Draw lines between each set of points
    #-----------------------------------------------#
    def linesButton(self):
        return
        # Draw lines and calculate distances between points
        # Only draw a line between points if we have an even number of points
        # self.points = self.irenStyle.points

        # self.numPoints = len(self.volumes[self.currentVolume].tPoints)
        
        # if ( self.numPoints % 2  == 0) and ( self.numPoints > 0 ):
        #     # Even number of points
        #     # Draw a line between each sequential set of points
        #     for i in range(0, self.numPoints, 2) :
        #         # Get the coordinates of each point
        #         coord1 = self.volumes[self.currentVolume].tPoints[i]
        #         coord2 = self.volumes[self.currentVolume].tPoints[i + 1]

        #         lineActor = util.drawLine(self, coord1, coord2)

        #         self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( lineActor )
        # else :
        #     if self.numPoints <= 0 :
        #         # No points selected
        #         self.log.createLogMsg(3, 'No points selected. Cannot draw lines.')
        #     else :
        #         # Odd number of points
        #         self.log.createLogMsg(3, 'Odd number of points selected. Please add more points before drawing lines.')

    #-----------------------------------------------#
    # Check if the dot product of the axes is zero
    #-----------------------------------------------#
    def checkAxesButton(self):
        if not self.volumes :
            self.log.createLogMsg(2, 'No volume loaded. Cannot compute dot product on empty list.')
            return
        elif not self.volumes[self.currentVolume].tPoints :
            self.log.createLogMsg(2, 'No points selected. Cannot compute dot product on empty list.')
            return

        loadedImage = self.volumes[self.currentVolume]

        if 'TRP' in loadedImage.name :
            '''TRAPEZIUM'''
            if len( self.volumes[self.currentVolume].tPoints ) != 4 :
                self.log.createLogMsg(3, 'Incorrect number of points selected for TRAPEZIUM. Four points must be selected to compute the dot product.')
                return

            TM1J = loadedImage.tPoints[0].GetCenter()
            TM2J = loadedImage.tPoints[1].GetCenter()
            TSTJ = loadedImage.tPoints[2].GetCenter()
            TDET = loadedImage.tPoints[3].GetCenter()
            originTRP = TSTJ

            Z_TRP = [ (TDET[0] - TM2J[0]), (TDET[1] - TM2J[1]), (TDET[2] - TM2J[2]) ]
            X_TRP = [0,0,0]
            vtk.vtkMath.Cross( [ (TSTJ[0] - TM1J[0]), (TSTJ[1] - TM1J[1]), (TSTJ[2] - TM1J[2]) ], Z_TRP, X_TRP)
            Y_TRP = [0,0,0]
            vtk.vtkMath.Cross( Z_TRP, X_TRP, Y_TRP )

            msg = 'TRAPEZIUM Segment Coordinate System axes check:' + \
                    '\nX * Y = ' + str(vtk.vtkMath.Dot(X_TRP, Y_TRP)) + \
                    '\nX * Z = ' + str(vtk.vtkMath.Dot(X_TRP, Z_TRP)) + \
                    '\nY * Z = ' + str(vtk.vtkMath.Dot(Y_TRP, Z_TRP))
            self.log.createLogMsg(1, msg)

            # If axes are orthogonal, save the data
            if math.isclose(vtk.vtkMath.Dot(X_TRP, Y_TRP), 0) and \
                math.isclose(vtk.vtkMath.Dot(X_TRP, Z_TRP), 0) and \
                math.isclose(vtk.vtkMath.Dot(Y_TRP, Z_TRP), 0) :
                self.trpSCS = [X_TRP, Y_TRP, Z_TRP] 

        elif 'MC1' in loadedImage.name:
            '''MC1'''
            if len( self.volumes[self.currentVolume].tPoints ) != 3 :
                self.log.createLogMsg(1, 'Incorrect number of points selected for FIRST METACARPAL. Three points must be selected to compute the dot product.')
                return

            # Points        
            M_LDT = loadedImage.tPoints[0].GetCenter()
            M_MDT = loadedImage.tPoints[1].GetCenter()
            M_CPB = loadedImage.tPoints[2].GetCenter()
            tubercle_mid = [ (M_LDT[0] + M_MDT[0])/2, (M_LDT[1] + M_MDT[1])/2, (M_LDT[2] + M_MDT[2])/2 ]
            originMC1 = M_CPB

            # Vectors
            V_ML = [ (M_LDT[0] - M_MDT[0]), (M_LDT[1] - M_MDT[1]), (M_LDT[2] - M_MDT[2]) ]
            Y_MC1 = [ (M_CPB[0] - tubercle_mid[0]), (M_CPB[1] - tubercle_mid[1]), (M_CPB[2] - tubercle_mid[2]) ]

            X_MC1 = [0,0,0]
            vtk.vtkMath.Cross([ tubercle_mid[0] - M_MDT[0], tubercle_mid[1] - M_MDT[1], tubercle_mid[2] - M_MDT[2] ], Y_MC1, X_MC1)

            Z_MC1 = [0,0,0]
            vtk.vtkMath.Cross(X_MC1, Y_MC1, Z_MC1)
            
            msg = 'FIRST METACARPAL Segment Coordinate System axes check:' + \
                    '\nX * Y = ' + str(vtk.vtkMath.Dot(X_MC1, Y_MC1)) + \
                    '\nX * Z = ' + str(vtk.vtkMath.Dot(X_MC1, Z_MC1)) + \
                    '\nY * Z = ' + str(vtk.vtkMath.Dot(Y_MC1, Z_MC1))
            self.log.createLogMsg(1, msg)

            # If axes are orthogonal, save the data
            if math.isclose(vtk.vtkMath.Dot(X_MC1, Y_MC1), 0) and \
                math.isclose(vtk.vtkMath.Dot(X_MC1, Z_MC1), 0) and \
                math.isclose(vtk.vtkMath.Dot(Y_MC1, Z_MC1), 0) :
                self.mc1SCS = [X_MC1, Y_MC1, Z_MC1] 
        return

    def checkJCSAxesButton(self):
        if not self.volumes:
            self.log.createLogMsg(3, 'No volume loaded. Cannot check JCS axes.')
            return

        loadedImage = self.volumes[self.currentVolume]

        directory = os.path.dirname(self.filePath)
        trpPointFile = os.path.join(directory, 'TRP_SCS.txt')
        mc1PointFile = os.path.join(directory, 'MC1_SCS.txt')

        if os.path.isfile(trpPointFile) and os.path.isfile(mc1PointFile) :
            self.log.createLogMsg(1, 'Reading in point file {}.'.format(trpPointFile))
            f = open(trpPointFile, 'r')
            self.trpSCS = []
            for line in f.readlines():
                fields = line.split(',')
                self.trpSCS.append( [float(fields[0]), float(fields[1]), float(fields[2]) ] )
            f.close()
            assert type(self.trpSCS) is list and len(self.trpSCS) == 4

            self.log.createLogMsg(1, 'Reading in point file {}.'.format(mc1PointFile))
            f = open(mc1PointFile, 'r')
            self.mc1SCS = []
            for line in f.readlines():
                fields = line.split(',')
                self.mc1SCS.append( [float(fields[0]), float(fields[1]), float(fields[2]) ] )
            f.close()
            assert type(self.mc1SCS) is list and len(self.mc1SCS) == 3
        else:
            self.log.createLogMsg(3, 'No file exists or incorrect file name for SCS text file.')
            return

        '''JCS'''
        #----------------------------
        # TRAPEZIUM SCS
        #----------------------------
        TM1J = self.trpSCS[0]
        TM2J = self.trpSCS[1]
        TSTJ = self.trpSCS[2]
        TDET = self.trpSCS[3]

        # Z - Runs medial-lateral
        Z_TRP = [ (TDET[0] - TM2J[0]), (TDET[1] - TM2J[1]), (TDET[2] - TM2J[2]) ]
        
        # X - Runs dorsal-volar
        X_TRP = [0,0,0]
        vtk.vtkMath.Cross( [ (TSTJ[0] - TM1J[0]), (TSTJ[1] - TM1J[1]), (TSTJ[2] - TM1J[2]) ], Z_TRP, X_TRP)
        
        # Y - Runs distal-proximal
        Y_TRP = [0,0,0]
        vtk.vtkMath.Cross( Z_TRP, X_TRP, Y_TRP )

        # Normalize vectors (normalizes in place and returns norm)
        Y_TRP_norm = vtk.vtkMath.Normalize(Y_TRP)
        X_TRP_norm = vtk.vtkMath.Normalize(X_TRP)
        Z_TRP_norm = vtk.vtkMath.Normalize(Z_TRP)

        #---------------------------- 
        # FIRST METACARPAL SCS
        #----------------------------
        M_LDT = self.mc1SCS[0]
        M_MDT = self.mc1SCS[1]
        M_CPB = self.mc1SCS[2]

        # Mid point between the lateral and medial MC1 tubercles
        tubercle_mid = [ (M_LDT[0] + M_MDT[0])/2, (M_LDT[1] + M_MDT[1])/2, (M_LDT[2] + M_MDT[2])/2 ]
        
        # Vector between the lateral and medial MC1 tubercles
        V_ML = [ (M_LDT[0] - M_MDT[0]), (M_LDT[1] - M_MDT[1]), (M_LDT[2] - M_MDT[2]) ]

        # Y - Runs distal-proximal
        Y_MC1 = [ (M_CPB[0] - tubercle_mid[0]), (M_CPB[1] - tubercle_mid[1]), (M_CPB[2] - tubercle_mid[2]) ]
        
        # X - Runs dorsal-volar
        X_MC1 = [0,0,0]
        vtk.vtkMath.Cross(V_ML, Y_MC1, X_MC1)
        
        # Z - Runs medial-lateral
        Z_MC1 = [0,0,0]
        vtk.vtkMath.Cross(X_MC1, Y_MC1, Z_MC1)

        # Normalize vectors (normalizes in place and returns norm)
        Y_MC1_norm = vtk.vtkMath.Normalize(Y_MC1)
        X_MC1_norm = vtk.vtkMath.Normalize(X_MC1)
        Z_MC1_norm = vtk.vtkMath.Normalize(Z_MC1)

        # Perform sanity checks
        msg = 'MC1 Segment Coordinate System axes check:' + \
                    '\nX_MC1 * Y_MC1 = ' + str(vtk.vtkMath.Dot(X_MC1, Y_MC1)) + \
                    '\nX_MC1 * Z_MC1 = ' + str(vtk.vtkMath.Dot(X_MC1, Z_MC1)) + \
                    '\nZ_MC1 * Y_MC1 = ' + str(vtk.vtkMath.Dot(Y_MC1, Z_MC1))
        self.log.createLogMsg(1, msg)

        msg = 'TMC Segment Coordinate System axes check:' + \
                    '\nX_TRP * Y_TRP = ' + str(vtk.vtkMath.Dot(X_TRP, Y_TRP)) + \
                    '\nX_TRP * Z_TRP = ' + str(vtk.vtkMath.Dot(X_TRP, Z_TRP)) + \
                    '\nZ_TRP * Y_TRP = ' + str(vtk.vtkMath.Dot(Y_TRP, Z_TRP))
        self.log.createLogMsg(1, msg)

        #----------------------------
        # TMC JSC:
        #----------------------------
        e1 = Z_TRP
        e3 = X_MC1
        e2 = [0,0,0]
        vtk.vtkMath.Cross(e1, e3, e2)

        # Perform sanity checks
        msg = 'TMC Joint Coordinate System axes check:' + \
                    '\ne1 * e3 = ' + str(vtk.vtkMath.Dot(e1, e3)) + \
                    '\ne1 * e2 = ' + str(vtk.vtkMath.Dot(e1, e2)) + \
                    '\ne2 * e3 = ' + str(vtk.vtkMath.Dot(e2, e3))
        self.log.createLogMsg(1, msg)

        msg = 'Angle between TMC Joint Coordinate System axes:' + \
                    '\nAngle between e1 and e3 = ' + str(math.degrees(math.acos(vtk.vtkMath.Dot(e1, e3) / (vtk.vtkMath.Norm(e1) * vtk.vtkMath.Norm(e3)) )) ) + \
                    '\nAngle between e1 and e2 = ' + str(math.degrees(math.acos(vtk.vtkMath.Dot(e1, e2) / (vtk.vtkMath.Norm(e1) * vtk.vtkMath.Norm(e2)) )) ) + \
                    '\nAngle between e2 and e3 = ' + str(math.degrees(math.acos(vtk.vtkMath.Dot(e2, e3) / (vtk.vtkMath.Norm(e2) * vtk.vtkMath.Norm(e3)) )) )
        self.log.createLogMsg(1, msg)

        # Write out the JCS to a text file
        directory = os.path.dirname(self.filePath)
        output_filename = os.path.join(directory, 'JSC_points.txt')

        self.log.createLogMsg(1, 'Writing JCS to {}'.format(output_filename))
        f = open(output_filename, 'w')
        contents = 'e1 = ' + str(e1) + '\n' + 'e2 = ' + str(e2) + '\n' + 'e3 = ' + str(e3)
        f.write(contents)
        f.close()

        return

    def angleButton(self):
        return

    def regButton(self):
        return

    #-----------------------------------------------#
    # Save point data to a text file
    #-----------------------------------------------#
    def saveDataButton(self):
        if not self.volumes:
            self.log.createLogMsg(3, 'No volume loaded. Cannot export point data.')
            return
        elif not self.volumes[self.currentVolume].tPoints:
            self.log.createLogMsg(3, 'No points selected. Cannot export point data.')
            return

        loadedImage = self.volumes[self.currentVolume]

        parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        modelDirectory = os.path.dirname(self.filePath)
        outputDirectory = os.path.join(parentDir, 'output')
        modelNumber = str(self.filePath[-24:-12])

        if 'TRP' in loadedImage.name and len(self.volumes[self.currentVolume].tPoints) == 4:
            output_filename = os.path.join(outputDirectory, modelNumber + '_TRP_SCS.txt')
        elif 'MC1' in loadedImage.name and len(self.volumes[self.currentVolume].tPoints) == 3:
            output_filename = os.path.join(outputDirectory, modelNumber + '_MC1_SCS.txt')
        else :
            self.log.createLogMsg(2, 'Not enough points for SCS selected. Writing data anyway.')
            output_filename = os.path.join(outputDirectory, 'dynact_viewer_points.txt')

        # Check if output exists and should overwrite
        # if os.path.isfile(output_filename):
            # self.log.createLogMsg(1, 'File {} already exists. Overwrite? [y/n]: '.format(output_filename))
            # self.log.createLogMsg(1, 'Please clear the log window, then enter')
            # result = self.log.readMsg(4, self.logTextBox)
            # if result.lower() != 'yes':
                # self.log.createLogMsg(1, 'Not overwriting. Please try again, or exit the program.')
                # return
            
        self.log.createLogMsg(1, 'Writing points to {}'.format(output_filename))
        f = open(output_filename, 'w')
        for point in loadedImage.tPoints :
            posn = point.GetCenter()
            line = str(posn[0]) + ', ' + str(posn[1]) + ', ' + str(posn[2]) + '\n'
            f.write(line)
        f.close()
        
        return

    def clearLogButton(self):
        self.logTextBox.clear()
