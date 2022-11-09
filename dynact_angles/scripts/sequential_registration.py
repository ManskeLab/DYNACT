"""
sequential_registration.py

Created by:   Michael Kuczynski
Created on:   July 20, 2020

Description: Register dynamic CT image frames using sequential registration.
"""

import os
import errno
import argparse
import numpy as np
import SimpleITK as sitk

"""
Prints the registration method's metric and optimizer position during the 
image registration process.

Parameters
----------
method : SimpleITK.ImageRegistrationMethod

Returns
-------

"""
def command_iteration(method) :
  print('{0:3} = {1:10.5f} : {2}'.format(method.GetOptimizerIteration(), \
                                            method.GetMetricValue(), \
                                            method.GetOptimizerPosition()))


"""
Loads all DYNACT images into an array.

Parameters
----------
dynact_dir : string

Returns
-------
dynact_img_list : list
"""
def get_dynact_images(dynact_dir):
    # Read in DYNACT images into an array
    # Array format:
    #       -dynact_img_list[i] = [volume_num, [MC1_SEG, TRP_SEG], grayscale_img]
    dynact_img_list = [None] * 60

    for i in range(1, 60, 1):
        # Get the next volume file
        next_file = os.path.join(dynact_dir, 'Volume_' + str(i) + '_Resampled.nii')
        next_file_abs_path = os.path.join(dynact_dir, next_file)

        if not os.path.isfile(next_file_abs_path):
            continue

        # Get the volume number
        if next_file[-16] == '_':
            volume_num = int(next_file[-15:-14])
        else:
            volume_num = int(next_file[-16:-14])

        # Read the image
        next_volume = sitk.ReadImage(next_file_abs_path, sitk.sitkFloat32)
        # print("Reading: {}".format(next_file_abs_path))

        # Add the SimpleITK image to the volume list
        # Use the volume number to avoid sorting
        dynact_img_list[volume_num-1] = [volume_num-1, [None]*2, next_volume]

    return dynact_img_list


"""
Resamples an input image (binary) using a reference image.

Parameters
----------
ref : SimpleITK.Image

img : SimpleITK.Image

Returns
-------
resampled : SimpleITK.Image
"""
def binary_resample(ref, img):
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetReferenceImage(ref)
    resample_filter.SetInterpolator(sitk.sitkNearestNeighbor)
    resample_filter.SetOutputPixelType(img.GetPixelID())
    resampled = resample_filter.Execute(img)
    
    return resampled


"""
Resamples an input image (binary) using a reference image and input TFM.

Parameters
----------
ref : SimpleITK.Image

img : SimpleITK.Image

tmat : SimpleITK.TFM

Returns
-------
resampled : SimpleITK.Image
"""
def binary_resample_tfm(ref, img, tmat):
    # FORMAT: sitk.Resample(imageToBeResampled, referenceImage, transformation, 
    #                       interpolator, defaultPixelValue, outputPixelType)
    resampled = sitk.Resample(img, ref, tmat, sitk.sitkNearestNeighbor, \
                                0.0, img.GetPixelID())
    
    return resampled


"""
Dilates a binary mask by a specified kernel size.

Parameters
----------
seg_img : SimpleITK.Image

kernel : list

Returns
-------
dilated_img : SimpleITK.Image
"""
def dilate_mask(seg_img, kernel=[15,15,1]):
    dilate = sitk.BinaryDilateImageFilter()
    dilate.SetKernelRadius(kernel)
    dilate.SetForegroundValue(1)
    dilated_img = dilate.Execute(seg_img)

    return dilated_img


"""
Masks an input image with a binary mask.

Parameters
----------
img : SimpleITK.Image

mask : SimpleITK.Image

Returns
-------
masked_img : SimpleITK.Image
"""
def mask_bone(img, mask):
    masked = sitk.MaskImageFilter()
    masked_img = masked.Execute(img, mask)

    return masked_img


"""
Computes the initial transform between fixed and moving images by matching by
the image geometric centres.

Parameters
----------
fixed : SimpleITK.Image

moving : SimpleITK.Image

Returns
-------
tmat : SimpleITK.TFM
"""
def initialize_tfm(fixed, moving):
    # FORMAT: CenteredTransformInitializer (fixedImage, movingImage, 
    #                                       transform, operationMode)
    tmat = sitk.CenteredTransformInitializer(fixed, moving, \
                                            sitk.Euler3DTransform(), \
                                            sitk.CenteredTransformInitializerFilter.GEOMETRY)

    return tmat


"""
Performs image registration between a fixed and moving image.

Parameters
----------
init_tmat : SimpleITK.TFM

fixed : SimpleITK.Image

moving : SimpleITK.Image

Returns
-------
final_tmat : SimpleITK.TFM
"""
def registration(init_tmat, fixed, moving):
    reg = sitk.ImageRegistrationMethod()

    # Similarity metric settings:
    reg.SetMetricAsMeanSquares()
    reg.SetMetricSamplingStrategy(reg.RANDOM)
    reg.SetMetricSamplingPercentage(0.0001)

    # Set Interpolator
    reg.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    reg.SetOptimizerAsPowell(numberOfIterations=100, valueTolerance=1e-22)
    reg.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    reg.SetShrinkFactorsPerLevel(shrinkFactors = [1, 1])
    reg.SetSmoothingSigmasPerLevel(smoothingSigmas=[1, 0])
    reg.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    reg.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(reg))

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    reg.SetInitialTransform(init_tmat, inPlace=False)

    # FORMAT: registration.Execute(fixedImage, movingImage)
    final_tmat = reg.Execute(fixed, moving)

    # Output the final metric value and the reason for stopping the optimizer
    print()
    print('Final metric value: {0}'.format(reg.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(reg.GetOptimizerStopConditionDescription()))
    print()

    return final_tmat


"""
Main function to perform the sequential image registration.

Parameters
----------
dynact_dir : string

mc1_seg : string

trp_seg : string

output_dir : string

Returns
-------

"""
def main(dynact_dir, mc1_seg, trp_seg, output_dir):
    dynact_img_list = get_dynact_images(dynact_img_list)

    # Read masks
    print('Reading in {}'.format(mc1_seg))
    mc1_seg_img = sitk.ReadImage(mc1_seg)
    print('Reading in {}'.format(trp_seg))
    trp_seg_img = sitk.ReadImage(trp_seg)

    # Create the output directories
    output_tmat_dir = os.path.join(output_dir, 'FinalTFMs')
    output_initial_transf_dir = os.path.join(output_dir, 'InitalTransformations')
    output_seg_dir = os.path.join(output_dir, 'RegisteredMasks')

    try:
        os.mkdir(output_tmat_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:     # Directory already exists error
            raise
    try:
        os.mkdir(output_initial_transf_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:     # Directory already exists error
            raise
    try:
        os.mkdir(output_seg_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:     # Directory already exists error
            raise

    # Resample the next MC1/TRP mask to match the DYNACT grayscale image
    mc1_seg_img_resampled = binary_resample(dynact_img_list[0][2], mc1_seg_img)
    trp_seg_img_resampled = binary_resample(dynact_img_list[0][2], trp_seg_img)

    # Crop the MC1 and TRP from the first frame
    # Dilate the MC1 and TRP segmentation masks
    dynact_img_list[0][1][0] = dilate_mask(mc1_seg_img_resampled)
    dynact_img_list[0][1][1] = dilate_mask(trp_seg_img_resampled)

    # Mask out each bone from the first frame
    masked_mc1_img = mask_bone(dynact_img_list[0][2], dynact_img_list[0][1][0])
    masked_trp_img = mask_bone(dynact_img_list[0][2], dynact_img_list[0][1][1])

    dynact_img_list[0][1][0] = mc1_seg_img_resampled
    dynact_img_list[0][1][1] = trp_seg_img_resampled

    dynact_full_mask_list = [None] * 60
    dynact_full_mask_list[0] = [mc1_seg_img, trp_seg_img]

    # Loop through all DYNACT frames and register the first volume to all other volumes
    # Registration is performed on the MC1 and TRP individually (to get frame 1 to all other frames TMAT)
    # Then, using ITK, find the transformation between each frame and the next frame using the centroid of each mask (to get between frame TMATs)
    ref_frame = dynact_img_list[0][2]
    ref_frame_mc1_mask = mc1_seg_img_resampled # Only used for cropping
    ref_frame_trp_mask = trp_seg_img_resampled # Only used for cropping
    ref_frame_mc1_masked = masked_mc1_img # Masked reference MC1
    ref_frame_trp_masked = masked_trp_img # Masked reference TRP
    ref_frame_mc1_full_mask = dynact_full_mask_list[0][0] # What we actually transform
    ref_frame_trp_full_mask = dynact_full_mask_list[0][1] # What we actually transform

    prev_frame_mc1_mask = mc1_seg_img_resampled
    prev_frame_trp_mask = trp_seg_img_resampled


    for i in range(0, len(dynact_img_list)-2):
        print('Registering volume {} to volume {}'.format(i+1, i+2))
        
        # Get the next frame
        previous_frame = dynact_img_list[i][2]
        current_frame = dynact_img_list[i+1][2]

        # Set the output file names
        # Keep number to match the input volume numbering (i.e., 1...60, not 0...59)
        mc1_inital_transf_path = os.path.join(output_initial_transf_dir, 'VOLUME_REF_TO_' + str(i+2) + '_MC1_INITAL_TRANSF.nii')
        trp_inital_transf_path = os.path.join(output_initial_transf_dir, 'VOLUME_REF_TO_' + str(i+2) + '_TRP_INITAL_TRANSF.nii')
        mc1_final_tfm_output_path = os.path.join(output_tmat_dir, 'VOLUME_REF_TO_' + str(i+2) + '_MC1_REG.tfm')
        trp_final_tfm_output_path = os.path.join(output_tmat_dir, 'VOLUME_REF_TO_' + str(i+2) + '_TRP_REG.tfm')
        mc1_final_image_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_MC1_REG.nii')
        trp_final_image_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_TRP_REG.nii')
        mc1_final_mask_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_MC1_MASK_REG.nii')
        trp_final_mask_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_TRP_MASK_REG.nii')
        mc1_final_full_mask_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_MC1_FULLMASK_REG.nii')
        trp_final_full_mask_output_path = os.path.join(output_seg_dir, 'VOLUME_REF_TO_' + str(i+2) + '_TRP_FULLMASK_REG.nii')


        # Initialize the registration by using the previous frame
        inital_transform_prev_to_current = initialize_tfm(current_frame, previous_frame)

        # Crop out the next_frame MC1 and TRP bones so the registration method has less area to iterate over
        # Mask the current frame MC1 and TRP
        mc1_seg_inital_transform_prev_to_curr = binary_resample_tfm(current_frame, prev_frame_mc1_mask, inital_transform_prev_to_current)
        trp_seg_inital_transform_prev_to_curr = binary_resample_tfm(current_frame, prev_frame_trp_mask, inital_transform_prev_to_current)

        mc1_current_frame_dilate_img = dilate_mask(mc1_seg_inital_transform_prev_to_curr)
        trp_current_frame_dilate_img = dilate_mask(trp_seg_inital_transform_prev_to_curr)

        mc1_current_frame_gray_masked = mask_bone(current_frame, mc1_current_frame_dilate_img)
        trp_current_frame_gray_masked = mask_bone(current_frame, trp_current_frame_dilate_img)

        inital_transform_ref_to_current_mc1 = initialize_tfm(mc1_current_frame_gray_masked, ref_frame_mc1_masked)
        inital_transform_ref_to_current_trp = initialize_tfm(trp_current_frame_gray_masked, ref_frame_trp_masked)

        # Start the registration
        # MC1
        final_tfm_mc1 = registration(inital_transform_ref_to_current_mc1, mc1_current_frame_gray_masked, ref_frame_mc1_masked)
        final_tfm_trp = registration(inital_transform_ref_to_current_trp, trp_current_frame_gray_masked, ref_frame_trp_masked)
        
        print('Writing to {}'.format(mc1_final_tfm_output_path))
        sitk.WriteTransform(final_tfm_mc1, mc1_final_tfm_output_path)

        print('Writing to {}'.format(trp_final_tfm_output_path))
        sitk.WriteTransform(final_tfm_trp, trp_final_tfm_output_path)

        # Resample images
        print('Resampling MC1')
        mc1_current_gray_resampled = binary_resample_tfm(current_frame, ref_frame_mc1_masked, final_tfm_mc1)
        mc1_current_seg_full_resampled = sitk.Resample(ref_frame_mc1_full_mask, current_frame.GetSize(),
                                    final_tfm_mc1, 
                                    sitk.sitkNearestNeighbor,
                                    ref_frame_mc1_full_mask.GetOrigin(),
                                    ref_frame_mc1_full_mask.GetSpacing(),
                                    ref_frame_mc1_full_mask.GetDirection(),
                                    0,
                                    ref_frame_mc1_full_mask.GetPixelID())

        print('Writing to {}'.format(mc1_final_image_output_path))
        sitk.WriteImage(mc1_current_gray_resampled, mc1_final_image_output_path)
        sitk.WriteImage(mc1_current_seg_full_resampled, mc1_final_full_mask_output_path)


        print('Resampling TRP')
        trp_current_gray_resampled = binary_resample_tfm(current_frame, ref_frame_trp_masked, final_tfm_trp)
        trp_current_seg_full_resampled = sitk.Resample(ref_frame_trp_full_mask, current_frame.GetSize(),
                                    final_tfm_trp, 
                                    sitk.sitkNearestNeighbor,
                                    ref_frame_trp_full_mask.GetOrigin(),
                                    ref_frame_trp_full_mask.GetSpacing(),
                                    ref_frame_trp_full_mask.GetDirection(),
                                    0,
                                    ref_frame_trp_full_mask.GetPixelID())

        print('Writing to {}'.format(trp_final_image_output_path))
        sitk.WriteImage(trp_current_gray_resampled, trp_final_image_output_path)
        sitk.WriteImage(trp_current_seg_full_resampled, trp_final_full_mask_output_path)

        prev_frame_mc1_mask = mc1_current_seg_full_resampled
        prev_frame_trp_mask = trp_current_seg_full_resampled


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dynact_dir', type=str)
    parser.add_argument('mc1_seg', type=str)
    parser.add_argument('trp_seg', type=str)
    parser.add_argument('output_dir', type=str)
    args = parser.parse_args()

    dynact_dir = args.dynact_dir
    mc1_seg = args.mc1_seg
    trp_seg = args.trp_seg
    output_dir = args.output_dir

    main(dynact_dir, mc1_seg, trp_seg, output_dir)
