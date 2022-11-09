"""
scs_differences.py

Created by: Michael Kuczynski
Created on: 11-01-2021

Description: Calculates the angle between each axis of a SCS between two raters.
"""

import os
import sys
import argparse
import numpy as np
import SimpleITK as sitk

from modBiomech.calc_coord_systems import calculate_mc1_scs, calculate_trp_scs, transform_point
from modBiomech.scs_diff import scs_diff
from modMisc.colours import Colours

# Global variable for debugging
debug = False

"""
Main function to find the SCS differences between raters.

Parameters
----------
rater1 : string

rater2 : string

next_scan : string

Returns
-------
arr : numpy.array
"""
def main(rater1, rater2, next_scan):
    #-------------------------------------------------------#
    #   Step 1: Setup inputs                                #
    #-------------------------------------------------------#
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    point_dir  = os.path.join(parent_dir, 'points')
    point_dir  = os.path.join(point_dir, 'points_July2021')
    reg_dir    = os.path.join(parent_dir, 'reg')
    model_dir  = os.path.join(parent_dir, 'models')

    # HR-pQCT directories:
    xct_pnts_dir = os.path.join(point_dir, next_scan)
    xct_pnts_dir = os.path.join(xct_pnts_dir, 'HR-pQCT')
    ct2xct_reg_dir = os.path.join(reg_dir, next_scan)
    ct2xct_reg_dir = os.path.join(ct2xct_reg_dir, 'staticCT_to_HR-pQCT')
    xct_model_dir  = os.path.join(model_dir, next_scan)
    xct_model_dir  = os.path.join(xct_model_dir, 'HR-pQCT')

    # Static CT directories:
    ct_pnts_dir = os.path.join(point_dir, next_scan)
    ct_pnts_dir = os.path.join(ct_pnts_dir, 'staticCT')
    ct2dynact_reg_dir = os.path.join(reg_dir, next_scan)
    ct2dynact_reg_dir = os.path.join(ct2dynact_reg_dir, 'staticCT_to_dynamicCT')
    ct2dynact_reg_dir = os.path.join(ct2dynact_reg_dir, 'B')
    if '9' in next_scan:
        ct2dynact_reg_dir = os.path.join(reg_dir, next_scan)
        ct2dynact_reg_dir = os.path.join(ct2dynact_reg_dir, 'staticCT_to_dynamicCT')
        ct2dynact_reg_dir = os.path.join(ct2dynact_reg_dir, 'C')

    ct_model_dir = os.path.join(model_dir, os.path.join(next_scan, 'staticCT'))

    # Dyanmic CT directories:
    dynact_pnts_dir = os.path.join(point_dir, next_scan)
    dynact_pnts_dir = os.path.join(dynact_pnts_dir, 'dynamicCT')
    dynactReg_dir = os.path.join(reg_dir, next_scan)
    dynactReg_dir = os.path.join(dynactReg_dir, 'dynamicCT_frames')
    dynactReg_dir = os.path.join(dynactReg_dir, os.path.join('B', 'FinalTFMs'))
    if '9' in next_scan:
        dynactReg_dir = os.path.join(reg_dir, next_scan)
        dynactReg_dir = os.path.join(dynactReg_dir, 'dynamicCT_frames')
        dynactReg_dir = os.path.join(dynactReg_dir, os.path.join('C', 'FinalTFMs'))

    dynact_model_dir  = os.path.join(model_dir, os.path.join(next_scan, 'dynamicCT'))

    #-------------------------------------------------------#
    #   Step 2: Read in the points from text file           #
    #-------------------------------------------------------#
    # There should be 3 points for the MC1 and 4 for the TRP
    # Points are picked in the XCT space

    #---------------#
    # Rater 1 Data  #
    #---------------#
    mc1_pnts_file1 = os.path.join(point_dir, str(next_scan) + \
                                    'e_MC1_SCS_' + str(rater1) + '.txt')
    trp_pnts_file1 = os.path.join(point_dir, str(next_scan) + \
                                    'e_TRP_SCS_' + str(rater1) + '.txt')
    
    mc1_pnts_list1 = [None] * 3
    trp_pnts_list1 = [None] * 4

    print(Colours.BLUE + '\t Reading in MC1 points: ' + Colours.WHITE + \
            '{}'.format(mc1_pnts_file1))
    try:
        with open(mc1_pnts_file1) as f:
            mc1_pnts_list1 = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(Colours.RED + 'ERROR: File does not exist!' + Colours.WHITE)
        sys.exit(1)

    print(Colours.BLUE + '\t Reading in TRP points: ' + Colours.WHITE + \
            '{}'.format(trp_pnts_file1))
    try:
        with open(trp_pnts_file1) as f:
            trp_pnts_list1 = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(Colours.RED + 'ERROR: File does not exist!' + Colours.WHITE)
        sys.exit(1)

    #---------------#
    # Rater 2 Data  #
    #---------------#
    mc1_pnts_file2 = os.path.join(point_dir, str(next_scan) + \
                                    'e_MC1_SCS_' + str(rater2) + '.txt')
    trp_pnts_file2 = os.path.join(point_dir, str(next_scan) + \
                                    'e_TRP_SCS_' + str(rater2) + '.txt')

    mc1_pnts_list2 = [None] * 3
    trp_pnts_list2 = [None] * 4

    print(Colours.BLUE + '\t Reading in MC1 points: ' + Colours.WHITE + \
            '{}'.format(mc1_pnts_file2))
    try:
        with open(mc1_pnts_file2) as f:
            mc1_pnts_list2 = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(Colours.RED + 'ERROR: File does not exist!' + Colours.WHITE)
        sys.exit(1)

    print(Colours.BLUE + '\t Reading in TRP points: ' + Colours.WHITE + \
            '{}'.format(trp_pnts_file2))
    try:
        with open(trp_pnts_file2) as f:
            trp_pnts_list2 = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(Colours.RED + 'ERROR: File does not exist!' + Colours.WHITE)
        sys.exit(1)


    # Put the directories into lists to cleanly pass to the computeAngles function
    xct_dir_list    = [xct_pnts_dir, ct2xct_reg_dir, xct_model_dir]
    ct_dir_list     = [ct_pnts_dir, ct2dynact_reg_dir, ct_model_dir] 
    dynact_dir_list = [dynact_pnts_dir, dynactReg_dir, dynact_model_dir] 
    
    #-------------------------------------------------------#
    #   Step 3: Transform XCT points to DYNACT space        #
    #-------------------------------------------------------#
    arr = xct2Dynact_transform(xct_dir_list, ct_dir_list, dynact_dir_list, 
                                mc1_pnts_list1, trp_pnts_list1,
                                mc1_pnts_list2, trp_pnts_list2)

    return arr


"""
Transforms from the XCT image space to the DYNACT image space (including 
between frame transformation). This is done for both the MC1 and TRP.

Parameters
----------
xct_dir_list : list

ct_dir_list : list

dynact_dir_list : list

mc1_pnts_list1 : list

trp_pnts_list1 : list

mc1_pnts_list2 : list

trp_pnts_list2 : list

Returns
-------
arr : numpy.array
"""
def xct2Dynact_transform(xct_dir_list, ct_dir_list, dynact_dir_list, 
                            mc1_pnts_list1, trp_pnts_list1, 
                            mc1_pnts_list2, trp_pnts_list2):
    #----------------------------------------------------------#
    #   Step 1: Setup directories, points, and XCT images      #
    #----------------------------------------------------------#
    # Unpack the directory lists
    xct_pnts_dir      = xct_dir_list[0]
    ct2xct_reg_dir    = xct_dir_list[1]
    xct_model_dir     = xct_dir_list[2]
    ct_pnts_dir       = ct_dir_list[0]
    ct2dynact_reg_dir = ct_dir_list[1]
    ct_model_dir      = ct_dir_list[2]
    dynact_pnts_dir   = dynact_dir_list[0]
    dynactReg_dir     = dynact_dir_list[1]
    dynact_model_dir  = dynact_dir_list[2]

    # Strip the list to create a seperate list for each point
    # Rater 1
    mc1_pnt1_R1 = [float(s) for s in mc1_pnts_list1[0].split(',')]
    mc1_pnt2_R1 = [float(s) for s in mc1_pnts_list1[1].split(',')]
    mc1_pnt3_R1 = [float(s) for s in mc1_pnts_list1[2].split(',')]

    trp_pnt1_R1 = [float(s) for s in trp_pnts_list1[0].split(',')]
    trp_pnt2_R1 = [float(s) for s in trp_pnts_list1[1].split(',')]
    trp_pnt3_R1 = [float(s) for s in trp_pnts_list1[2].split(',')]
    trp_pnt4_R1 = [float(s) for s in trp_pnts_list1[3].split(',')]

    # Rater 2
    mc1_pnt1_R2 = [float(s) for s in mc1_pnts_list2[0].split(',')]
    mc1_pnt2_R2 = [float(s) for s in mc1_pnts_list2[1].split(',')]
    mc1_pnt3_R2 = [float(s) for s in mc1_pnts_list2[2].split(',')]

    trp_pnt1_R2 = [float(s) for s in trp_pnts_list2[0].split(',')]
    trp_pnt2_R2 = [float(s) for s in trp_pnts_list2[1].split(',')]
    trp_pnt3_R2 = [float(s) for s in trp_pnts_list2[2].split(',')]
    trp_pnt4_R2 = [float(s) for s in trp_pnts_list2[3].split(',')]
    
    # Sanity check
    if debug:
        print(Colours.PURPLE + '\t DEBUG: Directories being used:' + Colours.WHITE)
        print('\t xct_pnts_dir: ' + str(xct_pnts_dir))
        print('\t ct2xct_reg_dir: ' + str(ct2xct_reg_dir))
        print('\t xct_model_dir: ' + str(xct_model_dir))
        print('\t ct_pnts_dir: ' + str(ct_pnts_dir))
        print('\t ct2dynact_reg_dir: ' + str(ct2dynact_reg_dir))
        print('\t ct_model_dir: ' + str(ct_model_dir))
        print('\t dynact_pnts_dir: ' + str(dynact_pnts_dir))
        print('\t dynactReg_dir: ' + str(dynactReg_dir))
        print('\t dynact_model_dir: ' + str(dynact_model_dir))
        print()
        print(Colours.PURPLE + '\t DEBUG: Points read in:' + Colours.WHITE)
        print('\t RATER 1:')
        print('\t MC1:')
        print('\t (' + str(mc1_pnt1_R1) + ')')
        print('\t (' + str(mc1_pnt2_R1) + ')')
        print('\t (' + str(mc1_pnt3_R1) + ')')
        print('\t TRP:')
        print('\t (' + str(trp_pnt1_R1) + ')')
        print('\t (' + str(trp_pnt2_R1) + ')')
        print('\t (' + str(trp_pnt3_R1) + ')')
        print('\t (' + str(trp_pnt4_R1) + ')')
        print()
        print('\t RATER 2:')
        print('\t MC1:')
        print('\t (' + str(mc1_pnt1_R2) + ')')
        print('\t (' + str(mc1_pnt2_R2) + ')')
        print('\t (' + str(mc1_pnt3_R2) + ')')
        print('\t TRP:')
        print('\t (' + str(trp_pnt1_R2) + ')')
        print('\t (' + str(trp_pnt2_R2) + ')')
        print('\t (' + str(trp_pnt3_R2) + ')')
        print('\t (' + str(trp_pnt4_R2) + ')')
        print()

    #----------------------------------------------------------#
    #   Step 2: Get the SCS difference in the XCT space        #
    #----------------------------------------------------------#
    # First create the SCSs in the XCT space and get the angle between SCS axes
    # between rater. Do this agin in the DYNACT space.
    # Use [0, 0, 0] as the origin of the SCS (i.e., move all axes to this origin)
    # This origin will be used as its the origin of prinicple axes of each bone
    # Matricies from these functions are returned in the following format:
    # [Xx  Xy  Xz]
    # [Yx  Yy  Yz]
    # [Zx  Zy  Zz]
    xct_mc1_scs_R1 = np.array(calculate_mc1_scs([mc1_pnt1_R1, \
                                                mc1_pnt2_R1, \
                                                mc1_pnt3_R1], \
                                                [0,0,0]))
    xct_trp_scs_R1 = np.array(calculate_trp_scs([trp_pnt1_R1, \
                                                trp_pnt2_R1, \
                                                trp_pnt3_R1, \
                                                trp_pnt4_R1], \
                                                [0,0,0]))

    xct_mc1_scs_R2 = np.array(calculate_mc1_scs([mc1_pnt1_R2, \
                                                mc1_pnt2_R2, \
                                                mc1_pnt3_R2], \
                                                [0,0,0]))
    xct_trp_scs_R2 = np.array(calculate_trp_scs([trp_pnt1_R2, \
                                                trp_pnt2_R2, \
                                                trp_pnt3_R2, \
                                                trp_pnt4_R2], \
                                                [0,0,0]))

    # Rater differences
    # X
    x_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[0], xct_mc1_scs_R2[0]))
    x_diff_trp = str(scsDiff(xct_trp_scs_R1[0], xct_trp_scs_R2[0]))

    # Y
    y_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[1], xct_mc1_scs_R2[1]))
    y_diff_trp = str(scsDiff(xct_trp_scs_R1[1], xct_trp_scs_R2[1]))

    # Z
    z_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[2], xct_mc1_scs_R2[2]))
    z_diff_trp = str(scsDiff(xct_trp_scs_R1[2], xct_trp_scs_R2[2]))
    
    xct_arr = np.zeros(shape=(58,6))
    xct_arr[0] = np.array([x_diff_mc1, y_diff_mc1, z_diff_mc1, x_diff_trp, y_diff_trp, z_diff_trp])


    #----------------------------------------------------------#
    #   Step 3: Transform points from XCT to CT image space    #
    #----------------------------------------------------------#
    # Read in the CT to XCT transform
    # Nifti to ITK World coordinates (Flip X and Y axes to go from VTK to ITK coordinates)
    mc1_pnt1_R1 = [-1*mc1_pnt1_R1[0], -1*mc1_pnt1_R1[1], mc1_pnt1_R1[2]]
    mc1_pnt2_R1 = [-1*mc1_pnt2_R1[0], -1*mc1_pnt2_R1[1], mc1_pnt2_R1[2]]
    mc1_pnt3_R1 = [-1*mc1_pnt3_R1[0], -1*mc1_pnt3_R1[1], mc1_pnt3_R1[2]]
    trp_pnt1_R1 = [-1*trp_pnt1_R1[0], -1*trp_pnt1_R1[1], trp_pnt1_R1[2]]
    trp_pnt2_R1 = [-1*trp_pnt2_R1[0], -1*trp_pnt2_R1[1], trp_pnt2_R1[2]]
    trp_pnt3_R1 = [-1*trp_pnt3_R1[0], -1*trp_pnt3_R1[1], trp_pnt3_R1[2]]
    trp_pnt4_R1 = [-1*trp_pnt4_R1[0], -1*trp_pnt4_R1[1], trp_pnt4_R1[2]]

    mc1_pnt1_R2 = [-1*mc1_pnt1_R2[0], -1*mc1_pnt1_R2[1], mc1_pnt1_R2[2]]
    mc1_pnt2_R2 = [-1*mc1_pnt2_R2[0], -1*mc1_pnt2_R2[1], mc1_pnt2_R2[2]]
    mc1_pnt3_R2 = [-1*mc1_pnt3_R2[0], -1*mc1_pnt3_R2[1], mc1_pnt3_R2[2]]
    trp_pnt1_R2 = [-1*trp_pnt1_R2[0], -1*trp_pnt1_R2[1], trp_pnt1_R2[2]]
    trp_pnt2_R2 = [-1*trp_pnt2_R2[0], -1*trp_pnt2_R2[1], trp_pnt2_R2[2]]
    trp_pnt3_R2 = [-1*trp_pnt3_R2[0], -1*trp_pnt3_R2[1], trp_pnt3_R2[2]]
    trp_pnt4_R2 = [-1*trp_pnt4_R2[0], -1*trp_pnt4_R2[1], trp_pnt4_R2[2]]

    # MC1
    ct2xct_path_mc1 = os.path.join(ct2xct_reg_dir, 'CT2XCT_MC1_REG.tfm')
    ct2xct_mc1_tfm = sitk.ReadTransform(ct2xct_path_mc1)
    xct2ct_mc1_tfm = ct2xct_mc1_tfm.GetInverse()

    mc1_pnt1_ct_R1 = transform_point(xct2ct_mc1_tfm, mc1_pnt1_R1)
    mc1_pnt2_ct_R1 = transform_point(xct2ct_mc1_tfm, mc1_pnt2_R1)
    mc1_pnt3_ct_R1 = transform_point(xct2ct_mc1_tfm, mc1_pnt3_R1)

    mc1_pnt1_ct_R2 = transform_point(xct2ct_mc1_tfm, mc1_pnt1_R2)
    mc1_pnt2_ct_R2 = transform_point(xct2ct_mc1_tfm, mc1_pnt2_R2)
    mc1_pnt3_ct_R2 = transform_point(xct2ct_mc1_tfm, mc1_pnt3_R2)

    # TRP
    ct2xct_path_trp = os.path.join(ct2xct_reg_dir, 'CT2XCT_TRP_REG.tfm')
    ct2xct_trp_tfm = sitk.ReadTransform(ct2xct_path_trp)
    xct2ct_trp_tfm = ct2xct_trp_tfm.GetInverse()

    trp_pnt1_ct_R1 = transform_point(xct2ct_trp_tfm, trp_pnt1_R1)
    trp_pnt2_ct_R1 = transform_point(xct2ct_trp_tfm, trp_pnt2_R1)
    trp_pnt3_ct_R1 = transform_point(xct2ct_trp_tfm, trp_pnt3_R1)
    trp_pnt4_ct_R1 = transform_point(xct2ct_trp_tfm, trp_pnt4_R1)

    trp_pnt1_ct_R2 = transform_point(xct2ct_trp_tfm, trp_pnt1_R2)
    trp_pnt2_ct_R2 = transform_point(xct2ct_trp_tfm, trp_pnt2_R2)
    trp_pnt3_ct_R2 = transform_point(xct2ct_trp_tfm, trp_pnt3_R2)
    trp_pnt4_ct_R2 = transform_point(xct2ct_trp_tfm, trp_pnt4_R2)

    if debug:
        print(Colours.PURPLE + '\t DEBUG: Points transformed to CT space:' + Colours.WHITE)
        print('\t RATER 1:')
        print('\t MC1:')
        print('\t mc1Point1CT: ' + str(mc1_pnt1_ct_R1))
        print('\t mc1Point2CT: ' + str(mc1_pnt2_ct_R1))
        print('\t mc1Point3CT: ' + str(mc1_pnt3_ct_R1))
        print('\t TRP:')
        print('\t trpPoint1CT: ' + str(trp_pnt1_ct_R1))
        print('\t trpPoint2CT: ' + str(trp_pnt2_ct_R1))
        print('\t trpPoint3CT: ' + str(trp_pnt3_ct_R1))
        print('\t trpPoint4CT: ' + str(trp_pnt4_ct_R1))
        print()
        print('\t RATER 1:')
        print('\t MC1:')
        print('\t mc1Point1CT: ' + str(mc1_pnt1_ct_R2))
        print('\t mc1Point2CT: ' + str(mc1_pnt2_ct_R2))
        print('\t mc1Point3CT: ' + str(mc1_pnt3_ct_R2))
        print('\t TRP:')
        print('\t trpPoint1CT: ' + str(trp_pnt1_ct_R2))
        print('\t trpPoint2CT: ' + str(trp_pnt2_ct_R2))
        print('\t trpPoint3CT: ' + str(trp_pnt3_ct_R2))
        print('\t trpPoint4CT: ' + str(trp_pnt4_ct_R2))
        print()


    #----------------------------------------------------------#
    #   Step 3: Transform points from CT to DYNACT image space #
    #----------------------------------------------------------#
    # Read in the CT to DYNACT (first frame) transform
    # MC1
    ct2dynact_path_mc1 = os.path.join(ct2dynact_reg_dir, 'CT2DYNACT_MC1_REG.tfm')
    ct2dynact_mc1_tfm = sitk.ReadTransform(ct2dynact_path_mc1)

    mc1_pnt1_dynact_R1 = transform_point(ct2dynact_mc1_tfm, mc1_pnt1_ct_R1)
    mc1_pnt2_dynact_R1 = transform_point(ct2dynact_mc1_tfm, mc1_pnt2_ct_R1)
    mc1_pnt3_dynact_R1 = transform_point(ct2dynact_mc1_tfm, mc1_pnt3_ct_R1)

    mc1_pnt1_dynact_R2 = transform_point(ct2dynact_mc1_tfm, mc1_pnt1_ct_R2)
    mc1_pnt2_dynact_R2 = transform_point(ct2dynact_mc1_tfm, mc1_pnt2_ct_R2)
    mc1_pnt3_dynact_R2 = transform_point(ct2dynact_mc1_tfm, mc1_pnt3_ct_R2)

    # TRP
    ct2dynact_path_trp = os.path.join(ct2dynact_reg_dir, 'CT2DYNACT_TRP_REG.tfm')
    ct2dynact_trp_tfm = sitk.ReadTransform(ct2dynact_path_trp)

    trp_pnt1_dynact_R1 = transform_point(ct2dynact_trp_tfm, trp_pnt1_ct_R1)
    trp_pnt2_dynact_R1 = transform_point(ct2dynact_trp_tfm, trp_pnt2_ct_R1)
    trp_pnt3_dynact_R1 = transform_point(ct2dynact_trp_tfm, trp_pnt3_ct_R1)
    trp_pnt4_dynact_R1 = transform_point(ct2dynact_trp_tfm, trp_pnt4_ct_R1)

    trp_pnt1_dynact_R2 = transform_point(ct2dynact_trp_tfm, trp_pnt1_ct_R2)
    trp_pnt2_dynact_R2 = transform_point(ct2dynact_trp_tfm, trp_pnt2_ct_R2)
    trp_pnt3_dynact_R2 = transform_point(ct2dynact_trp_tfm, trp_pnt3_ct_R2)
    trp_pnt4_dynact_R2 = transform_point(ct2dynact_trp_tfm, trp_pnt4_ct_R2)

    if debug:
        print(Colours.PURPLE + '\t DEBUG: Points transformed to DYNACT space:' + Colours.WHITE)
        print('\t RATER 1:')
        print('\t MC1:')
        print('\t mc1Point1DYNACT: ' + str(mc1_pnt1_dynact_R1))
        print('\t mc1Point2DYNACT: ' + str(mc1_pnt2_dynact_R1))
        print('\t mc1Point3DYNACT: ' + str(mc1_pnt3_dynact_R1))
        print('\t TRP:')
        print('\t trpPoint1DYNACT: ' + str(trp_pnt1_dynact_R1))
        print('\t trpPoint2DYNACT: ' + str(trp_pnt2_dynact_R1))
        print('\t trpPoint3DYNACT: ' + str(trp_pnt3_dynact_R1))
        print('\t trpPoint4DYNACT: ' + str(trp_pnt4_dynact_R1))
        print()
        print('\t RATER 2:')
        print('\t MC1:')
        print('\t mc1Point1DYNACT: ' + str(mc1_pnt1_dynact_R2))
        print('\t mc1Point2DYNACT: ' + str(mc1_pnt2_dynact_R2))
        print('\t mc1Point3DYNACT: ' + str(mc1_pnt3_dynact_R2))
        print('\t TRP:')
        print('\t trpPoint1DYNACT: ' + str(trp_pnt1_dynact_R2))
        print('\t trpPoint2DYNACT: ' + str(trp_pnt2_dynact_R2))
        print('\t trpPoint3DYNACT: ' + str(trp_pnt3_dynact_R2))
        print('\t trpPoint4DYNACT: ' + str(trp_pnt4_dynact_R2))
        print()

    #----------------------------------------------------------#
    #   Step 4: Transform between DYNACT frames                #
    #----------------------------------------------------------#
    diff_mc1_arr = np.zeros(shape=(58,3))
    diff_trp_arr = np.zeros(shape=(58,3))

    for i in range(2,60):
        # Transform to the next DYNACT frame
        # MC1
        dynact_reg_path_mc1 = os.path.join(dynactReg_dir, 'VOLUME_REF_TO_' + str(i) + '_MC1_REG.tfm')
        dynact_next_reg_mc1_tfm = sitk.ReadTransform(dynact_reg_path_mc1)
        
        mc1_pnt1_dynact_frame_R1 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt1_dynact_R1)
        mc1_pnt2_dynact_frame_R1 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt2_dynact_R1)
        mc1_pnt3_dynact_frame_R1 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt3_dynact_R1)

        mc1_pnt1_dynact_frame_R2 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt1_dynact_R2)
        mc1_pnt2_dynact_frame_R2 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt2_dynact_R2)
        mc1_pnt3_dynact_frame_R2 = transform_point(dynact_next_reg_mc1_tfm, mc1_pnt3_dynact_R2)

        # TRP
        dynact_reg_path_trp = os.path.join(dynactReg_dir, 'VOLUME_REF_TO_' + str(i) + '_TRP_REG.tfm')
        dynact_next_reg_trp_tfm = sitk.ReadTransform(dynact_reg_path_trp)

        trp_pnt1_dynact_frame_R1 = transform_point(dynact_next_reg_trp_tfm, trp_pnt1_dynact_R1)
        trp_pnt2_dynact_frame_R1 = transform_point(dynact_next_reg_trp_tfm, trp_pnt2_dynact_R1)
        trp_pnt3_dynact_frame_R1 = transform_point(dynact_next_reg_trp_tfm, trp_pnt3_dynact_R1)
        trp_pnt4_dynact_frame_R1 = transform_point(dynact_next_reg_trp_tfm, trp_pnt4_dynact_R1)

        trp_pnt1_dynact_frame_R2 = transform_point(dynact_next_reg_trp_tfm, trp_pnt1_dynact_R2)
        trp_pnt2_dynact_frame_R2 = transform_point(dynact_next_reg_trp_tfm, trp_pnt2_dynact_R2)
        trp_pnt3_dynact_frame_R2 = transform_point(dynact_next_reg_trp_tfm, trp_pnt3_dynact_R2)
        trp_pnt4_dynact_frame_R2 = transform_point(dynact_next_reg_trp_tfm, trp_pnt4_dynact_R2)

        # Use [0, 0, 0] as the origin of the SCS (i.e., move all axes to this origin)
        # This origin will be used as its the origin of prinicple axes of each bone
        # Matricies from these functions are returned in the following format:
        # [Xx  Xy  Xz]
        # [Yx  Yy  Yz]
        # [Zx  Zy  Zz]
        xct_mc1_scs_R1 = np.array(calculate_mc1_scs([mc1_pnt1_dynact_frame_R1, \
                                                    mc1_pnt2_dynact_frame_R1, \
                                                    mc1_pnt3_dynact_frame_R1], \
                                                    [0,0,0]))
        xct_trp_scs_R1 = np.array(calculate_trp_scs([trp_pnt1_dynact_frame_R1, \
                                                    trp_pnt2_dynact_frame_R1, \
                                                    trp_pnt3_dynact_frame_R1, \
                                                    trp_pnt4_dynact_frame_R1], \
                                                    [0,0,0]))

        xct_mc1_scs_R2 = np.array(calculate_mc1_scs([mc1_pnt1_dynact_frame_R2, \
                                                    mc1_pnt2_dynact_frame_R2, \
                                                    mc1_pnt3_dynact_frame_R2], \
                                                    [0,0,0]))
        xct_trp_scs_R2 = np.array(calculate_trp_scs([trp_pnt1_dynact_frame_R2, \
                                                    trp_pnt2_dynact_frame_R2, \
                                                    trp_pnt3_dynact_frame_R2, \
                                                    trp_pnt4_dynact_frame_R2], \
                                                    [0,0,0]))
            
        # Rater differences
        # X
        x_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[0], xct_mc1_scs_R2[0]))
        x_diff_trp = str(scsDiff(xct_trp_scs_R1[0], xct_trp_scs_R2[0]))

        # Y
        y_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[1], xct_mc1_scs_R2[1]))
        y_diff_trp = str(scsDiff(xct_trp_scs_R1[1], xct_trp_scs_R2[1]))

        # Z
        z_diff_mc1 = str(scsDiff(xct_mc1_scs_R1[2], xct_mc1_scs_R2[2]))
        z_diff_trp = str(scsDiff(xct_trp_scs_R1[2], xct_trp_scs_R2[2]))

        diff_mc1_arr[i-2] = np.array([x_diff_mc1, y_diff_mc1, z_diff_mc1])
        diff_trp_arr[i-2] = np.array([x_diff_trp, y_diff_trp, z_diff_trp])

    arr = np.hstack([xct_arr, diff_mc1_arr, diff_trp_arr])
    return arr


if __name__ == "__main__":
    # Allow for extra output for debugging
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', nargs='?', type=bool, default=False)
    args = parser.parse_args()
    debug = args.debug

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(parent_dir, 'models')
    output_dir = os.path.join(parent_dir, 'output')

    raters = ['JJT', 'TB', 'MTK001', 'MTK002', 'MTK003']
    header_arr = np.array([['Frame', \
                            'JJT_TB_XCT_MC1_X', 'JJT_TB_XCT_MC1_Y', 'JJT_TB_XCT_MC1_Z', \
                            'JJT_TB_XCT_TRP_X', 'JJT_TB_XCT_TRP_Y', 'JJT_TB_XCT_TRP_Z', \
                            'JJT_TB_MC1_X', 'JJT_TB_MC1_Y', 'JJT_TB_MC1_Z', \
                            'JJT_TB_TRP_X', 'JJT_TB_TRP_Y', 'JJT_TB_TRP_Z', \
                            'JJT_MTK1_XCT_MC1_X', 'JJT_MTK1_XCT_MC1_Y', 'JJT_MTK1_XCT_MC1_Z', \
                            'JJT_MTK1_XCT_TRP_X', 'JJT_MTK1_XCT_TRP_Y', 'JJT_MTK1_XCT_TRP_Z', \
                            'JJT_MTK1_MC1_X', 'JJT_MTK1_MC1_Y', 'JJT_MTK1_MC1_Z', \
                            'JJT_MTK1_TRP_X', 'JJT_MTK1_TRP_Y', 'JJT_MTK1_TRP_Z', \
                            'TB_MTK1_XCT_MC1_X', 'TB_MTK1_XCT_MC1_Y', 'TB_MTK1_XCT_MC1_Z', \
                            'TB_MTK1_XCT_TRP_X', 'TB_MTK1_XCT_TRP_Y', 'TB_MTK1_XCT_TRP_Z', \
                            'TB_MTK1_MC1_X', 'TB_MTK1_MC1_Y', 'TB_MTK1_MC1_Z', \
                            'TB_MTK1_TRP_X', 'TB_MTK1_TRP_Y', 'TB_MTK1_TRP_Z', \
                            'MTK1_MTK2_XCT_MC1_X', 'MTK1_MTK2_XCT_MC1_Y', 'MTK2_MTK1_MC1_Z', \
                            'MTK1_MTK2_XCT_TRP_X', 'MTK1_MTK2_XCT_TRP_Y', 'MTK1_MTK2_XCT_TRP_Z', \
                            'MTK1_MTK2_MC1_X', 'MTK1_MTK2_MC1_Y', 'MTK2_MTK1_MC1_Z', \
                            'MTK1_MTK2_TRP_X', 'MTK1_MTK2_TRP_Y', 'MTK1_MTK2_TRP_Z', \
                            'MTK1_MTK3_XCT_MC1_X', 'MTK1_MTK3_XCT_MC1_Y', 'MTK1_MTK3_XCT_MC1_Z', \
                            'MTK1_MTK3_XCT_TRP_X', 'MTK1_MTK3_XCT_TRP_Y', 'MTK1_MTK3_XCT_TRP_Z', \
                            'MTK1_MTK3_MC1_X', 'MTK1_MTK3_MC1_Y', 'MTK1_MTK3_MC1_Z', \
                            'MTK1_MTK3_TRP_X', 'MTK1_MTK3_TRP_Y', 'MTK1_MTK3_TRP_Z', \
                            'MTK2_MTK3_XCT_MC1_X', 'MTK2_MTK3_XCT_MC1_Y', 'MTK2_MTK3_XCT_MC1_Z', \
                            'MTK2_MTK3_XCT_TRP_X', 'MTK2_MTK3_XCT_TRP_Y', 'MTK2_MTK3_XCT_TRP_Z', \
                            'MTK2_MTK3_MC1_X', 'MTK2_MTK3_MC1_Y', 'MTK2_MTK3_MC1_Z', \
                            'MTK2_MTK3_TRP_X', 'MTK2_MTK3_TRP_Y', 'MTK2_MTK3_TRP_Z']], dtype=object)
    frame_arr = np.arange(58).astype(str)
    frame_arr.shape = (58,1)

    # Compute angles for each rater, for each scan
    for sub_dir in next(os.walk(model_dir))[1]:
        # Skip a few directories that aren't ready for processing
        if 'DYNACT1_011' in sub_dir or 'DYNACT1_001' in sub_dir or 'Marker' in sub_dir:
            continue

        print(Colours.BOLD + 'Computing SCS for ' + str(sub_dir) + '...' + Colours.WHITE)

        output_arr = frame_arr
        # JJT vs TB
        output_arr = np.hstack([output_arr, main(raters[0], raters[1], sub_dir)])
        # JJT vs MTK1
        output_arr = np.hstack([output_arr, main(raters[0], raters[2], sub_dir)])
        # TB vs MTK1
        output_arr = np.hstack([output_arr, main(raters[1], raters[2], sub_dir)])
        # MTK1 vs MTK2
        output_arr = np.hstack([output_arr, main(raters[2], raters[3], sub_dir)])
        # MTK1 vs MTK3
        output_arr = np.hstack([output_arr, main(raters[2], raters[4], sub_dir)])
        # MTK2 vs MTK3
        output_arr = np.hstack([output_arr, main(raters[3], raters[4], sub_dir)])
        output_arr = np.vstack([header_arr, output_arr])
        output_arr = output_arr.astype(str)
        
        print(Colours.BOLD + 'Writing out values to CSV...' + Colours.WHITE)
        print()
        output_csv = os.path.join(output_dir, str(sub_dir) + '_scs.csv')
        np.savetxt(output_csv, output_arr, delimiter=',', fmt='%s')

    print()
    print(Colours.BOLD + 'Done!')