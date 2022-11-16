"""
compute_motion.py

Created by:   Michael T. Kuczynski
Created on:   Jan. 11, 2021
"""

import os
import sys
import argparse
import numpy as np
import SimpleITK as sitk

from modMisc.colours import Colours
from modBiomech.calc_coord_systems import (
    calculate_mc1_scs,
    calculate_trp_scs,
    transform_point,
)

# Global variable for debugging
debug = False


def main(rater, next_scan):
    """
    Main function to compute joint angles and translations. Directory structure is
    assumed to follow a specific format to automate setup of files/folders used
    in the computation of joint motion.

    Parameters
    ----------
    rater : string
        String containing the name of the next rater to process

    next_scan : string
        String containing the next directory to process

    Returns
    -------
    arr : list
        A list containing the rotations and translations computed for the specified
        rater and scan
    """
    # -------------------------------------------------------#
    #   Step 1: Setup inputs                                #
    # -------------------------------------------------------#
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    point_dir = os.path.join(parent_dir, "points")
    point_dir = os.path.join(point_dir, "points_July2021")
    reg_dir = os.path.join(parent_dir, "reg")
    model_dir = os.path.join(parent_dir, "models")

    # HR-pQCT directories:
    xct_pnts_dir = os.path.join(point_dir, os.path.join(next_scan, "HR-pQCT"))
    ct2xct_reg_dir = os.path.join(
        reg_dir, os.path.join(next_scan, "staticCT_to_HR-pQCT")
    )
    xct_model_dir = os.path.join(model_dir, os.path.join(next_scan, "HR-pQCT"))

    # Static and Dynamic CT directories:
    ct_pnts_dir = os.path.join(point_dir, os.path.join(next_scan, "staticCT"))
    ct2dynact_reg_dir = os.path.join(
        reg_dir, os.path.join(next_scan, "staticCT_to_dynamicCT/B")
    )

    dynact_pnts_dir = os.path.join(point_dir, os.path.join(next_scan, "dynamicCT"))
    dynact_reg_dir = os.path.join(
        reg_dir, os.path.join(next_scan, "dynamicCT_frames/B/FinalTFMs")
    )

    if "3" in next_scan or "5" in next_scan or "7" in next_scan or "9" in next_scan:
        ct2dynact_reg_dir = os.path.join(
            reg_dir, os.path.join(next_scan, "staticCT_to_dynamicCT/C")
        )
        dynact_reg_dir = os.path.join(
            reg_dir, os.path.join(next_scan, "dynamicCT_frames/C/FinalTFMs")
        )

    ct_model_dir = os.path.join(model_dir, os.path.join(next_scan, "staticCT"))
    dynact_model_dir = os.path.join(model_dir, os.path.join(next_scan, "dynamicCT"))

    # -------------------------------------------------------#
    #   Step 2: Read in the points from text file           #
    # -------------------------------------------------------#
    # There should be 3 points for the MC1 and 4 for the TRP
    # Points are picked in the XCT space
    mc1_pnts_file = os.path.join(
        point_dir, str(next_scan) + "e_MC1_SCS_" + str(rater) + ".txt"
    )
    trp_pnts_file = os.path.join(
        point_dir, str(next_scan) + "e_TRP_SCS_" + str(rater) + ".txt"
    )

    mc1_pnts_list = [None] * 3
    trp_pnts_list = [None] * 4

    print(
        Colours.BLUE
        + "\t Reading in MC1 points: "
        + Colours.WHITE
        + "{}".format(mc1_pnts_file)
    )
    try:
        with open(mc1_pnts_file) as f:
            mc1_pnts_list = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(Colours.RED + "ERROR: File does not exist!" + Colours.WHITE)
        sys.exit(1)

    print(
        Colours.BLUE
        + "\t Reading in TRP points: "
        + Colours.WHITE
        + "{}".format(trp_pnts_file)
    )
    try:
        with open(trp_pnts_file) as f:
            trp_pnts_list = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(Colours.RED + "ERROR: File does not exist!" + Colours.WHITE)
        sys.exit(1)

    # Put the directories into lists to cleanly pass to the compute_angles function
    xct_dir_list = [xct_pnts_dir, ct2xct_reg_dir, xct_model_dir]
    ct_dir_list = [ct_pnts_dir, ct2dynact_reg_dir, ct_model_dir]
    dynact_dir_list = [dynact_pnts_dir, dynact_reg_dir, dynact_model_dir]

    # -------------------------------------------------------#
    #   Step 3: Transform XCT points to DYNACT space        #
    # -------------------------------------------------------#
    arr = xct_to_dynact_transform(
        xct_dir_list, ct_dir_list, dynact_dir_list, mc1_pnts_list, trp_pnts_list
    )

    return arr


def compute_angles(R_relative):
    """
    Function to compute joint rotations by decomposing the input rotation matrix.

    alpha (a) = abduction-adduction angle (X_MC1)
    beta  (b) = axial rotation (Floating axis)
    gama  (g) = flexion-extension (Z_TRP)

    Relative rotation matrix is assumed to have the following form:
    Rxyz = Rz * Ry * Rx
    Rxyz = [ cos(b)cos(g)   (sin(a)sin(b)cos(g) + cos(a)sin(g))   (-cos(a)sin(b)cos(g) + sin(a)sin(g)) ]
        [ -cos(b)sin(g)  (-sin(a)sin(b)sin(g) + cos(a)cos(g))   (cos(a)sin(b)sin(g) + sin(a)cos(g)) ]
        [ sin(b)                    -sin(a)cos(b)                         cos(a)cos(b)              ]

    Parameters
    ----------
    R_relative : list

    Returns
    -------
    angles : list
    """
    beta = np.arcsin(R_relative[2, 0])
    alpha = np.arcsin(-1 * R_relative[2, 1] / np.cos(beta))
    gama = np.arcsin(-1 * R_relative[1, 0] / np.cos(beta))

    angles = [alpha, beta, gama]
    return angles


def compute_translations(R_relative, curr_origin, prev_origin):
    """
    Computes joint translations at a specific DYNACT frame. Translations are
    computed for the origin of the MC1 relative to the TRP.

    Parameters
    ----------
    R_relative : list
        Matrix to move from the MC1 coordinates to the TRP coordinates

    curr_origin : list
        MC1 origin at the current DYNACT frame

    prev_origin : string
        MC1 origin at the previous DYNACT frame

    Returns
    -------
    translations : list
        List of the X, Y, and Z translations of the MC1 relative to the TRP

    transformed_origin : list
        Origin for the next frame
    """
    transformed_origin = R_relative.dot(
        np.array([float(curr_origin[0]), float(curr_origin[1]), float(curr_origin[2])])
    )

    t_x = str(float(transformed_origin[0]) - float(prev_origin[0]))
    t_y = str(float(transformed_origin[1]) - float(prev_origin[1]))
    t_z = str(float(transformed_origin[2]) - float(prev_origin[2]))

    translations = [t_x, t_y, t_z]
    return translations, transformed_origin


def dynact_frame_transform(
    dynact_reg_dir, mc1_pnts_dynact, trp_pnts_dynact, R_relative
):
    """
    Transform MC1 and TRP points from XCT to CT, CT to DYNACT frame #1, and
    between DYNACT frames. Joint angles and translations are then computed for
    each DYNACT frame.

    Parameters
    ----------
    dynact_reg_dir : list

    mc1_pnts_dynact : list
        Anatommical landmarks for the MC1.
        Contains 3 points: 1) LDT, 2) MDT, 3) M1TJ (origin)

    trp_pnts_dynact : list
        Anatommical landmarks for the TRP.
        Contains 4 points: 1) TM1J (origin), 2) TM2J, 3) TSTJ, 4) TDET

    Returns
    -------
    rotations : list
        The abduction/adduction, flexion/extension, and axial rotation angles

    translations : list
        The X, Y, and Z translations of the MC1
    """
    mc1_pnt1_dynact = mc1_pnts_dynact[0]
    mc1_pnt2_dynact = mc1_pnts_dynact[1]
    mc1_pnt3_dynact = mc1_pnts_dynact[2]
    trp_pnt1_dynact = trp_pnts_dynact[0]
    trp_pnt2_dynact = trp_pnts_dynact[1]
    trp_pnt3_dynact = trp_pnts_dynact[2]
    trp_pnt4_dynact = trp_pnts_dynact[3]

    # Abduction, flexion, and internal rotation are positive
    # Adduction, extension, and external rotation are negative
    angle_list = compute_angles(R_relative)
    ab_ad = np.rad2deg(angle_list[0])
    ax_rot = np.rad2deg(angle_list[1])
    flex_ext = np.rad2deg(angle_list[2])

    ab_ad_arr = np.arange(59).astype(str)
    flex_ext_arr = np.arange(59).astype(str)
    ax_rot_arr = np.arange(59).astype(str)
    o_x = np.arange(59).astype(str)
    o_y = np.arange(59).astype(str)
    o_z = np.arange(59).astype(str)
    t_x = np.arange(59).astype(str)
    t_y = np.arange(59).astype(str)
    t_z = np.arange(59).astype(str)

    ab_ad_arr.shape = (59, 1)
    flex_ext_arr.shape = (59, 1)
    ax_rot_arr.shape = (59, 1)
    o_x.shape = (59, 1)
    o_y.shape = (59, 1)
    o_z.shape = (59, 1)
    t_x.shape = (59, 1)
    t_y.shape = (59, 1)
    t_z.shape = (59, 1)

    ab_ad_arr[0] = str(ab_ad)
    flex_ext_arr[0] = str(flex_ext)
    ax_rot_arr[0] = str(ax_rot)

    transformed_origin = R_relative.dot(
        np.array(
            [
                float(mc1_pnt3_dynact[0]),
                float(mc1_pnt3_dynact[1]),
                float(mc1_pnt3_dynact[2]),
            ]
        )
    )
    o_x[0] = str(transformed_origin[0])
    o_y[0] = str(transformed_origin[1])
    o_z[0] = str(transformed_origin[2])

    if debug:
        print(Colours.BLUE + "\t Printing joint motion for frame #1:" + Colours.WHITE)
        print("\t Abduction-Adduction: " + str(ab_ad))
        print("\t Flexion-Extension: " + str(flex_ext))
        print("\t Internal-External Rotation: " + str(ax_rot))
        print()
        print("\t Translation X: " + str(o_x[0]))
        print("\t Translation Y: " + str(o_y[0]))
        print("\t Translation Z: " + str(o_z[0]))
        print()

    # Transform between DYNACT frames
    for i in range(2, 60):
        # Transform to the next DYNACT frame
        # MC1
        dynact_reg_path_mc1 = os.path.join(
            dynact_reg_dir, "VOLUME_REF_TO_" + str(i) + "_MC1_REG.tfm"
        )
        dynact_next_reg_mc1_tfm = sitk.ReadTransform(dynact_reg_path_mc1)

        mc1_pnt1_dynact_frame = transform_point(
            dynact_next_reg_mc1_tfm, mc1_pnt1_dynact
        )
        mc1_pnt2_dynact_frame = transform_point(
            dynact_next_reg_mc1_tfm, mc1_pnt2_dynact
        )
        mc1_pnt3_dynact_frame = transform_point(
            dynact_next_reg_mc1_tfm, mc1_pnt3_dynact
        )

        # TRP
        dynact_reg_path_trp = os.path.join(
            dynact_reg_dir, "VOLUME_REF_TO_" + str(i) + "_TRP_REG.tfm"
        )
        dynact_next_reg_trp_tfm = sitk.ReadTransform(dynact_reg_path_trp)

        trp_pnt1_dynact_frame = transform_point(
            dynact_next_reg_trp_tfm, trp_pnt1_dynact
        )
        trp_pnt2_dynact_frame = transform_point(
            dynact_next_reg_trp_tfm, trp_pnt2_dynact
        )
        trp_pnt3_dynact_frame = transform_point(
            dynact_next_reg_trp_tfm, trp_pnt3_dynact
        )
        trp_pnt4_dynact_frame = transform_point(
            dynact_next_reg_trp_tfm, trp_pnt4_dynact
        )

        # Calculate joint angles for testing
        # Matricies from these functions are returned in the following format:
        # [Xx  Xy  Xz]
        # [Yx  Yy  Yz]
        # [Zx  Zy  Zz]
        xct_mc1_scs = np.array(
            calculate_mc1_scs(
                [mc1_pnt1_dynact_frame, mc1_pnt2_dynact_frame, mc1_pnt3_dynact_frame]
            )
        )
        xct_trp_scs = np.array(
            calculate_trp_scs(
                [
                    trp_pnt1_dynact_frame,
                    trp_pnt2_dynact_frame,
                    trp_pnt3_dynact_frame,
                    trp_pnt4_dynact_frame,
                ]
            )
        )

        M_scs_MC1 = np.array([xct_mc1_scs[0], xct_mc1_scs[1], xct_mc1_scs[2]])
        M_scs_TRP = np.array([xct_trp_scs[0], xct_trp_scs[1], xct_trp_scs[2]])

        # Calculate angle of MC1 relative to TRP
        R_relative = np.linalg.inv(M_scs_TRP) * M_scs_MC1

        # Abduction, flexion, and internal rotation are positive
        # Adduction, extension, and external rotation are negative
        angle_list = compute_angles(R_relative)
        ab_ad = np.rad2deg(angle_list[0])
        ax_rot = np.rad2deg(angle_list[1])
        flex_ext = np.rad2deg(angle_list[2])

        # translation
        prev_origin = [o_x[i - 2], o_y[i - 2], o_z[i - 2]]
        t, o = compute_translations(R_relative, mc1_pnt3_dynact_frame, prev_origin)
        t_x[i - 1] = t[0]
        t_y[i - 1] = t[1]
        t_z[i - 1] = t[2]
        o_x[i - 1] = o[0]
        o_y[i - 1] = o[1]
        o_z[i - 1] = o[2]

        ab_ad_arr[i - 1] = str(ab_ad)
        flex_ext_arr[i - 1] = str(flex_ext)
        ax_rot_arr[i - 1] = str(ax_rot)

        # Keep commented out to reduce the processing time
        # if debug:
        #     print(Colours.BLUE + '\t Printing joint motion for frame #' + str(i-1) + ':' + Colours.WHITE)
        #     print('\t Abduction-Adduction: ' + str(ab_ad))
        #     print('\t Flexion-Extension: ' + str(flex_ext))
        #     print('\t Internal-External Rotation: ' + str(ax_rot))
        #     print()
        #     print('\t Translation X: ' + str(t_x[i-1]))
        #     print('\t Translation Y: ' + str(t_y[i-1]))
        #     print('\t Translation Z: ' + str(t_z[i-1]))
        #     print()

    rotations = [ab_ad_arr, flex_ext_arr, ax_rot_arr]
    translations = [t_x, t_y, t_z]
    return rotations, translations


def xct_to_dynact_transform(
    xct_dir_list, ct_dir_list, dynact_dir_list, mc1_pnts_list, trp_pnts_list
):
    """
    Transforms XCT points to the DYNACT space to compute joint motion.

    Parameters
    ----------
    xct_dir_list : list

    ct_dir_list : list

    dynact_dir_list : list

    mc1_pnts_list : list

    trp_pnts_list : list

    Returns
    -------
    arr : list
    """
    # ----------------------------------------------------------#
    #   Step 1: Setup directories, points, and XCT images      #
    # ----------------------------------------------------------#
    # Unpack the directory lists
    xct_pnts_dir = xct_dir_list[0]
    ct2xct_reg_dir = xct_dir_list[1]
    xct_model_dir = xct_dir_list[2]
    ct_pnts_dir = ct_dir_list[0]
    ct2dynact_reg_dir = ct_dir_list[1]
    ct_model_dir = ct_dir_list[2]
    dynact_pnts_dir = dynact_dir_list[0]
    dynact_reg_dir = dynact_dir_list[1]
    dynact_model_dir = dynact_dir_list[2]

    # Strip the list to create a seperate list for each point
    mc1_pnt1 = [float(s) for s in mc1_pnts_list[0].split(",")]
    mc1_pnt2 = [float(s) for s in mc1_pnts_list[1].split(",")]
    mc1_pnt3 = [float(s) for s in mc1_pnts_list[2].split(",")]

    trp_pnt1 = [float(s) for s in trp_pnts_list[0].split(",")]
    trp_pnt2 = [float(s) for s in trp_pnts_list[1].split(",")]
    trp_pnt3 = [float(s) for s in trp_pnts_list[2].split(",")]
    trp_pnt4 = [float(s) for s in trp_pnts_list[3].split(",")]

    if debug:
        print(Colours.PURPLE + "\t DEBUG: Directories being used:" + Colours.WHITE)
        print("\t xct_pnts_dir: " + str(xct_pnts_dir))
        print("\t ct2xct_reg_dir: " + str(ct2xct_reg_dir))
        print("\t xct_model_dir: " + str(xct_model_dir))
        print("\t ct_pnts_dir: " + str(ct_pnts_dir))
        print("\t ct2dynact_reg_dir: " + str(ct2dynact_reg_dir))
        print("\t ct_model_dir: " + str(ct_model_dir))
        print("\t dynact_pnts_dir: " + str(dynact_pnts_dir))
        print("\t dynact_reg_dir: " + str(dynact_reg_dir))
        print("\t dynact_model_dir: " + str(dynact_model_dir))
        print()
        print(Colours.PURPLE + "\t DEBUG: Points read in:" + Colours.WHITE)
        print("\t MC1:")
        print("\t (" + str(mc1_pnt1) + ")")
        print("\t (" + str(mc1_pnt2) + ")")
        print("\t (" + str(mc1_pnt3) + ")")
        print("\t TRP:")
        print("\t (" + str(trp_pnt1) + ")")
        print("\t (" + str(trp_pnt2) + ")")
        print("\t (" + str(trp_pnt3) + ")")
        print("\t (" + str(trp_pnt4) + ")")
        print()

    # ----------------------------------------------------------#
    #   Step 2: Transform points from XCT to CT image space    #
    # ----------------------------------------------------------#
    # Read in the CT to XCT transform
    # Nifti to ITK World coordinates (Flip X and Y axes to go from VTK to ITK coordinates)
    mc1_pnt1 = [-1 * mc1_pnt1[0], -1 * mc1_pnt1[1], mc1_pnt1[2]]
    mc1_pnt2 = [-1 * mc1_pnt2[0], -1 * mc1_pnt2[1], mc1_pnt2[2]]
    mc1_pnt3 = [-1 * mc1_pnt3[0], -1 * mc1_pnt3[1], mc1_pnt3[2]]

    trp_pnt1 = [-1 * trp_pnt1[0], -1 * trp_pnt1[1], trp_pnt1[2]]
    trp_pnt2 = [-1 * trp_pnt2[0], -1 * trp_pnt2[1], trp_pnt2[2]]
    trp_pnt3 = [-1 * trp_pnt3[0], -1 * trp_pnt3[1], trp_pnt3[2]]
    trp_pnt4 = [-1 * trp_pnt4[0], -1 * trp_pnt4[1], trp_pnt4[2]]

    # MC1
    ct2xct_path_mc1 = os.path.join(ct2xct_reg_dir, "CT2XCT_MC1_REG.tfm")
    ct2xct_mc1_tfm = sitk.ReadTransform(ct2xct_path_mc1)
    xct2ct_mc1_tfm = ct2xct_mc1_tfm.GetInverse()

    mc1_pnt1_ct = transform_point(xct2ct_mc1_tfm, mc1_pnt1)
    mc1_pnt2_ct = transform_point(xct2ct_mc1_tfm, mc1_pnt2)
    mc1_pnt3_ct = transform_point(xct2ct_mc1_tfm, mc1_pnt3)

    # TRP
    ct2xct_path_trp = os.path.join(ct2xct_reg_dir, "CT2XCT_TRP_REG.tfm")
    ct2xct_trp_tfm = sitk.ReadTransform(ct2xct_path_trp)
    xct2ct_trp_tfm = ct2xct_trp_tfm.GetInverse()

    trp_pnt1_ct = transform_point(xct2ct_trp_tfm, trp_pnt1)
    trp_pnt2_ct = transform_point(xct2ct_trp_tfm, trp_pnt2)
    trp_pnt3_ct = transform_point(xct2ct_trp_tfm, trp_pnt3)
    trp_pnt4_ct = transform_point(xct2ct_trp_tfm, trp_pnt4)

    if debug:
        print(
            Colours.PURPLE + "\t DEBUG: Points transformed to CT space:" + Colours.WHITE
        )
        print("\t MC1:")
        print("\t mc1_pnt1_ct: " + str(mc1_pnt1_ct))
        print("\t mc1_pnt2_ct: " + str(mc1_pnt2_ct))
        print("\t mc1_pnt3_ct: " + str(mc1_pnt3_ct))
        print("\t TRP:")
        print("\t trp_pnt1_ct: " + str(trp_pnt1_ct))
        print("\t trp_pnt2_ct: " + str(trp_pnt2_ct))
        print("\t trp_pnt3_ct: " + str(trp_pnt3_ct))
        print("\t trp_pnt4_ct: " + str(trp_pnt4_ct))
        print()

    # ----------------------------------------------------------#
    #   Step 3: Transform points from CT to DYNACT image space #
    # ----------------------------------------------------------#
    # Read in the CT to DYNACT (first frame) transform
    # MC1
    ct2dynact_path_mc1 = os.path.join(ct2dynact_reg_dir, "CT2DYNACT_MC1_REG.tfm")
    ct2dynact_mc1_tfm = sitk.ReadTransform(ct2dynact_path_mc1)

    mc1_pnt1_dynact = transform_point(ct2dynact_mc1_tfm, mc1_pnt1_ct)
    mc1_pnt2_dynact = transform_point(ct2dynact_mc1_tfm, mc1_pnt2_ct)
    mc1_pnt3_dynact = transform_point(ct2dynact_mc1_tfm, mc1_pnt3_ct)

    # TRP
    ct2dynact_path_trp = os.path.join(ct2dynact_reg_dir, "CT2DYNACT_TRP_REG.tfm")
    ct2dynact_trp_tfm = sitk.ReadTransform(ct2dynact_path_trp)

    trp_pnt1_dynact = transform_point(ct2dynact_trp_tfm, trp_pnt1_ct)
    trp_pnt2_dynact = transform_point(ct2dynact_trp_tfm, trp_pnt2_ct)
    trp_pnt3_dynact = transform_point(ct2dynact_trp_tfm, trp_pnt3_ct)
    trp_pnt4_dynact = transform_point(ct2dynact_trp_tfm, trp_pnt4_ct)

    if debug:
        print(
            Colours.PURPLE
            + "\t DEBUG: Points transformed to DYNACT space:"
            + Colours.WHITE
        )
        print("\t MC1:")
        print("\t mc1_pnt1_dynact: " + str(mc1_pnt1_dynact))
        print("\t mc1_pnt2_dynact: " + str(mc1_pnt2_dynact))
        print("\t mc1_pnt3_dynact: " + str(mc1_pnt3_dynact))
        print("\t TRP:")
        print("\t trp_pnt1_dynact: " + str(trp_pnt1_dynact))
        print("\t trp_pnt2_dynact: " + str(trp_pnt2_dynact))
        print("\t trp_pnt3_dynact: " + str(trp_pnt3_dynact))
        print("\t trp_pnt4_dynact: " + str(trp_pnt4_dynact))
        print()

    # Calculate joint angles for testing
    # Matricies from these functions are returned in the following format:
    # [Xx  Xy  Xz]
    # [Yx  Yy  Yz]
    # [Zx  Zy  Zz]
    xct_mc1_scs = np.array(
        calculate_mc1_scs([mc1_pnt1_dynact, mc1_pnt2_dynact, mc1_pnt3_dynact])
    )
    xct_trp_scs = np.array(
        calculate_trp_scs(
            [trp_pnt1_dynact, trp_pnt2_dynact, trp_pnt3_dynact, trp_pnt4_dynact]
        )
    )

    # Matricies for axes should be formatted as follows:
    # Rxyz = [Rz  Ry  Rx]
    # Rxyz = [Zx  Yx  Xx]
    #        [Zy  Yy  Xy]
    #        [Zz  Yz  Xz]
    M_scs_MC1 = np.array([xct_mc1_scs[0], xct_mc1_scs[1], xct_mc1_scs[2]])
    M_scs_TRP = np.array([xct_trp_scs[0], xct_trp_scs[1], xct_trp_scs[2]])

    # Calculate angle of MC1 relative to TRP
    R_relative = np.linalg.inv(M_scs_TRP) * M_scs_MC1

    if debug:
        print(Colours.PURPLE + "\t DEBUG: XCT coordinate systems:" + Colours.WHITE)
        print("\t M_scs_MC1: \n\t " + str(M_scs_MC1).replace("\n", "\n \t"))
        print("\t M_scs_TRP: \n\t " + str(M_scs_TRP).replace("\n", "\n \t"))
        print(
            Colours.PURPLE + "\t DEBUG: XCT relative rotation matrix:" + Colours.WHITE
        )
        print("\t R_relative: \n\t " + str(R_relative).replace("\n", "\n \t"))
        print()

    mc1_pnts_dynact = [mc1_pnt1_dynact, mc1_pnt2_dynact, mc1_pnt3_dynact]
    trp_pnts_dynact = [
        trp_pnt1_dynact,
        trp_pnt2_dynact,
        trp_pnt3_dynact,
        trp_pnt4_dynact,
    ]
    rotations, translations = dynact_frame_transform(
        dynact_reg_dir, mc1_pnts_dynact, trp_pnts_dynact, R_relative
    )

    ab_ad_arr = rotations[0]
    flex_ext_arr = rotations[1]
    ax_rot_arr = rotations[2]
    t_x = translations[0]
    t_y = translations[1]
    t_z = translations[2]

    arr = np.hstack([ab_ad_arr, flex_ext_arr, ax_rot_arr, t_x, t_y, t_z])
    return arr


if __name__ == "__main__":
    # Allow for extra output for debugging
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", nargs="?", type=bool, default=False)
    args = parser.parse_args()
    debug = args.debug

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(parent_dir, "models")
    output_dir = os.path.join(parent_dir, "output")

    rater_list = ["JJT", "TB", "MTK001", "MTK002", "MTK003"]
    header_arr = np.array(
        [
            [
                "Frame",
                "JJT_AbAd",
                "JJT_FlexExt",
                "JJT_Rot",
                "JJT_X",
                "JJT_Y",
                "JJT_Z",
                "TB_AbAd",
                "TB_FlexExt",
                "TB_Rot",
                "TB_X",
                "TB_Y",
                "TB_Z",
                "MTK_001_AbAd",
                "MTK_001_FlexExt",
                "MTK_001_Rot",
                "MTK_001_X",
                "MTK_001_Y",
                "MTK_001_Z",
                "MTK_002_AbAd",
                "MTK_002_FlexExt",
                "MTK_002_Rot",
                "MTK_002_X",
                "MTK_002_Y",
                "MTK_002_Z",
                "MTK_003_AbAd",
                "MTK_003_FlexExt",
                "MTK_003_Rot",
                "MTK_003_X",
                "MTK_003_Y",
                "MTK_003_Z",
            ]
        ],
        dtype=object,
    )
    frame_arr = np.arange(59).astype(str)
    frame_arr.shape = (59, 1)

    # Compute angles for each rater, for each scan
    for sub_dir in next(os.walk(model_dir))[1]:
        # Skip a few directories that aren't ready for processing
        if "DYNACT1_011" in sub_dir or "DYNACT1_001" in sub_dir or "Marker" in sub_dir:
            continue

        print(
            Colours.BOLD
            + "Computing angles for "
            + str(sub_dir)
            + "..."
            + Colours.WHITE
        )

        output_arr = frame_arr
        output_arr = np.hstack([output_arr, main(rater_list[0], sub_dir)])
        output_arr = np.hstack([output_arr, main(rater_list[1], sub_dir)])
        output_arr = np.hstack([output_arr, main(rater_list[2], sub_dir)])
        output_arr = np.hstack([output_arr, main(rater_list[3], sub_dir)])
        output_arr = np.hstack([output_arr, main(rater_list[4], sub_dir)])
        output_arr = np.vstack([header_arr, output_arr])
        output_arr = output_arr.astype(str)

        print(Colours.BOLD + "Writing out values to CSV..." + Colours.WHITE)
        print()
        output_csv = os.path.join(output_dir, str(sub_dir) + "_angles.csv")
        np.savetxt(output_csv, output_arr, delimiter=",", fmt="%s")

    print()
    print(Colours.BOLD + "Done!")
