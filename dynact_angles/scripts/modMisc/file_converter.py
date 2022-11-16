"""
file_converter.py

Created by: Michael Kuczynski
Created on: Jan. 21, 2020

Description: Converts between 3D image file formats. Current supported formats:
                1. DICOM
                2. NIFTI
                3. MHA
                4. AIM/ISQ
                5. NRRD
                6. TIFF
"""

import os
import itk
import sys
import argparse
import SimpleITK as sitk

from sitk_itk import sitk2itk, itk2sitk
from img_to_dicom import img_to_dicom


def fileConverter(input_img, output_img):
    """
    Converts between image file formats.

    Parameters
    ----------
    input_img : string

    output_img : string

    Returns
    -------

    """
    print("******************************************************")
    print(f"CONVERTING: {input_img} to {output_img}")

    # Extract directory, filename, basename, and extensions from the output image
    out_dir, out_filename = os.path.split(output_img)
    out_basename, out_ext = os.path.splitext(out_filename)

    # Check the output file format
    if out_ext.lower() == ".mha":
        output_img_filename = os.path.join(out_dir, out_basename + ".mha")
    elif out_ext.lower() == ".mhd" or out_ext.lower() == ".raw":
        output_img_filename = os.path.join(out_dir, out_basename + ".mhd")
        output_img_filename_RAW = os.path.join(out_dir, out_basename + ".raw")
    elif out_ext.lower() == ".nii" or out_ext.lower() == ".nii.gz":
        output_img_filename = os.path.join(out_dir, out_basename + ".nii")
    elif out_ext.lower() == ".nrrd":
        output_img_filename = os.path.join(out_dir, out_basename + ".nrrd")
    elif out_ext.lower() == ".dcm":
        output_img_filename = os.path.join(out_dir, out_basename + ".dcm")
    elif out_ext.lower() == ".tif":
        output_img_filename = os.path.join(out_dir, out_basename + ".tif")
    elif out_ext.lower() == ".isq":
        output_img_filename = os.path.join(out_dir, out_basename + ".ISQ")
    else:
        print()
        print("Error: output file extension must be MHD, MHA, RAW, NRRD, TIFF or NII.")
        sys.exit(1)

    # Check if the input is a DICOM series directory
    if os.path.isdir(input_img):
        # Check if the directory exists
        if not os.path.exists(input_img):
            print()
            print("Error: DICOM directory does not exist!")
            sys.exit(1)
        else:
            reader = sitk.ImageSeriesReader()

            # Convert to 16-bit Int to ensure compatibility with ITK-Python functions
            # Needed for writing TIFF images
            if out_ext.lower() == ".tif":
                reader.SetOutputPixelType(sitk.sitkInt16)

            dicom_names = reader.GetGDCMSeriesFileNames(input_img)
            reader.SetFileNames(dicom_names)

            output_img = reader.Execute()
    else:
        # Extract directory, filename, basename, and extensions from the input image
        in_dir, in_filename = os.path.split(input_img)
        in_basename, in_ext = os.path.splitext(in_filename)

        # AIM image file
        if ".aim" in in_ext.lower():
            # If the input AIM contains a version number, remove it and rename the file
            if ";" in in_ext.lower():
                input_img_new = input_img.rsplit(";", 1)[0]
                os.rename(input_img, input_img_new)
                input_img = input_img_new

            # Read in the AIM using ITK
            # Only support short images for now
            img_type = itk.Image[itk.ctype("signed short"), 3]
            reader = itk.ImageFileReader[img_type].New()
            img_io = itk.ScancoImageIO.New()
            reader.SetImageIO(img_io)
            reader.SetFileName(input_img)
            reader.Update()

            output_img = itk2sitk(reader.GetOutput())

        # ISQ image file
        elif ".isq" in in_ext.lower():
            # If the input ISQ contains a version number, remove it and rename the file
            if ";" in in_ext.lower():
                input_img_new = input_img.rsplit(";", 1)[0]
                os.rename(input_img, input_img_new)
                input_img = input_img_new

            # Read in the ISQ using ITK
            img_type = itk.Image[itk.ctype("signed short"), 3]
            reader = itk.ImageFileReader[img_type].New()
            img_io = itk.ScancoImageIO.New()
            reader.SetImageIO(img_io)
            reader.SetFileName(input_img)
            reader.Update()

            output_img = itk2sitk(reader.GetOutput())

        # Other image file (e.g., MHA, NII, NRRD)
        elif os.path.isfile(input_img) and (
            ".nii" or ".mha" or ".mhd" or ".raw" or ".nrrd" in in_ext.lower()
        ):
            # Convert to 16-bit Int to ensure compatibility with ITK-Python functions for writing TIFFs
            if out_ext.lower() == ".tif":
                output_img = sitk.ReadImage(input_img, sitk.sitkInt16)
            else:
                # Use unkown pixel type (may cause errors if the pixel type is not supported by ITK-Python)
                output_img = sitk.ReadImage(input_img, sitk.sitkInt16)

        else:
            print()
            print("Error: Input image is an incorrect type!")
            sys.exit(1)

    # Setup the correct writer based on the output image extension
    if out_ext.lower() == ".mha":
        print("WRITING IMAGE: " + str(output_img_filename))
        sitk.WriteImage(output_img, str(output_img_filename))

    elif out_ext.lower() == ".mhd" or out_ext.lower() == ".raw":
        print("WRITING IMAGE: " + str(output_img_filename))
        sitk.WriteImage(output_img, str(output_img_filename))

    elif out_ext.lower() == ".nii" or out_ext.lower() == ".nii.gz":
        print("WRITING IMAGE: " + str(output_img_filename))
        sitk.WriteImage(output_img, str(output_img_filename))

    elif out_ext.lower() == ".nrrd":
        print("WRITING IMAGE: " + str(output_img_filename))
        sitk.WriteImage(output_img, str(output_img_filename))

    elif out_ext.lower() == ".tif":
        # SimpleITK TIFFImageIO is a bit buggy (sometimes writes out binary images...)
        # Use ITK instead. Need to force the use of a supported ITK-Python pixel type. Signed short is used as default
        img_type = itk.Image[itk.SS, 3]

        # Need to convert to ITK image
        # Should be read in as signed short by default so we shouldn't need to cast
        image = sitk2itk(output_img)

        # Image values need to rescaled
        rescaler = itk.RescaleIntensityImageFilter[img_type, img_type].New()
        rescaler.SetInput(image)
        rescaler.SetOutputMinimum(0)
        pixel_type_maximum = itk.NumericTraits[itk.SS].max()
        rescaler.SetOutputMaximum(pixel_type_maximum)

        print("WRITING IMAGE: " + str(output_img_filename))
        writer = itk.ImageFileWriter[img_type].New()
        writer.SetFileName(str(output_img_filename))
        writer.SetInput(rescaler.GetOutput())
        writer.Update()

    elif out_ext.lower() == ".dcm":
        print("WRITING IMAGE: " + str(output_img_filename))
        img2dicom(output_img, out_dir)

    elif out_ext.lower() == ".isq":
        output_img_ISQ = sitk2itk(output_img)
        print("WRITING IMAGE: " + str(output_img_filename))

        img_type = itk.Image[itk.ctype("signed short"), 3]
        writer = itk.ImageFileWriter[img_type].New()
        img_io = itk.ScancoImageIO.New()
        writer.SetImageIO(img_io)
        writer.SetInput(output_img_ISQ)
        writer.SetFileName(output_img_filename)
        writer.Update()

        # Set header information
        img_io.SetEnergy(68)
        img_io.SetIntensity(1.47)
        img_io.SetReconstructionAlg(3)
        img_io.SetSite(4)
        img_io.SetScannerID(3401)
        img_io.SetPatientIndex(2567)
        img_io.SetMeasurementIndex(12778)
        img_io.SetSampleTime(100)
        img_io.SetScannerType(9)
        img_io.SetMuScaling(8192)
        img_io.SetNumberOfProjections(900)
        img_io.SetSliceIncrement(0.0609)
        img_io.SetSliceThickness(0.0609)
        # img_io.SetScanDistance(139852)
        # img_io.SetReferenceLine(109737)
        # img_io.SetNumberOfSamples(2304)
        # img_io.SetStartPosition()

        writer.Write()

    print("DONE")
    print("******************************************************")
    print()


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_img", type=str, help="The input image (path + filename)")
    parser.add_argument(
        "output_img", type=str, help="The output image (path + filename)"
    )
    args = parser.parse_args()

    input_img = args.input_img
    output_img = args.output_img

    fileConverter(input_img, output_img)
