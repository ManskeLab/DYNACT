"""
comb_poly_data.py

Created by: Michael Kuczynski
Created on: Jan. 11, 2021
"""

import vtk
import argparse


def comb_poly_data(vtk_path1, vtk_path2):
    """
    Combines two VTK PolyData files into one PolyData image. The combined PolyData
    is smoothed.

    Parameters
    ----------
    vtk_path1 : string

    vtk_path2 : string

    Returns
    -------
    final_img : VTK.Image
    """
    image_reader1 = vtk.vtkPolyDataReader()
    image_reader1.SetFileName(vtk_path1)
    image_reader1.Update()

    image_reader2 = vtk.vtkPolyDataReader()
    image_reader2.SetFileName(vtk_path2)
    image_reader2.Update()

    append = vtk.vtkAppendPolyData()
    append.AddInputData(image_reader1.GetOutput())
    append.AddInputData(image_reader2.GetOutput())
    append.Update()

    # Remove any duplicate points.
    clean_filter = vtk.vtkCleanPolyData()
    clean_filter.SetInputConnection(append.GetOutputPort())
    clean_filter.Update()

    smooth_img = vtk.vtkSmoothPolyDataFilter()
    smooth_img.SetInputConnection(clean_filter.GetOutputPort())
    smooth_img.SetNumberOfIterations(50)
    smooth_img.SetRelaxationFactor(0.2)
    smooth_img.FeatureEdgeSmoothingOff()
    smooth_img.BoundarySmoothingOn()
    smooth_img.Update()

    final_img = smooth_img.GetOutput()

    return final_img


def main(input_vtk_path1, input_vtk_path2):
    """
    Main function to combine PolyData files.

    Parameters
    ----------
    input_vtk_path1 : string

    input_vtk_path2 : string

    Returns
    -------
    polydata : VTK.PolyData
    """
    polydata = comb_poly_data(input_vtk_path1, input_vtk_path2)
    return polydata


if __name__ == "__main__":
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("vtk_path1", type=str)
    parser.add_argument("vtk_path2", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    vtk_path1 = args.vtk_path1
    vtk_path2 = args.vtk_path2
    output_path = args.output_path

    polydata = main(vtk_path1, vtk_path2)

    writer = vtk.vtkPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName(output_path)
    writer.Update()
