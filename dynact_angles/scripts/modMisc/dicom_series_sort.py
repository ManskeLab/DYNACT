"""
dicom_series_sort.py

Created by: Michael Kuczynski
Created on: Aug. 09, 2019

Description: Sorts all DICOMs in the provided directory into subdirectories 
                based on the series description tag.
"""

import os
import sys
import errno
import pydicom
import argparse

from pydicom.errors import InvalidDicomError


def print_progress(iteration, total, prefix="", suffix="", decimals=1, bar_length=100):
    """
    Print iterations progress.

    Parameters
    ----------
    iteration : int
        Current iteration

    total : int
        Total iterations

    prefix : string
        Prefix string

    suffix : string
        Suffix string

    decimals : int
        Positive number of decimals in percent complete

    bar_length : int
        Character length of bar

    Returns
    -------

    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    sys.stdout.write("\r%s |%s| %s%s %s" % (prefix, bar, percents, "%", suffix)),

    if iteration == total:
        sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == "__main__":
    # Parse input arguements
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path", type=str, help="The input DICOM directory (compressed files)"
    )
    args = parser.parse_args()

    input_path = args.input_path

    # Check if the provided directory exists
    if not os.path.exists(input_path):
        print("Error: provided directory does not exist!")
        sys.exit(1)

    # Get the absolute path of the directory provided. Use os.path.join() to avoid slash direction issues between Mac, Linux, and Windows
    input_path_abs = os.path.abspath(input_path)

    # Get the number of files in a directory for the progress bar
    l = len(
        [
            name
            for name in os.listdir(input_path_abs)
            if os.path.isfile(os.path.join(input_path_abs, name))
        ]
    )

    # Counter for the progress bar
    i = 0

    # Loop through all DICOMs in the provided directory, rename, decompress, and copy to the appropriate directory
    for file in os.listdir(input_path_abs):
        filename = os.fsdecode(file)

        current_file_path = os.path.join(input_path_abs, filename)

        # Check if we have a file
        if os.path.isfile(current_file_path):

            # Read the DICOM file. Make sure we have a valid DICOM file...
            try:
                dicom = pydicom.dcmread(current_file_path)
            except InvalidDicomError:
                continue

            # Check transfer syntax tag in DICOM header to see if file is compressed or not
            # If the file is already decompressed, skip it
            tsUID = dicom.file_meta.TransferSyntaxUID

            # Get the file's tag and parse out the series description
            # Series description is located at [0x0008, 0x103e]
            # Use the instance number located at [0x0020, 0x0013] to rename the images
            series_description = str(dicom[0x0008, 0x103E].value).upper()
            instance_number = dicom[0x0020, 0x0013].value

            # Make the instance number have the same number of digits for all images
            instance_number_str = str(instance_number).rjust(4, "0")

            series_file_path = os.path.join(input_path_abs, series_description)
            new_file_name = "IM_" + instance_number_str + ".dcm"

            # Uncompressed Implicit VR Little-endian = 1.2.840.10008.1.2
            # Uncompressed Explicit VR Little-endian = 1.2.840.10008.1.2.1
            # Uncompressed Explicit VR Big-endian = 1.2.840.10008.1.2.2
            if not (
                (tsUID == "1.2.840.10008.1.2")
                or (tsUID == "1.2.840.10008.1.2.1")
                or (tsUID == "1.2.840.10008.1.2.2")
            ):
                dicom.decompress()

            # If the series description directory doesn't already exist, create one
            if not os.path.exists(series_file_path):
                os.makedirs(series_file_path)

            output_file_path = os.path.join(series_file_path, new_file_name)

            # Save the decompressed file
            try:
                dicom.save_as(output_file_path)
            except OSError as e:
                if e.errno != errno.ENOENT:  # No such file or directory error
                    print("ERROR: No such file or directory named " + output_file_path)
                    raise

            # Update progress bar
            print_progress(
                i + 1, l, prefix="Progress:", suffix="Complete", bar_length=50
            )
            i = i + 1
