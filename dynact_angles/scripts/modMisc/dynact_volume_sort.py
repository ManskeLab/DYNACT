"""
dynact_volume_sort.py

Created by: Michael Kuczynski
Created on: July 20, 2020

Description: Sorts uncompressed DICOM images from dynamic CT scans by 
             frame/volume. The number of volumes is calculated as follows: 
                Volumes = (total # images) / (# images per volume)
                Volumes = (total # images) / (total collimation width / slice thickness)
"""

import os
import math
import errno
import shutil
import pydicom
import argparse


def move_dicom(img_path, image_per_volume, input_dir):
    """
    Moves DICOM images to a new directory.

    Parameters
    ----------
    img_path : string

    image_per_volume : int

    input_dir : string

    Returns
    -------

    """
    ds = pydicom.dcmread(img_path)
    instance_num = int(ds.InstanceNumber)

    image_volume = math.ceil(instance_num / image_per_volume)

    copyDir = os.path.join(input_dir, "Volume_" + str(image_volume))
    shutil.move(os.path.join(input_dir, img_path), copyDir)


def sort_dynact_volumes(input_directory):
    """
    Sorts DICOM images into separate folders for each volume.
    # volumes = (total # images) / (total collimation width / slice thickness)

    Parameters
    ----------
    input_directory : string

    Returns
    -------

    """
    # Calculate the number of volumes in the series using the first image in the directory as input
    # First count the number of DICOM files in the provided directory
    list_of_files = os.listdir(input_directory)
    num_images = len([x for x in list_of_files if x.endswith(".dcm")])

    collimation_width = 0
    slice_thickness = 0
    image_per_volume = 0
    num_volumes = 0

    # Use a boolean variable to get collimation width and slice thickness from the first DICOM read in
    first_image = True

    # Loop through the entire input folder
    # Get the tag of each DICOM image to analyze the series description
    # Finally, place the image into the correct volume directory
    for dicom_file in os.listdir(input_directory):
        # Get the next item in the directory
        next_item = os.fsdecode(dicom_file)

        # Skip any directories and loop over files only
        if os.path.isdir(next_item):
            print("Skipping directory: " + next_item)
            continue

        filename, extension = os.path.splitext(next_item)

        if first_image and extension == ".dcm":
            first_image = False
            image = os.path.join(input_directory, next_item)
            ds = pydicom.dcmread(image)
            collimation_width = int(ds.TotalCollimationWidth)
            slice_thickness = float(ds.SliceThickness)
            image_per_volume = int(collimation_width / slice_thickness)
            num_volumes = int(num_images / image_per_volume)

            print(
                "Total number of DICOM images in provided driectory: " + str(num_images)
            )
            print("Found a total collimation width of: " + str(collimation_width))
            print("Found a slice thickness of: " + str(slice_thickness))
            print("Number of images per volume: " + str(image_per_volume))
            print("Number of volumes is: " + str(num_volumes))

            # Now create a new sub-directory for each volume
            for i in range(1, num_volumes + 1, 1):
                temp_dir = os.path.join(input_directory, "Volume_" + str(i))
                try:
                    os.mkdir(temp_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:  # File already exists error
                        raise

    print("Moving images...")

    for dicom_file in os.listdir(input_directory):
        # Get the next item in the directory
        next_item = os.fsdecode(dicom_file)

        # Skip any directories and loop over files only
        if os.path.isdir(next_item):
            print("Skipping directory: " + next_item)
            continue

        filename, extension = os.path.splitext(next_item)

        # Now loop through the images and copy them to the correct volume directory
        if extension == ".dcm":
            image = os.path.join(input_directory, next_item)
            move_dicom(image, image_per_volume, input_directory)


if __name__ == "__main__":
    # Read in the input DICOM directory
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", type=str, help="The input DICOM directory")
    args = parser.parse_args()

    input_directory = args.input_directory

    sort_dynact_volumes(input_directory)
    print("DONE!")
