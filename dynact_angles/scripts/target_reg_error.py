"""
target_reg_error.py

Created by: Michael Kuczynski
Created on: Sept. 01, 2021
"""

import itk
import math
import argparse
import numpy as np
import SimpleITK as sitk

from modMisc.sitk_itk import sitk2itk


def get_landmarks(xct_landmark_img, ct_landmarks_img, fiducial_list):
    """
    Converts a landmark image (binary) to a listy of points.

    Parameters
    ----------
    xct_landmark_img : SimpleITK.Image

    ct_landmarks_img : SimpleITK.Image

    fiducial_list : list
        List containing the fiducial images

    Returns
    -------
    xct_fiducials_flat : list
        List containing the XCT fiducial points

    ct_fiducials_flat : list
        List containing the CT fiducial points

    xct_targets : list
        List containing the XCT target points

    ct_targets : list
        List containing the CT target points
    """
    xct_F1_img = fiducial_list[0]
    xct_F2_img = fiducial_list[1]
    xct_F3_img = fiducial_list[2]
    ct_F1_img = fiducial_list[0]
    ct_F2_img = fiducial_list[1]
    ct_F3_img = fiducial_list[2]

    # Flatten landmarks
    landmark_stats = sitk.LabelShapeStatisticsImageFilter()
    landmark_stats.ComputeOrientedBoundingBoxOn()

    # XCT landmarks
    landmark_stats.Execute(xct_landmark_img)

    xct_landmarks = []
    for label in landmark_stats.GetLabels():
        xct_landmarks.append(landmark_stats.GetOrientedBoundingBoxOrigin(label))

    xct_landmarks_flat = [c for p in xct_landmarks for c in p]
    xct_target1 = np.array(
        [xct_landmarks_flat[0], xct_landmarks_flat[1], xct_landmarks_flat[2]]
    )
    xct_target2 = np.array(
        [xct_landmarks_flat[3], xct_landmarks_flat[4], xct_landmarks_flat[5]]
    )
    xct_target3 = np.array(
        [xct_landmarks_flat[6], xct_landmarks_flat[7], xct_landmarks_flat[8]]
    )
    xct_targets = [xct_target1, xct_target2, xct_target3]

    # CT Landmarks
    landmark_stats.Execute(ct_landmarks_img)

    ct_landmarks = []
    for label in landmark_stats.GetLabels():
        ct_landmarks.append(landmark_stats.GetOrientedBoundingBoxOrigin(label))

    ct_landmarks_flat = [c for p in ct_landmarks for c in p]
    ct_target1 = np.array(
        [ct_landmarks_flat[0], ct_landmarks_flat[1], ct_landmarks_flat[2]]
    )
    ct_target2 = np.array(
        [ct_landmarks_flat[3], ct_landmarks_flat[4], ct_landmarks_flat[5]]
    )
    ct_target3 = np.array(
        [ct_landmarks_flat[6], ct_landmarks_flat[7], ct_landmarks_flat[8]]
    )
    ct_targets = [ct_target1, ct_target2, ct_target3]

    # ------------------------------------------------------------------------------------#
    # Get the centroids of the beads in CT and XCT space
    # Use these to find the "gold standard" transformation, Tgs
    # ------------------------------------------------------------------------------------#
    # Create a component map for each binary image, then compute image statistics
    component_map = sitk.ConnectedComponentImageFilter()
    shape_stats = sitk.LabelShapeStatisticsImageFilter()

    # XCT fiducial centroids (gold standard)
    label = component_map.Execute(xct_F1_img)
    shape_stats.Execute(label)
    xct_F1_centroid = shape_stats.GetCentroid(1)

    label = component_map.Execute(xct_F2_img)
    shape_stats.Execute(label)
    xct_F2_centroid = shape_stats.GetCentroid(1)

    label = component_map.Execute(xct_F3_img)
    shape_stats.Execute(label)
    xct_F3_centroid = shape_stats.GetCentroid(1)

    xct_fiducials = [
        [xct_F1_centroid[0], xct_F1_centroid[1], xct_F1_centroid[2]],
        [xct_F2_centroid[0], xct_F2_centroid[1], xct_F2_centroid[2]],
        [xct_F3_centroid[0], xct_F3_centroid[1], xct_F3_centroid[2]],
    ]
    xct_fiducials_flat = [c for p in xct_fiducials for c in p]

    # CT fiducial centroids (after registration)
    label = component_map.Execute(ct_F1_img)
    shape_stats.Execute(label)
    ct_F1_centroid = shape_stats.GetCentroid(1)

    label = component_map.Execute(ct_F2_img)
    shape_stats.Execute(label)
    ct_F2_centroid = shape_stats.GetCentroid(1)

    label = component_map.Execute(ct_F3_img)
    shape_stats.Execute(label)
    ct_F3_centroid = shape_stats.GetCentroid(1)

    ct_fiducials = [
        [ct_F1_centroid[0], ct_F1_centroid[1], ct_F1_centroid[2]],
        [ct_F2_centroid[0], ct_F2_centroid[1], ct_F2_centroid[2]],
        [ct_F3_centroid[0], ct_F3_centroid[1], ct_F3_centroid[2]],
    ]
    ct_fiducials_flat = [c for p in ct_fiducials for c in p]

    return xct_fiducials_flat, ct_fiducials_flat, xct_targets, ct_targets


def compute_TGS(xct_fiducials_flat, ct_fiducials_flat):
    """
    Computes the gold-standard transformation matrix using the fiducial points.

    Parameters
    ----------
    xct_fiducials_flat :
        A list of the XCT fiducial points

    ct_fiducials_flat :
        A list of the CT fiducial points

    Returns
    -------
    Tgs : SimpleITK.TFM
        The gold-standard transformation matrix
    """
    # ------------------------------------------------------------#
    # Compute Tgs between CT and XCT
    # ------------------------------------------------------------#
    landmarkInitializer = sitk.LandmarkBasedTransformInitializerFilter()
    landmarkInitializer.SetFixedLandmarks(xct_fiducials_flat)
    landmarkInitializer.SetMovingLandmarks(ct_fiducials_flat)
    Tgs = landmarkInitializer.Execute(sitk.VersorRigid3DTransform())

    sitk.WriteTransform(
        Tgs,
        "/Users/mkuczyns/OneDrive - University of Calgary/ManskeLabImages/DYNACT/04 - DYNACT1/reg/DYNACT1_011/staticCT_to_HR-pQCT/TGS.tfm",
    )

    return Tgs


def compute_FLE(rmse_fre):
    """
    Computes the fiducial localization error.

    Parameters
    ----------
    rmse_fre : float

    Returns
    -------
    fle : float
    """
    # Calculate the estimate of the FLE
    Nf = 3  # Number of fiducials

    fle = math.sqrt((Nf / (Nf - 2)) * rmse_fre)

    return fle


def compute_FRE(T_gs, xct_centroids, ct_centroids):
    """
    Computes the fiducial registration error.

    Parameters
    ----------
    T_gs : SimpleITK.TFM
        The gold-standard transformation matrix

    xct_centroids : list
        List containing the XCT centroids

    ct_centroids : list
        List containing the CT centroids

    Returns
    -------
    rms_fre : float
        The root mean square for the FRE
    """
    # Calculate the estimate of the FRE
    # Although FLE, FRE, and TRE are vector quantities, they are often
    # represented as scalar quantities by taking the RMS of the vector components

    Nf = 3  # Number of fiducials

    xct_F1_centroid = xct_centroids[0]
    xct_F2_centroid = xct_centroids[1]
    xct_F3_centroid = xct_centroids[2]
    ct_F1_centroid = ct_centroids[0]
    ct_F2_centroid = ct_centroids[1]
    ct_F3_centroid = ct_centroids[2]

    ct_F1_centroid = T_gs.GetInverse().TransformPoint(ct_F1_centroid)
    ct_F2_centroid = T_gs.GetInverse().TransformPoint(ct_F2_centroid)
    ct_F3_centroid = T_gs.GetInverse().TransformPoint(ct_F3_centroid)

    fre1 = math.sqrt(
        (1 / Nf) * ((ct_F1_centroid[0] - xct_F1_centroid[0]) ** 2)
        + ((ct_F1_centroid[1] - xct_F1_centroid[1]) ** 2)
        + ((ct_F1_centroid[2] - xct_F1_centroid[2]) ** 2)
    )
    fre2 = math.sqrt(
        (1 / Nf) * ((ct_F2_centroid[0] - xct_F2_centroid[0]) ** 2)
        + ((ct_F2_centroid[1] - xct_F2_centroid[1]) ** 2)
        + ((ct_F2_centroid[2] - xct_F2_centroid[2]) ** 2)
    )
    fre3 = math.sqrt(
        (1 / Nf) * ((ct_F3_centroid[0] - xct_F3_centroid[0]) ** 2)
        + ((ct_F3_centroid[1] - xct_F3_centroid[1]) ** 2)
        + ((ct_F3_centroid[2] - xct_F3_centroid[2]) ** 2)
    )

    rms_fre = math.sqrt((1 / 3) * (fre1**2 + fre2**2 + fre3**2))

    return rms_fre


def compute_TRE(Nf, dx, dy, dz, rms_fx, rms_fy, rms_fz, fle):
    """
    Computes the target registration error.

    Parameters
    ----------
    Nf : int
        Number of fiducials

    dx : float
        Distance between the PA and target (X-axis)

    dy : float
        Distance between the PA and target (Y-axis)

    dz : float
        Distance between the PA and target (Z-axis)

    rms_fx : float
        RMS distance of all fiducials to the PA (X-axis)

    rms_fy : float
        RMS distance of all fiducials to the PA (Y-axis)

    rms_fz : float
        RMS distance of all fiducials to the PA (Z-axis)

    fle : float
        Fiducial localization error

    Returns
    -------
    tre : float
    """
    tre = math.sqrt(
        (1 / Nf)
        * (
            1
            + (1 / 3)
            * (
                (dx**2) / (rms_fx**2)
                + (dy**2) / (rms_fy**2)
                + (dz**2) / (rms_fz**2)
            )
        )
        * fle**2
    )
    return tre


def compute_PA(combined_img):
    """
    Computes the prinicpal axes (PA) for an input image. We need to convert
    SimpleITKimages to ITK images before finding the PAs.

    Parameters
    ----------
    combined_img : SimpleITK.Image

    Returns
    -------
    pa : list
        List containing the PAs
    """
    # Compute the principal axes (PA) of the XCT fiducials (gold standard)
    fiducial_img = sitk2itk(combined_img)

    moments = itk.ImageMomentsCalculator.New(fiducial_img)
    moments.Compute()

    fiducial_img_PA = moments.GetPrincipalAxes()  # In physical coordinates

    PA_x = np.array(
        [fiducial_img_PA(0, 0), fiducial_img_PA(0, 1), fiducial_img_PA(0, 2)]
    )
    PA_y = np.array(
        [fiducial_img_PA(1, 0), fiducial_img_PA(1, 1), fiducial_img_PA(1, 2)]
    )
    PA_z = np.array(
        [fiducial_img_PA(2, 0), fiducial_img_PA(2, 1), fiducial_img_PA(2, 2)]
    )

    pa = [PA_x, PA_y, PA_z]

    return pa


def get_distance_to_PA(T_gs, targets, PAs, F1_centroid, F2_centroid, F3_centroid):
    """
    Computes the distance between the PAs and the fiducial centroids.

    Parameters
    ----------
    T_gs : SimpleITK.TFM
        Gold standard transformation matrix

    targets : list
        List of the targets

    PAs : list
        List of PAs in XCT space

    F1_centroid : list
        List of centroids of the first fiducial

    F2_centroid : list
        List of centroids of the second fiducial

    F3_centroid : list
        List of centroids of the third fiducial

    Returns
    -------
    d : list
        List of the RMSEs of the distances between target and PA

    xct_F1_d : list
        List of distances from the first fiducial to the PA axes

    xct_F2_d : list
        List of distances from the second fiducial to the PA axes

    xct_F3_d : list
        List of distances from the third fiducial to the PA axes
    """
    # Find the distance from the target to each axis of the PA (d)
    xct_target1 = targets[0]
    xct_target2 = targets[1]
    xct_target3 = targets[2]
    xctPA_x = PAs[0]
    xctPA_y = PAs[1]
    xctPA_z = PAs[2]
    xct_F1_centroid = F1_centroid[0]
    xct_F1_centroid = F1_centroid[1]
    xct_F1_centroid = F1_centroid[2]
    xct_F2_centroid = F2_centroid[0]
    xct_F2_centroid = F2_centroid[1]
    xct_F2_centroid = F2_centroid[2]
    xct_F3_centroid = F3_centroid[0]
    xct_F3_centroid = F3_centroid[1]
    xct_F3_centroid = F3_centroid[2]

    target1 = T_gs.GetInverse().TransformPoint(xct_target1)
    target2 = T_gs.GetInverse().TransformPoint(xct_target2)
    target3 = T_gs.GetInverse().TransformPoint(xct_target3)

    dx1 = math.sqrt(
        ((target1[0] - xctPA_x[0]) ** 2)
        + ((target1[1] - xctPA_x[1]) ** 2)
        + ((target1[2] - xctPA_x[2]) ** 2)
    )
    dy1 = math.sqrt(
        ((target1[0] - xctPA_y[0]) ** 2)
        + ((target1[1] - xctPA_y[1]) ** 2)
        + ((target1[2] - xctPA_y[2]) ** 2)
    )
    dz1 = math.sqrt(
        ((target1[0] - xctPA_z[0]) ** 2)
        + ((target1[1] - xctPA_z[1]) ** 2)
        + ((target1[2] - xctPA_z[2]) ** 2)
    )

    dx2 = math.sqrt(
        ((target2[0] - xctPA_x[0]) ** 2)
        + ((target2[1] - xctPA_x[1]) ** 2)
        + ((target2[2] - xctPA_x[2]) ** 2)
    )
    dy2 = math.sqrt(
        ((target2[0] - xctPA_y[0]) ** 2)
        + ((target2[1] - xctPA_y[1]) ** 2)
        + ((target2[2] - xctPA_y[2]) ** 2)
    )
    dz2 = math.sqrt(
        ((target2[0] - xctPA_z[0]) ** 2)
        + ((target2[1] - xctPA_z[1]) ** 2)
        + ((target2[2] - xctPA_z[2]) ** 2)
    )

    dx3 = math.sqrt(
        ((target3[0] - xctPA_x[0]) ** 2)
        + ((target3[1] - xctPA_x[1]) ** 2)
        + ((target3[2] - xctPA_x[2]) ** 2)
    )
    dy3 = math.sqrt(
        ((target3[0] - xctPA_y[0]) ** 2)
        + ((target3[1] - xctPA_y[1]) ** 2)
        + ((target3[2] - xctPA_y[2]) ** 2)
    )
    dz3 = math.sqrt(
        ((target3[0] - xctPA_z[0]) ** 2)
        + ((target3[1] - xctPA_z[1]) ** 2)
        + ((target3[2] - xctPA_z[2]) ** 2)
    )

    dx = compute_RMSE(dx1, dx2, dx3)
    dy = compute_RMSE(dy1, dy2, dy3)
    dz = compute_RMSE(dz1, dz2, dz3)

    # Find the distance from each XCT fiducial to each axis of the PA
    xct_F1_dx = math.sqrt(
        ((xct_F1_centroid[0] - xctPA_x[0]) ** 2)
        + ((xct_F1_centroid[1] - xctPA_x[1]) ** 2)
        + ((xct_F1_centroid[2] - xctPA_x[2]) ** 2)
    )
    xct_F1_dy = math.sqrt(
        ((xct_F1_centroid[0] - xctPA_y[0]) ** 2)
        + ((xct_F1_centroid[1] - xctPA_y[1]) ** 2)
        + ((xct_F1_centroid[2] - xctPA_y[2]) ** 2)
    )
    xct_F1_dz = math.sqrt(
        ((xct_F1_centroid[0] - xctPA_z[0]) ** 2)
        + ((xct_F1_centroid[1] - xctPA_z[1]) ** 2)
        + ((xct_F1_centroid[2] - xctPA_z[2]) ** 2)
    )

    xct_F2_dx = math.sqrt(
        ((xct_F2_centroid[0] - xctPA_x[0]) ** 2)
        + ((xct_F2_centroid[1] - xctPA_x[1]) ** 2)
        + ((xct_F2_centroid[2] - xctPA_x[2]) ** 2)
    )
    xct_F2_dy = math.sqrt(
        ((xct_F2_centroid[0] - xctPA_y[0]) ** 2)
        + ((xct_F2_centroid[1] - xctPA_y[1]) ** 2)
        + ((xct_F2_centroid[2] - xctPA_y[2]) ** 2)
    )
    xct_F2_dz = math.sqrt(
        ((xct_F2_centroid[0] - xctPA_z[0]) ** 2)
        + ((xct_F2_centroid[1] - xctPA_z[1]) ** 2)
        + ((xct_F2_centroid[2] - xctPA_z[2]) ** 2)
    )

    xct_F3_dx = math.sqrt(
        ((xct_F3_centroid[0] - xctPA_x[0]) ** 2)
        + ((xct_F3_centroid[1] - xctPA_x[1]) ** 2)
        + ((xct_F3_centroid[2] - xctPA_x[2]) ** 2)
    )
    xct_F3_dy = math.sqrt(
        ((xct_F3_centroid[0] - xctPA_y[0]) ** 2)
        + ((xct_F3_centroid[1] - xctPA_y[1]) ** 2)
        + ((xct_F3_centroid[2] - xctPA_y[2]) ** 2)
    )
    xct_F3_dz = math.sqrt(
        ((xct_F3_centroid[0] - xctPA_z[0]) ** 2)
        + ((xct_F3_centroid[1] - xctPA_z[1]) ** 2)
        + ((xct_F3_centroid[2] - xctPA_z[2]) ** 2)
    )

    d = [dx, dy, dz]
    xct_F1_d = [xct_F1_dx, xct_F1_dy, xct_F1_dz]
    xct_F2_d = [xct_F2_dx, xct_F2_dy, xct_F2_dz]
    xct_F3_d = [xct_F3_dx, xct_F3_dy, xct_F3_dz]

    return d, xct_F1_d, xct_F2_d, xct_F3_d


def compute_RMSE(input1, input2, input3):
    """
    Calculates the root mean square error between three inputs.

    Parameters
    ----------
    input1 : float

    input2 : float

    input3 : float

    Returns
    -------
    rmse : float
    """
    rmse = math.sqrt((1 / 3) * (input1**2 + input2**2 + input3**2))
    return rmse


def main(image_list, fiducial_list, landmark_list, output_TGS, intensity_TFM):
    """
    Main function to compute FRE, FLE, and TRE.

    Parameters
    ----------
    image_list : list

    fiducial_list : list

    landmark_list : list

    output_TGS : string

    intensity_TFM : string

    Returns
    -------
    tre : float
    """
    ct_img = sitk.ReadImage(image_list[0])
    xct_img = sitk.ReadImage(image_list[1])
    xct_F1_img = sitk.ReadImage(fiducial_list[0])
    xct_F2_img = sitk.ReadImage(fiducial_list[1])
    xct_F3_img = sitk.ReadImage(fiducial_list[2])
    ct_F1_img = sitk.ReadImage(fiducial_list[0])
    ct_F2_img = sitk.ReadImage(fiducial_list[1])
    ct_F3_img = sitk.ReadImage(fiducial_list[2])
    xct_landmark_img = sitk.ReadImage(landmark_list[0], sitk.sitkUInt8)
    ct_landmarks_img = sitk.ReadImage(landmark_list[1], sitk.sitkUInt8)
    T_r = sitk.ReadTransform(intensity_TFM)

    fiducial_img_list = [
        xct_F1_img,
        xct_F2_img,
        xct_F3_img,
        ct_F1_img,
        ct_F2_img,
        ct_F3_img,
    ]

    xct_fiducials_flat, ct_fiducials_flat, xct_targets, ct_targets = get_landmarks(
        xct_landmark_img, ct_landmarks_img, fiducial_img_list
    )
    T_gs = compute_TGS(xct_fiducials_flat, ct_fiducials_flat)

    # Transform CT image to XCT using Tgs
    # sitk.Resample(imageToBeResampled, referenceImage, transformation, interpolator, defaultPixelValue, outputPixelType)
    ct_transformed_Tgs = sitk.Resample(
        ct_img, xct_img, T_gs, sitk.sitkLinear, 0.0, ct_img.GetPixelID()
    )
    sitk.WriteImage(ct_transformed_Tgs, output_TGS)

    # Calculate the TRE of the Tgs compared to the intensity-based registration (Tr)
    transformed_ct_landmarks_Tr = [T_r.TransformPoint(p) for p in ct_landmarks]
    transformed_ct_landmarks_Tgs = [T_gs.TransformPoint(p) for p in ct_landmarks]

    errors = [
        (np.linalg.norm(np.array(p_fixed) - np.array(p_moving)))
        for p_fixed, p_moving in zip(
            transformed_ct_landmarks_Tgs, transformed_ct_landmarks_Tr
        )
    ]
    min_errors = np.min(errors)
    max_errors = np.max(errors)
    print(
        "TRE between gold-standard and intensity-based registration for landmarks = "
        + str(errors)
    )

    # Combine the 3 marker images (binary) to get a single distribution of markers
    # Repeat for the CT image and XCT image
    combined_img_xct = xct_F1_img + xct_F2_img + xct_F3_img
    comb_img_ct = ct_F1_img + ct_F2_img + ct_F3_img

    PA_xct = compute_PA(combined_img_xct)

    rms_fre = compute_FRE(T_gs, xct_fiducials_flat, ct_fiducials_flat)
    fle = compute_FLE(rms_fre)
    d, xct_F1_d, xct_F2_d, xct_F3_d = get_distance_to_PA(
        T_gs,
        xct_targets,
        PA_xct,
        xct_fiducials_flat[0],
        xct_fiducials_flat[1],
        xct_fiducials_flat[2],
    )

    # Compute the RMS distance of all fiducials to each axis of the PA (f)
    rms_fx = compute_RMSE(xct_F1_d[0], xct_F2_d[0], xct_F3_d[0])
    rms_fy = compute_RMSE(xct_F1_d[1], xct_F2_d[1], xct_F3_d[1])
    rms_fz = compute_RMSE(xct_F1_d[2], xct_F2_d[2], xct_F3_d[2])

    # Calculate the estimate of the TRE
    tre = compute_TRE(3, d[0], d[1], d[2], rms_fx, rms_fy, rms_fz, fle)

    return tre


if __name__ == "__main__":
    # Load images
    parser = argparse.ArgumentParser()
    parser.add_argument("ct", type=str)
    parser.add_argument("xct", type=str)
    parser.add_argument("xct_F1", type=str)
    parser.add_argument("xct_F2", type=str)
    parser.add_argument("xct_F3", type=str)
    parser.add_argument("ct_F1", type=str)
    parser.add_argument("ct_F2", type=str)
    parser.add_argument("ct_F3", type=str)
    parser.add_argument("xct_landmarks", type=str)
    parser.add_argument("ct_landmarks", type=str)
    parser.add_argument("output_TGS", type=str)
    parser.add_argument("intensity_TFM", type=str)
    args = parser.parse_args()

    ct = args.ct
    xct = args.xct
    xct_F1 = args.xct_F1
    xct_F2 = args.xct_F2
    xct_F3 = args.xct_F3
    ct_F1 = args.ct_F1
    ct_F2 = args.ct_F2
    ct_F3 = args.ct_F3
    xct_landmarks = args.xct_landmarks
    ct_landmarks = args.ct_landmarks
    output_TGS = args.output_TGS
    intensity_TFM = args.intensity_TFM

    image_list = [ct, xct]
    fiducial_list = [xct_F1, xct_F2, xct_F3, ct_F1, ct_F2, ct_F3]
    landmark_list = [xct_landmarks, ct_landmarks]

    tre = main(image_list, fiducial_list, landmark_list, output_TGS, intensity_TFM)

    print("TRE of gold-standard = " + str(tre))
