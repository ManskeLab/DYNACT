"""
xct2ct_reg.py

Created by: Michael Kuczynski
Created on: 27-07-2020

Description: Perform XCT to clinical CT image registration.
				First, an initial alignment of images is obtained through a 
				landmark based, rigid 3D transformation. Final image alignment
				is obtained with by optimizing the mutual information between
            	images.

Usage: 
python xct2ct_reg.py fixed_image.nii fixed_landmarks.nii moving_image.nii moving_landmarks.nii
"""

import os
import argparse
import SimpleITK as sitk


def command_iteration(method):
    """
    Prints the registration metric value during image registration.

    Parameters
    ----------
    method : SimpleITK.ImageRegistrationMethod

    Returns
    -------

    """
    print(
        "{0:3} = {1:10.5f} : {2}".format(
            method.GetOptimizerIteration(),
            method.GetMetricValue(),
            method.GetOptimizerPosition(),
        )
    )


def get_landmark(img):
    """
    Function to get landmarks points from the binary landmark image. Must provide 3
    landmarks in the landmark image.

    Parameters
    ----------
    img : SimpleITK.Image

    Returns
    -------
    landmarks : list
    """
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.ComputeOrientedBoundingBoxOn()
    stats.Execute(img)

    num_labels = stats.GetNumberOfLabels()
    if num_labels != 3:
        os.sys.exit("[ERROR] Only found {} labels, not 3".format(num_labels))

    landmarks = []
    for label in stats.GetLabels():
        landmarks.append(stats.GetOrientedBoundingBoxOrigin(label))

    return landmarks


def initialize_registration(fixed_landmarks, moving_landmarks):
    """
    Get the initial transform for the registration method by finding the transform
    between the fixed and moving landmarks.

    Parameters
    ----------
    fixed_landmarks : list

    moving_landmarks : list

    Returns
    -------
    ref_transform : SimpleITK.TFM
    """
    # Initialize transforms
    print("Performing initial transform")
    fixed_fiducial_points_flat = [c for p in fixed_landmarks for c in p]
    moving_fiducial_points_flat = [c for p in moving_landmarks for c in p]

    ref_transform = sitk.LandmarkBasedTransformInitializer(
        sitk.Similarity3DTransform(),
        fixed_fiducial_points_flat,
        moving_fiducial_points_flat,
    )

    # For debugging
    # sitk.WriteImage(sitk.Resample(moving_image, fixed_image,
    # 								ref_transform,
    # 								sitk.sitkLinear, 0.0,
    # 								moving_image.GetPixelID()),
    # 								moving_image_registered_path)

    print("fixed moving reference transform")
    print(ref_transform)

    return ref_transform


def image_registration(fixed_img, moving_img, ref_transform):
    """
    Function to perform the image registration.

    Parameters
    ----------
    fixed_image : SimpleITK.Image

    moving_image : SimpleITK.Image

    ref_transform : SimpleITK.TFM

    Returns
    -------
    final_transform : SimpleITK.TFM
    """
    # Set up registration
    reg = sitk.ImageRegistrationMethod()

    # Similarity metric settings:
    reg.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    reg.SetMetricSamplingStrategy(reg.RANDOM)
    reg.SetMetricSamplingPercentage(0.01)

    # Set Interpolator
    reg.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    reg.SetOptimizerAsPowell(numberOfIterations=300, valueTolerance=1e-18)
    reg.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    reg.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    reg.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    reg.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    reg.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(reg))

    # Perform the registration
    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    reg.SetInitialTransform(ref_transform, inPlace=False)
    print("Start registration")

    # registration.Execute(fixedImage, movingImage)
    final_transform = reg.Execute(fixed_img, moving_img)
    print("Final metric value: {0}".format(reg.GetMetricValue()))
    print(
        "Optimizer's stopping condition, {0}".format(
            reg.GetOptimizerStopConditionDescription()
        )
    )

    return final_transform


def main(fixed_landmarks_path, moving_landmarks_path, fixed_img_path, moving_img_path):
    """
    Main function to start the registration process.

    Parameters
    ----------
    fixed_landmarks_path : string

    moving_landmarks_path : string

    fixed_img_path : string

    moving_img_path : string

    Returns
    -------
    moving_resampled : SimpleITK.Image
    """
    # Read in landmarks
    print("Reading in {}".format(fixed_landmarks_path))
    fixed_landmarks_reader = sitk.ReadImage(fixed_landmarks_path, sitk.sitkUInt8)

    print("Reading in {}".format(moving_landmarks_path))
    moving_landmarks_reader = sitk.ReadImage(moving_landmarks_path, sitk.sitkUInt8)

    print("Getting fixed landmarks")
    fixed_landmarks = get_landmark(fixed_landmarks_reader)
    print("  fixed Landmarks: {}".format(fixed_landmarks))

    print("Getting moving landmarks")
    moving_landmarks = get_landmark(moving_landmarks_reader)
    print("  moving Landmarks: {}".format(moving_landmarks))

    # Read images
    print("Reading in {}".format(fixed_img_path))
    fixed_img = sitk.ReadImage(fixed_img_path, sitk.sitkFloat64)

    print("Reading in {}".format(moving_img_path))
    moving_img = sitk.ReadImage(moving_img_path, sitk.sitkFloat64)

    # Perform landmark transformation
    ref_transform = initialize_registration(fixed_landmarks, moving_landmarks)

    # Setup registration method
    final_transform = image_registration(fixed_img, moving_img, ref_transform)

    print("Writing to {}".format(moving_img_tmat_path))
    sitk.WriteTransform(final_transform, moving_img_tmat_path)

    # Resample and write registered image
    print("Resampling")
    # sitk.Resample(imageToBeResampled, referenceImage, transformation, \
    # 				interpolator, defaultPixelValue, outputPixelType)
    moving_resampled = sitk.Resample(
        moving_img,
        fixed_img,
        final_transform,
        sitk.sitkLinear,
        0.0,
        moving_img.GetPixelID(),
    )

    return moving_resampled


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "fixed_img_path", type=str, help="The fixed image (path + filename)"
    )
    parser.add_argument(
        "fixed_landmarks_path",
        type=str,
        help="The fixed landmarks (segmentation)  image (path + filename)",
    )
    parser.add_argument(
        "moving_img_path", type=str, help="The moving image (path + filename)"
    )
    parser.add_argument(
        "moving_landmarks_path",
        type=str,
        help="The moving landmarks (segmentation)  image (path + filename)",
    )
    parser.add_argument(
        "output_path",
        nargs="?",
        type=str,
        help="The directory for any outputs",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    fixed_img_path = args.fixed_img_path
    fixed_landmarks_path = args.fixed_landmarks_path
    moving_img_path = args.moving_img_path
    moving_landmarks_path = args.moving_landmarks_path
    output_path = args.output_path

    # Registered moving image and transformation matrix:
    if "mc1" in fixed_img_path.lower() or "mc1" in moving_img_path.lower():
        bone = "MC1"
    else:
        bone = "TRP"

    if "fixed" in fixed_img_path.lower():
        scan = "CT2XCT"
    else:
        scan = "CT2DYNACT"

    moving_img_registered_path = os.path.join(
        output_path, scan + "_" + bone + "_REG.nii"
    )
    moving_img_tmat_path = os.path.join(output_path, scan + "_" + bone + "_REG.tfm")

    moving_resampled = main(
        fixed_landmarks_path, moving_landmarks_path, fixed_img_path, moving_img_path
    )

    print("Writing to {}".format(moving_img_registered_path))
    sitk.WriteImage(moving_resampled, moving_img_registered_path)
