#----------------------------------------------------- 
# volumeData.py
#
# Created by:   Michael Kuczynski
# Created on:   29-05-2020
#
# Description: A class to hold information for each volume in a dynamic CT dataset.
#----------------------------------------------------- 

import vtk

class VolumeData:
    def __init__(self):
        self.name = "None"
        self.volPoly = None
        self.volActor = None
        self.volNum = -1
        self.tMat = []
        self.tPoints = []
        self.tLines = []

    def printContents(self):
        print('Volume #{}:'.format(self.volNum))
        print(self.name)
        print(self.volActor)
        print(self.tMat)
        print('---------------------------')