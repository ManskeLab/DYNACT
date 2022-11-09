"""
calc_coord_systems.py

Created by: Michael Kuczynski
Created on: 11-01-2021

Description: Functions to calculate SCSs and JCS.
"""

import numpy as np

"""
Transforms a point using the provided SimpleITK transform.

Parameters
----------
transform : SimpleITK.TFM

Returns
-------
transformed_pnt : list
"""
def transform_point(transform, pnt):
    transformed_pnt = transform.TransformPoint(pnt)
    return transformed_pnt


"""
Compute the TRP SCS using the 4 landmarks.

Parameters
----------
points : list

Returns
-------
numpy.array
"""
def calculate_trp_scs(points):
    #----------------------------#
    # TRAPEZIUM SCS              #
    #----------------------------#
    TM1J = points[0] # TRP origin
    TM2J = points[1]
    TSTJ = points[2]
    TDET = points[3]

    # Z - Runs lateral-medial
    Z_TRP = [(TDET[0] - TM2J[0]), (TDET[1] - TM2J[1]), (TDET[2] - TM2J[2])]

    # X - Runs dorsal-volar
    V_TM1J_TSTJ = [(TSTJ[0] - TM1J[0]), (TSTJ[1] - TM1J[1]), (TSTJ[2] - TM1J[2])]
    X_TRP = [0,0,0]
    X_TRP = np.cross( V_TM1J_TSTJ, Z_TRP )
    
    # Y - Runs distal-proximal
    Y_TRP = [0,0,0]
    Y_TRP = np.cross( Z_TRP, X_TRP )

    # Normalize vectors (normalizes in place and returns norm)
    X_TRP = X_TRP / np.linalg.norm(X_TRP)
    Y_TRP = Y_TRP / np.linalg.norm(Y_TRP)
    Z_TRP = Z_TRP / np.linalg.norm(Z_TRP)

    return np.array([X_TRP, Y_TRP, Z_TRP])


"""
Compute the MC1 SCS using the 3 landmarks.

Parameters
----------
points : list

Returns
-------
numpy.array
"""
def calculate_mc1_scs(points):
    #----------------------------# 
    # FIRST METACARPAL SCS       #
    #----------------------------#
    M_LDT = points[0]
    M_MDT = points[1]
    M_CPB = points[2] # MC1 origin

    # Mid point between the lateral and medial MC1 tubercles
    tubercle_mid = [(M_LDT[0] + M_MDT[0])/2, (M_LDT[1] + M_MDT[1])/2, (M_LDT[2] + M_MDT[2])/2]
    
    # Vector between the lateral and medial MC1 tubercles (from lateral to medial)
    V_LMDT = [(M_LDT[0] - M_MDT[0]), (M_LDT[1] - M_MDT[1]), (M_LDT[2] - M_MDT[2])]

    # Y - Runs proximal-distal (assumed, not specified in paper  by Cheze, et al., 2009)
    Y_MC1 = [(M_CPB[0] - tubercle_mid[0]), (M_CPB[1] - tubercle_mid[1]), (M_CPB[2] - tubercle_mid[2])]
    
    # X - Runs dorsal-volar
    X_MC1 = [0,0,0]
    X_MC1 = np.cross(Y_MC1, V_LMDT)
    
    # Z - Runs medial-lateral
    Z_MC1 = [0,0,0]
    Z_MC1 = np.cross(X_MC1, Y_MC1)

    # Normalize vectors (normalizes in place and returns norm)
    X_MC1 = X_MC1 / np.linalg.norm(X_MC1)
    Y_MC1 = Y_MC1 / np.linalg.norm(Y_MC1)
    Z_MC1 = Z_MC1 / np.linalg.norm(Z_MC1)

    return np.array([X_MC1, Y_MC1, Z_MC1])
