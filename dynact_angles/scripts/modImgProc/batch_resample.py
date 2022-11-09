"""
batch_resample.py

Created by: Michael Kuczynski
Created on: Aug. 07, 2019

Description: Batch resamples images based on specified user input parameters.

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
import argparse

from resample import Resample

"""


Parameters
----------
input_path : string

output_path : string

new_spacing : list

new_origin : list

new_size : list

new_direction : list
                    
interpolator : string
                    
output_data_type : int

Returns
-------

"""
def batch_resample(input_path, output_path, new_spacing, new_origin, new_size, 
                    new_direction, interpolator, output_data_type):
    try:
        os.makedirs( os.path.join(input_path[0:-10], 'RESAMPLED') )
    except FileExistsError:
        pass

    for next_dir in os.listdir(input_path) :
        output_path = os.path.join(os.path.join(input_path[0:-10], 'RESAMPLED'), next_dir + '_Resampled.nii')
        next_dir = os.path.join(input_path, next_dir)

        if os.path.isdir(next_dir):
            Resample(next_dir, output_path, new_spacing, new_origin, new_size, \
                    new_direction, interpolator, output_data_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resample an image using SimpleITK')
    parser.add_argument('input_path', help='The input image file path')
    parser.add_argument('output_path', help='The output image file path')
    parser.add_argument('new_spacing', nargs=3, type=float, help='The new voxel spacing')
    parser.add_argument('-o', '--origin', dest='new_origin', type=float, nargs=3, help='The new image origin')
    parser.add_argument('-s', '--size', dest='new_size', nargs=3, type=int, help='The new image size/dimensions')
    parser.add_argument('-d', '--direction', dest='new_direction', type=int, nargs=9, help='The new image direction')
    parser.add_argument('-i', '--interpolator', dest='interpolator', help='The interpolator to use')
    parser.add_argument('-t', '--type', dest='output_data_type', type=int, help='The resampled image data type')
    args = parser.parse_args()

    # Parse arguments
    input_path = args.input_path
    output_path = args.output_path
    new_spacing = args.new_spacing
    new_origin = args.new_origin
    new_size = args.new_size
    new_direction = args.new_direction
    interpolator = args.interpolator
    output_data_type = args.output_data_type

    batch_resample(input_path, output_path, new_spacing, new_origin, new_size, \
                    new_direction, interpolator, output_data_type)

    