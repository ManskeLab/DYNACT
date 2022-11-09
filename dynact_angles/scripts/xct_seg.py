"""
xct_seg.py

Created by:   Michael T. Kuczynski
Created on:   Jan. 11, 2021
"""

import os
import sys
import argparse
import numpy as np
import SimpleITK as sitk

# Some global variables for debugging
debug = False
output_path_debug = os.path.getcwd()
bone_debug = ''


"""
Runs a binary threshold on a grayscale image.

Parameters
----------
img : SimpleITK.Image

lower_thresh : int

upper_thresh : int

Returns
-------
seg_img : SimpleITK.Image
"""
def xct_threshold(img, lower_thresh, upper_thresh):
    print('Running global threshold...')
    seg = sitk.BinaryThresholdImageFilter()
    seg.SetLower_thresh(lower_thresh)
    seg.SetUpper_thresh(upper_thresh)
    seg.SetOutsideValue(0)
    seg.SetInsideValue(1)
    seg_img = seg.Execute(img)

    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_SEG.nii')
        sitk.WriteImage(seg_img, output_img_path)

    return seg_img


"""
Runs a binary median filter on a binary image.

Parameters
----------
img : SimpleITK.Image

kernel : list

Returns
-------
filtered_img : SimpleITK.Image
"""
def xct_binary_median_filter(img, kernel=[3,3,3]):
    print('Applying median filter...')

    filt = sitk.BinaryMedianImageFilter()
    filt.SetRadius(kernel)
    filtered_img = filt.Execute(img)

    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_FILTER.nii')
        sitk.WriteImage(filtered_img, output_img_path)

    return filtered_img


"""
Runs a opening operation on a binary image.

Parameters
----------
img : SimpleITK.Image

kernel : list

Returns
-------
open_img : SimpleITK.Image
"""
def xct_binary_open(img, kernel):
    print('Applying binary opening operation...')
    open_img = sitk.BinaryOpeningByReconstruction(img, kernel)

    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_OPEN.nii')
        sitk.WriteImage(open_img, output_img_path)

    return open_img


"""
Runs a closing operation on a binary image.

Parameters
----------
img : SimpleITK.Image

kernel : list

Returns
-------
close_img : SimpleITK.Image
"""
def xct_binary_close(img, kernel):
    print('Applying binary closing operation...')
    close_img = sitk.BinaryClosingByReconstruction(img, kernel)

    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_CLOSE.nii')
        sitk.WriteImage(close_img, output_img_path)

    return close_img


"""
Runs a hole filling operation on a binary image.

Parameters
----------
img : SimpleITK.Image

Returns
-------
fill_img : SimpleITK.Image
"""
def xct_binary_fill_holes(img, output_path):
    print('Filling holes...')
    fill = sitk.BinaryFillholeImageFilter()
    fill.SetForegroundValue(1)
    fill_img = fill.Execute(img)
    
    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_FILLHOLE.nii')
        sitk.WriteImage(fill_img, output_img_path)

    return fill_img


"""
Runs a connected component operation on a binary image and returns the largest
component (assumed to be the bone of interest).

Parameters
----------
img : SimpleITK.Image

Returns
-------
one_label_img : SimpleITK.Image
"""
def xct_connected_comp(img, output_path):
    print('Running connected components...')
    connected_comp = sitk.ConnectedComponentImageFilter()
    connected_comp_img = connected_comp.Execute(img)

    print('Relabeling components...')
    relabel = sitk.RelabelComponentImageFilter()
    relabel.SortByObjectSizeOn()
    relabel_img = relabel.Execute(connected_comp_img)

    print('Found {0} labels...'.format(relabel.GetNumberOfObjects()))
    print(relabel.GetSizeOfObjectsInPixels())

    if debug:
        output_img_path = os.path.join(output_path_debug, str(bone_debug) + '_RELABEL.nii')
        sitk.WriteImage(relabel_img, output_img_path)
    
    print('Removing extra labels...')
    one_label = sitk.BinaryThresholdImageFilter()
    one_label.SetLower_thresh(1)
    one_label.SetUpper_thresh(1)
    one_label.SetOutsideValue(0)
    one_label.SetInsideValue(1)
    one_label_img = one_label.Execute(relabel_img)

    return one_label_img


"""
Main function to run the segmentation process.

Parameters
----------
input_path : string

output_path : string

lower_thresh : int

upper_thresh : int

clean_output : string

final_closing_kernel : list

Returns
-------
final_img : SimpleITK.Image
"""
def main(input_path, lower_thresh, upper_thresh, clean_output, final_closing_kernel):
    img = sitk.ReadImage(input_path)

    # Threshold
    seg_img = xct_threshold(img, lower_thresh, upper_thresh)

    # Median filter
    filter_img = xct_binary_median_filter(seg_img)

    # Open and close
    cleaned_thresh_img = xct_binary_open(filter_img, [15, 15, 3])
    cleaned_thresh_img = xct_binary_close(cleaned_thresh_img, [3, 3, 3])

    # Fill holes
    fill_img = xct_binary_fill_holes(cleaned_thresh_img)

    # Write out image and check if bones are connected (manually)
    sitk.WriteImage(fill_img, clean_output)
    input("Press Enter to continue...")
    fill_img = sitk.ReadImage(clean_output)

    # Connected Components
    single_comp = xct_connected_comp(fill_img)

    # Close
    close_img = xct_binary_close(single_comp, final_closing_kernel)

    # Fill holes
    fill_img2 = xct_binary_fill_holes(close_img)

    # Median filter
    final_img = xct_binary_median_filter(fill_img2)

    return final_img


if __name__ == "__main__":
    # Read in the input arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('input_img_path', help='The input image file path')
    parser.add_argument('lower_thresh', default=3000, type=float)
    parser.add_argument('upper_thresh', default=15000, type=float)
    parser.add_argument('-d', '--debug', nargs='?', type=bool, default=False)
    args = parser.parse_args()

    # Parse arguments
    input_img_path = args.input_img_path
    lower_thresh = args.lower_thresh
    upper_thresh = args.upper_thresh
    debug = args.debug

    output_path = os.path.dirname(input_img_path)

    if debug:
        output_path_debug = output_path
        if 'MC1' in input_img_path:
            bone_debug = 'MC1'
        else:
            bone_debug = 'TRP'

    if 'MC1' in input_img_path:
        final_closing_kernel = [27,27,3]
        clean_output = os.path.join(output_path, 'MC1_CLEAN_IMAGE.nii')
        output_img = os.path.join(output_path, 'MC1_SEG.nii')
    else:
        final_closing_kernel = [19,19,3]
        clean_output = os.path.join(output_path, 'TRP_CLEAN_IMAGE.nii')
        output_img = os.path.join(output_path, 'TRP_SEG.nii')

    final_img = main(input_img_path, output_path, lower_thresh, upper_thresh, \
            clean_output, final_closing_kernel)

    # Write out the final image
    print('Writing out final segmentation...')
    sitk.WriteImage(final_img, output_img)
