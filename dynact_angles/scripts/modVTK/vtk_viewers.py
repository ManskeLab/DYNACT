"""
vtk_viewers.py

Created by: Michael Kuczynski
Created on: Jan. 11, 2021
"""

import vtk
import argparse

"""
Displays the MC1 and TRP bones with the points selected for SCS definition.

Parameters
----------
mc1_mask : string

trp_mask : string

mc1_pnt1 : list

mc1_pnt2 : list

mc1_pnt3 : list

trp_pnt1 : list

trp_pnt2 : list

trp_pnt3 : list

trp_pnt4 : list

Returns
-------

"""
def display(mc1_mask, trp_mask, mc1_pnt1, mc1_pnt2, mc1_pnt3, trp_pnt1, trp_pnt2, trp_pnt3, trp_pnt4):
    # Display points
    reader_mc1 = vtk.vtkPolyDataReader()
    reader_mc1.SetFileName(mc1_mask)
    reader_mc1.Update()

    reader_trp = vtk.vtkPolyDataReader()
    reader_trp.SetFileName(trp_mask)
    reader_trp.Update()

    # Add points as spheres
    sphere1_mc1 = vtk.vtkSphereSource()
    sphere1_mc1.SetCenter(mc1_pnt1)
    sphere1_mc1.SetRadius(1.0)
    sphere2_mc1 = vtk.vtkSphereSource()
    sphere2_mc1.SetCenter(mc1_pnt2)
    sphere2_mc1.SetRadius(1.0)
    sphere3_mc1 = vtk.vtkSphereSource()
    sphere3_mc1.SetCenter(mc1_pnt3)
    sphere3_mc1.SetRadius(1.0)

    sphere1_trp = vtk.vtkSphereSource()
    sphere1_trp.SetCenter(trp_pnt1)
    sphere1_trp.SetRadius(1.0)
    sphere2_trp = vtk.vtkSphereSource()
    sphere2_trp.SetCenter(trp_pnt2)
    sphere2_trp.SetRadius(1.0)
    sphere3_trp = vtk.vtkSphereSource()
    sphere3_trp.SetCenter(trp_pnt3)
    sphere3_trp.SetRadius(1.0)
    sphere4_trp = vtk.vtkSphereSource()
    sphere4_trp.SetCenter(trp_pnt4)
    sphere4_trp.SetRadius(1.0)

    # Join polydata
    append_filter = vtk.vtkAppendPolyData()
    append_filter.AddInputData(reader_mc1.GetOutput())
    append_filter.AddInputData(reader_trp.GetOutput())
    append_filter.Update()

    #  Remove any duplicate points.
    clean_filter = vtk.vtkCleanPolyData()
    clean_filter.SetInputConnection(append_filter.GetOutputPort())
    clean_filter.Update()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clean_filter.GetOutputPort())

    sphere1_mc1_mapper = vtk.vtkPolyDataMapper()
    sphere1_mc1_mapper.SetInputConnection(sphere1_mc1.GetOutputPort())
    sphere2_mc1_mapper = vtk.vtkPolyDataMapper()
    sphere2_mc1_mapper.SetInputConnection(sphere2_mc1.GetOutputPort())
    sphere3_mc1_mapper = vtk.vtkPolyDataMapper()
    sphere3_mc1_mapper.SetInputConnection(sphere3_mc1.GetOutputPort())

    sphere1_trp_mapper = vtk.vtkPolyDataMapper()
    sphere1_trp_mapper.SetInputConnection(sphere1_trp.GetOutputPort())
    sphere2_trp_mapper = vtk.vtkPolyDataMapper()
    sphere2_trp_mapper.SetInputConnection(sphere2_trp.GetOutputPort())
    sphere3_trp_mapper = vtk.vtkPolyDataMapper()
    sphere3_trp_mapper.SetInputConnection(sphere3_trp.GetOutputPort())
    sphere4_trp_mapper = vtk.vtkPolyDataMapper()
    sphere4_trp_mapper.SetInputConnection(sphere4_trp.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    sphere1_mc1_actor = vtk.vtkActor()
    sphere1_mc1_actor.SetMapper(sphere1_mc1_mapper)
    sphere1_mc1_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
    sphere2_mc1_actor = vtk.vtkActor()
    sphere2_mc1_actor.SetMapper(sphere2_mc1_mapper)
    sphere2_mc1_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
    sphere3_mc1_actor = vtk.vtkActor()
    sphere3_mc1_actor.SetMapper(sphere3_mc1_mapper)
    sphere3_mc1_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

    sphere1_trp_actor = vtk.vtkActor()
    sphere1_trp_actor.SetMapper(sphere1_trp_mapper)
    sphere1_trp_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
    sphere2_trp_actor = vtk.vtkActor()
    sphere2_trp_actor.SetMapper(sphere2_trp_mapper)
    sphere2_trp_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
    sphere3_trp_actor = vtk.vtkActor()
    sphere3_trp_actor.SetMapper(sphere3_trp_mapper)
    sphere3_trp_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
    sphere4_trp_actor = vtk.vtkActor()
    sphere4_trp_actor.SetMapper(sphere4_trp_mapper)
    sphere4_trp_actor.GetProperty().SetColor(0.0, 1.0, 0.0)

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Add the actors to the scene
    renderer.AddActor(actor)
    renderer.AddActor(sphere1_mc1_actor)
    renderer.AddActor(sphere2_mc1_actor)
    renderer.AddActor(sphere3_mc1_actor)
    renderer.AddActor(sphere1_trp_actor)
    renderer.AddActor(sphere2_trp_actor)
    renderer.AddActor(sphere3_trp_actor)
    renderer.AddActor(sphere4_trp_actor)
    renderer.SetBackground(0,0,0)

    # Render and interact
    render_window.Render()
    render_window_interactor.Start()


"""
Displays the MC1 and TRP bones with the SCS axes.

Parameters
----------
mc1_mask : string

trp_mask : string

mc1_X : list

mc1_Y : list

mc1_Z : list

trp_X : list

trp_Y : list

trp_Z : list

m0 : list
    MC1 origin

t0 : list
    TRP origin

Returns
-------

"""
def display_axes(mc1_mask, trp_mask, mc1_X, mc1_Y, mc1_Z, trp_X, trp_Y, trp_Z, mO, tO):
    # Display points
    reader_mc1 = vtk.vtkPolyDataReader()
    reader_mc1.SetFileName(mc1_mask)
    reader_mc1.Update()
    reader_trp = vtk.vtkPolyDataReader()
    reader_trp.SetFileName(trp_mask)
    reader_trp.Update()

    # Join polydata
    append_filter = vtk.vtkAppendPolyData()
    append_filter.AddInputData(reader_mc1.GetOutput())
    append_filter.AddInputData(reader_trp.GetOutput())
    append_filter.Update()

    #  Remove any duplicate points.
    clean_filter = vtk.vtkCleanPolyData()
    clean_filter.SetInputConnection(append_filter.GetOutputPort())
    clean_filter.Update()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clean_filter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Add points as spheres
    mc1_axis1 = vtk.vtkLineSource()
    mc1_axis1.SetPoint1(mO)
    mc1_axis1.SetPoint2(mc1_X)
    mc1_axis2 = vtk.vtkLineSource()
    mc1_axis2.SetPoint1(mO)
    mc1_axis2.SetPoint2(mc1_Y)
    mc1_axis3 = vtk.vtkLineSource()
    mc1_axis3.SetPoint1(mO)
    mc1_axis3.SetPoint2(mc1_Z)
    mc1_origin = vtk.vtkSphereSource()
    mc1_origin.SetCenter(mO)
    mc1_origin.SetRadius(0.1)

    trp_axis1 = vtk.vtkLineSource()
    trp_axis1.SetPoint1(tO)
    trp_axis1.SetPoint2(trp_X)
    trp_axis2 = vtk.vtkLineSource()
    trp_axis2.SetPoint1(tO)
    trp_axis2.SetPoint2(trp_Y)
    trp_axis3 = vtk.vtkLineSource()
    trp_axis3.SetPoint1(tO)
    trp_axis3.SetPoint2(trp_Z)
    trp_origin = vtk.vtkSphereSource()
    trp_origin.SetCenter(tO)
    trp_origin.SetRadius(0.1)

    mc1_axis1_mapper = vtk.vtkPolyDataMapper()
    mc1_axis1_mapper.SetInputConnection(mc1_axis1.GetOutputPort())
    mc1_axis2_mapper = vtk.vtkPolyDataMapper()
    mc1_axis2_mapper.SetInputConnection(mc1_axis2.GetOutputPort())
    mc1_axis3_mapper = vtk.vtkPolyDataMapper()
    mc1_axis3_mapper.SetInputConnection(mc1_axis3.GetOutputPort())
    mc1_origin_mapper = vtk.vtkPolyDataMapper()
    mc1_origin_mapper.SetInputConnection(mc1_origin.GetOutputPort())

    trp_axis1_mapper = vtk.vtkPolyDataMapper()
    trp_axis1_mapper.SetInputConnection(trp_axis1.GetOutputPort())
    trp_axis2_mapper = vtk.vtkPolyDataMapper()
    trp_axis2_mapper.SetInputConnection(trp_axis2.GetOutputPort())
    trp_axis3_mapper = vtk.vtkPolyDataMapper()
    trp_axis3_mapper.SetInputConnection(trp_axis3.GetOutputPort())
    trp_origin_mapper = vtk.vtkPolyDataMapper()
    trp_origin_mapper.SetInputConnection(trp_origin.GetOutputPort())

    mc1_axis1_actor = vtk.vtkActor()
    mc1_axis1_actor.SetMapper(mc1_axis1_mapper)
    mc1_axis1_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
    mc1_axis1_actor.GetProperty().SetLineWidth(5)
    mc1_axis2_actor = vtk.vtkActor()
    mc1_axis2_actor.SetMapper(mc1_axis2_mapper)
    mc1_axis2_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
    mc1_axis2_actor.GetProperty().SetLineWidth(5)
    mc1_axis3_actor = vtk.vtkActor()
    mc1_axis3_actor.SetMapper(mc1_axis3_mapper)
    mc1_axis3_actor.GetProperty().SetColor(0.0, 0.0, 1.0)
    mc1_axis3_actor.GetProperty().SetLineWidth(5)
    mc1_origin_actor = vtk.vtkActor()
    mc1_origin_actor.SetMapper(mc1_origin_mapper)
    mc1_origin_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

    trp_axis1_actor = vtk.vtkActor()
    trp_axis1_actor.SetMapper(trp_axis1_mapper)
    trp_axis1_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
    trp_axis1_actor.GetProperty().SetLineWidth(5)
    trp_axis2_actor = vtk.vtkActor()
    trp_axis2_actor.SetMapper(trp_axis2_mapper)
    trp_axis2_actor.GetProperty().SetColor(0.0, 1.0, 0.0)
    trp_axis2_actor.GetProperty().SetLineWidth(5)
    trp_axis3_actor = vtk.vtkActor()
    trp_axis3_actor.SetMapper(trp_axis3_mapper)
    trp_axis3_actor.GetProperty().SetColor(0.0, 0.0, 1.0)
    trp_axis3_actor.GetProperty().SetLineWidth(5)
    trp_origin_actor = vtk.vtkActor()
    trp_origin_actor.SetMapper(trp_origin_mapper)
    trp_origin_actor.GetProperty().SetColor(0.0, 1.0, 0.0)

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Add the actors to the scene
    # renderer.AddActor(actor)
    # renderer.AddActor(actor)
    renderer.AddActor(mc1_axis1_actor)
    renderer.AddActor(mc1_axis2_actor)
    renderer.AddActor(mc1_axis3_actor)
    renderer.AddActor(mc1_origin_actor)
    renderer.AddActor(trp_axis1_actor)
    renderer.AddActor(trp_axis2_actor)
    renderer.AddActor(trp_axis3_actor)
    renderer.AddActor(trp_origin_actor)
    renderer.SetBackground(0,0,0)

    # Render and interact
    render_window.Render()
    render_window_interactor.Start()
