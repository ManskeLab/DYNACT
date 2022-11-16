"""
transform.py

Created by:   Michael T. Kuczynski
Created on:   Feb. 21, 2020

Description: Transform an image using the provided SimpleITK.TFM file.

Usage: 
python transform.py fixedImage.ext movingImage.ext transformation.tfm

Optional Inputs:
    -o output_img : specify an output transformed image
    -i interpolator : specify an interpolator from interpolator_dict
    -r True : Invert the TFM matrix
"""

import os
import sys
import argparse
import SimpleITK as sitk

# Dictionary for interpolator types
interpolator_dict = {
    "nn": sitk.sitkNearestNeighbor,
    "linear": sitk.sitkLinear,
    "spline": sitk.sitkBSpline,
    "gaussian": sitk.sitkGaussian,
}


def check_extensions(fixed_img_path, moving_img_path, tfm_path):
    """
    Checks file extensions for both images and the transformation matrix to make
    sure images are either NII or MHA and the transformation matrix is a TFM file.

    Parameters
    ----------
    fixed_img_path : string

    moving_img_path : string

    tfm_path : string

    Returns
    -------

    """
    # Check file extensions
    # Images can only be .nii or .mha, transformation matrix can only be .tfm
    fixed_dir, fixed_filename = os.path.split(fixed_img_path)
    fixed_basename, fixed_ext = os.path.splitext(fixed_filename)

    moving_dir, moving_filename = os.path.split(moving_img_path)
    moving_basename, moving_ext = os.path.splitext(moving_filename)

    tfm_dir, tfm_filename = os.path.split(tfm_path)
    tfm_basename, tfm_ext = os.path.splitext(tfm_filename)

    if not (fixed_ext.lower() == ".mha" or fixed_ext.lower() == ".nii"):
        print()
        print(f"Error: Invalid file extension {fixed_ext} for: {fixed_img_path}")
        sys.exit(1)
    elif not (moving_ext.lower() == ".mha" or moving_ext.lower() == ".nii"):
        print()
        print(f"Error: Invalid file extension {moving_ext} for: {moving_img_path}")
        sys.exit(1)
    elif not (tfm_ext.lower() == ".tfm"):
        print()
        print(f"Error: Invalid file extension {tfm_ext} for: {tfm_path}")
        sys.exit(1)

    # Make sure expected files exist
    expected_files = [fixed_img_path, moving_img_path, tfm_path]
    for file_name in expected_files:
        if not os.path.isfile(file_name):
            print()
            print("Error: Could not find file: ")
            print(f"{file_name}")
            sys.exit(1)


def main(fixed_img_path, moving_img_path, tfm_path, inverse_tfm, interpolator):
    """
    Main function to transform images.

    Parameters
    ----------
    fixed_img_path : string

    moving_img_path : string

    tfm_path : SimpleITK.TFM

    inverse_tfm : bool

    interpolator : string

    Returns
    -------
    resampled : SimpleITK.Image
    """
    check_extensions(fixed_img_path, moving_img_path, tfm_path)

    print()
    print(f"TRANFORMING: \n{moving_img_path} \nto \n{fixed_img_path}")

    # Read in fixed image
    print()
    print("READING: ")
    print(f"{fixed_img_path}")
    fixed = sitk.ReadImage(fixed_img_path)

    # Read in moving image
    print("READING: ")
    print(f"{moving_img_path}")
    moving = sitk.ReadImage(moving_img_path)

    # Read in the transform
    print("READING: ")
    print(f"{tfm_path}")
    tmat = sitk.ReadTransform(tfm_path)

    if inverse_tfm:
        tmat = tmat.GetInverse()

    # Transform the moving image
    print()
    print("RESAMPLING: ")
    print(f"{moving_img_path}")
    resampled = sitk.Resample(
        moving, fixed, tmat, interpolator, 0.0, moving.GetPixelID()
    )

    return resampled


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("fixed_img", type=str, help="Fixed image (path + filename)")
    parser.add_argument(
        "moving_img", type=str, help="Moving image to be transformed (path + filename)"
    )
    parser.add_argument(
        "tfm", type=str, help="The transformation matrix .TFM file (path + filename)"
    )
    parser.add_argument(
        "-o",
        dest="output_file",
        type=str,
        default="",
        help="Output image (path + filename). Default = moving image directory",
    )
    parser.add_argument(
        "-i",
        dest="interpolator",
        type=str,
        default="linear",
        help="SimpleITK interpolator type (nn, linear, spline, or gaussian). Default = linear",
    )
    parser.add_argument(
        "-r",
        dest="inverse_tfm",
        default=False,
        help="Option to apply the inverse transform. Default = False",
    )
    args = parser.parse_args()

    fixed_img = args.fixed_img
    moving_img = args.moving_img
    tfm = args.tfm
    inverse_tfm = args.inverse_tfm
    output_file = args.output_file

    interpolator = (args.interpolator).lower()
    interpolator = interpolator_dict.get(interpolator)

    transformed_img = main(fixed_img, moving_img, tfm, inverse_tfm, interpolator)

    # If no output file or directory was provided, save the transformed image to the same directory as the moving image
    if not output_file:
        # Extract directory, filename, basename, and extensions from the output image
        output_dir, out_filename = os.path.split(moving_img)
        out_basename, output_ext = os.path.splitext(out_filename)
        output_file = os.path.join(output_dir, out_basename + "_TRANSF" + output_ext)

        print()
        print(
            "Warning: No output file name or directory provided. Writing transformed image to: "
        )
        print(f"{output_file}")

    print()
    print("WRITING: ")
    print(f"{output_file}")
    sitk.WriteImage(transformed_img, output_file)
