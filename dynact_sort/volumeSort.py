#----------------------------------------------------- 
# dynactVolumeSort.py
#
# Created by:   Michael Kuczynski
# Created on:   20-07-2020
#
# Description: Sorts uncompressed DICOM images from dynamic CT scans by frame/volume.
#              The number of volumes is calculated using the following:
#                   # Volumes = (total # images) / (# images per volume)
#                   # Volumes = (total # images) / (total collimation width / slice thickness)
#
#----------------------------------------------------- 
# Usage:
#   1. conda activate manskelab
#   2. dynactVolumeSort.py <DICOM_FOLDER>
#----------------------------------------------------- 

import os
import math
import errno
import shutil
import pydicom
import argparse

def moveDICOM(image, imagePerVolume, inputDir):
    ds = pydicom.dcmread(image)
    instanceNum = int(ds.InstanceNumber)

    imageVolume = math.ceil(instanceNum / imagePerVolume)

    copyDir = os.path.join(inputDir, 'Volume_' + str(imageVolume))
    shutil.move( os.path.join(inputDir, image), copyDir )

def sortDYNACTVolumes(inputDirectory):
    # Calculate the number of volumes in the series using the first image in the directory as input
    # First count the number of DICOM files in the provided directory
    list_of_files = os.listdir(inputDirectory)
    numImages = len([x for x in list_of_files if x.endswith(".dcm")])

    collimationWidth = 0
    sliceThickness = 0
    imagePerVolume = 0
    numVolumes = 0

    # Use a boolean variable to get collimation width and slice thickness from the first DICOM read in
    firstImage = True

    # Loop through the entire input folder 
    # Get the tag of each DICOM image to analyze the series description
    # Finally, place the image into the correct volume directory
    for DICOMfile in os.listdir(inputDirectory):
        # Get the next item in the directory
        nextItem = os.fsdecode(DICOMfile)

        # Skip any directories and loop over files only
        if os.path.isdir(nextItem):
            print('Skipping directory: ' + nextItem)
            continue

        filename, extension = os.path.splitext( nextItem )

        if firstImage and extension == '.dcm':
            firstImage = False
            image = os.path.join(inputDirectory, nextItem)
            ds = pydicom.dcmread(image)
            collimationWidth = int(ds.TotalCollimationWidth)
            sliceThickness = float(ds.SliceThickness)
            imagePerVolume = int(collimationWidth / sliceThickness)
            numVolumes = int(numImages / imagePerVolume)

            print('Total number of DICOM images in provided driectory: ' + str(numImages))
            print('Found a total collimation width of: ' + str(collimationWidth))
            print('Found a slice thickness of: ' + str(sliceThickness))
            print('Number of images per volume: ' + str(imagePerVolume))
            print('Number of volumes is: ' + str(numVolumes))

            # Now create a new sub-directory for each volume
            for i in range(1, numVolumes + 1, 1):
                tempDir = os.path.join(inputDirectory, 'Volume_' + str(i))
                try:
                    os.mkdir(tempDir)
                except OSError as e:
                    if e.errno != errno.EEXIST:     # File already exists error
                        raise

    print('Moving images...')
        
    for DICOMfile in os.listdir(inputDirectory):
        # Get the next item in the directory
        nextItem = os.fsdecode(DICOMfile)

        # Skip any directories and loop over files only
        if os.path.isdir(nextItem):
            print('Skipping directory: ' + nextItem)
            continue

        filename, extension = os.path.splitext( nextItem )

        # Now loop through the images and copy them to the correct volume directory
        if extension == '.dcm':
            image = os.path.join(inputDirectory, nextItem)
            moveDICOM(image, imagePerVolume, inputDirectory)


if __name__ == '__main__':
    # Read in the input DICOM directory
    parser = argparse.ArgumentParser()
    parser.add_argument('inputDirectory', type=str, help='The input DICOM directory')
    args = parser.parse_args()

    inputDirectory = args.inputDirectory

    sortDYNACTVolumes(inputDirectory)
    print ("DONE!")