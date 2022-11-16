"""
resample.py

Created by: Michael Kuczynski
Created on: Aug. 07, 2019

Description: Resamples input images based on specified user input parameters.

Modified by:        Michael Kuczynski
Modified on:        2020.26.08
Modification notes: Updated to use SimpleITK and take more optional arguments.

Usage:
  python resample.py Input_path Output_path SpacingX SpacingY SpacingZ

Optional arguments:
  -i interpolatorType       Accepted types: linear, spline, nearestneighbor, or gaussian
  -o New_origin              Must be a list of three values in the form: X, Y, Z
  -s new_size                Dimensions. Must be a list of three values in the form: X, Y, Z
  -d new_direction           Must be a list of nine values in the form: 1 0 0 1 0 0 1 0 0
  -t output_data_type         Select a valid output data type:
                                0=uint8, 1=int8, 2=uint16, 3=int16, 4=uint32, 5=int32
                                6=uint64, 7=int64, 8=float32, 9=float64, -1=unknown
"""

import os
import sys
import argparse
import SimpleITK as sitk

from sitk_interpolators import interp_dict, interp_dict_enum
from sitk_data_types import data_type_dict, sitk_pixelID_enum


def resample(
    input_path,
    output_path,
    new_spacing,
    new_origin,
    new_size,
    new_direction,
    interpolator,
    output_data_type,
):
    """
    Resamples an image using specified parameters.

    Parameters
    ----------

    Returns
    -------
    """
    print(input_path)
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(input_path)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()
    image_size = image.GetSize()
    image_origin = image.GetOrigin()
    image_spacing = image.GetSpacing()
    image_direction = image.GetDirection()
    image_data_type = image.GetPixelID()

    # Resampled image information
    output_path_abs = os.path.abspath(output_path)
    resampled_path = output_path_abs
    resampled_spacing = new_spacing

    # Check optional arguements
    if interpolator is None or interpolator.lower() not in interp_dict:
        print("** Invalid or no interpolator provided. Using: linear interpolator")
        sitk_interp = sitk.sitkLinear
    else:
        sitk_interp = interp_dict.get(interpolator.lower())
        print(
            "** Using: provided interpolator: " + str(interp_dict_enum.get(sitk_interp))
        )

    if new_origin is None:
        print(
            "** Invalid or no image origin provided. Using: "
            + str(image_origin)
            + " as the resampled origin"
        )
        resampled_origin = image_origin
    else:
        resampled_origin = new_origin
        print(
            "** Using provided origin: "
            + str(resampled_origin)
            + " as the resampled origin"
        )

    if new_direction is None:
        print(
            "** Invalid or no image direction provided. Using: "
            + str(image_direction)
            + " as the resampled direction"
        )
        resampled_direction = image_direction
    else:
        resampled_direction = new_direction
        print(
            "** Using provided direction: "
            + str(resampled_direction)
            + " as the resampled direction"
        )

    if new_size is None:
        print(
            "** Invalid or no image dimensions provided. Calculating new image size..."
        )

        # Formula to calculate new image dimensions:
        # newDim = oldDim * oldSpacing / new_spacing
        temp = [
            image_spacing[0] / resampled_spacing[0],
            image_spacing[1] / resampled_spacing[1],
            image_spacing[2] / resampled_spacing[2],
        ]
        temp = [
            int(temp[0] * image_size[0]),
            int(temp[1] * image_size[1]),
            int(temp[2] * image_size[2]),
        ]
        resampled_size = temp

        print("   Using new image dimensions of: " + str(resampled_size))
    else:
        resampled_size = new_size
        print("   Using provided image dimensions of: " + str(resampled_size))

    if output_data_type is None or output_data_type not in sitk_pixelID_enum:
        print(
            "** Invalid or no output data type provided. Using: "
            + str(image.GetPixelIDTypeAsString())
        )
        resampled_data_type = image_data_type
    else:
        resampled_data_type = output_data_type
        print(
            "** Using provided data type: "
            + str(sitk_pixelID_enum.get(resampled_data_type))
        )

    # Print some information about the image
    print()
    print("*******************************************************")
    print("Input Image Information:")
    print("Dimensions:  " + str(image_size))
    print("Spacing:     " + str(image_spacing))
    print("Origin:      " + str(image_origin))
    print("Direction:   " + str(image_direction))
    print("Data Type:   " + image.GetPixelIDTypeAsString())
    print("*******************************************************")
    print("Resampled Image Information:")
    print("Dimensions:   " + str(resampled_size))
    print("Spacing:      " + str(resampled_spacing))
    print("Origin:       " + str(resampled_origin))
    print("Direction:    " + str(resampled_direction))
    print("Data Type:    " + str(sitk_pixelID_enum.get(resampled_data_type)))
    print("Interpolator: " + str(interp_dict_enum.get(sitk_interp)))
    print("*******************************************************")
    print()

    # Resample the image
    print("** Resampling...")
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetSize(resampled_size)
    resample_filter.SetOutputOrigin(resampled_origin)
    resample_filter.SetOutputSpacing(resampled_spacing)
    resample_filter.SetOutputDirection(resampled_direction)
    resample_filter.SetInterpolator(sitk_interp)
    resample_filter.SetOutputPixelType(resampled_data_type)

    # Print resampling progress
    resample_filter.AddCommand(
        sitk.sitkProgressEvent,
        lambda: print(
            "\rProgress: {0:03.1f}%...".format(100 * resample_filter.GetProgress()),
            end="",
        ),
    )
    resample_filter.AddCommand(sitk.sitkProgressEvent, lambda: sys.stdout.flush())

    resampled_image = resample_filter.Execute(image)

    print("Done!")

    print("*******************************************************")
    print("Resample Information:")
    print(resample_filter)
    print("*******************************************************")
    print()

    # Write out the resampled image
    print("Writing resampled image to: " + str(resampled_path))
    sitk.WriteImage(resampled_image, resampled_path)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resample an image using SimpleITK")
    parser.add_argument("inputImage", help="The input image file path")
    parser.add_argument("outputImage", help="The output image file path")
    parser.add_argument(
        "new_spacing", nargs=3, type=float, help="The new voxel spacing"
    )
    parser.add_argument(
        "-o",
        "--origin",
        dest="new_origin",
        type=float,
        nargs=3,
        help="The new image origin",
    )
    parser.add_argument(
        "-s",
        "--size",
        dest="new_size",
        nargs=3,
        type=int,
        help="The new image size/dimensions",
    )
    parser.add_argument(
        "-d",
        "--direction",
        dest="new_direction",
        type=int,
        nargs=9,
        help="The new image direction",
    )
    parser.add_argument(
        "-i", "--interpolator", dest="interpolator", help="The interpolator to use"
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="output_data_type",
        type=int,
        help="The resampled image data type",
    )
    args = parser.parse_args()

    # Parse arguments
    inputImage = args.inputImage
    outputImage = args.outputImage
    new_spacing = args.new_spacing
    new_origin = args.new_origin
    new_size = args.new_size
    new_direction = args.new_direction
    interpolator = args.interpolator
    output_data_type = args.output_data_type

    # Input image information
    input_pathAbs = os.path.abspath(inputImage)

    resample(
        input_pathAbs,
        outputImage,
        new_spacing,
        new_origin,
        new_size,
        new_direction,
        interpolator,
        output_data_type,
    )
