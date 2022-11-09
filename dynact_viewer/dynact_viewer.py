"""
dynact_viewer.py

Created By: Michael Kuczynski
Created On: 31-01-2020

Description: Implementation of a dynamic CT viewer and point picker
             in Python 3 (originally written in C++14).
Usage:
    python dynactViewer.py
"""
import sys
from PyQt5 import QtWidgets

from util.mainWindow import App

# STEPS:
# Select input and output folders
# Decompress and sort raw DICOM images
# Setup interactor style
# Setup timer callback
# Setup scene
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion') 
    window = App()
    sys.exit(app.exec_())