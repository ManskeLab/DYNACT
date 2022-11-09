import numpy as np

"""
Converts a vector to a unit vector.

Parameters
----------
input_vector : numpy.array

Returns
-------
numpy.array
"""
def unit_vector(input_vector):
    return input_vector / np.linalg.norm(input_vector)


"""
Finds the difference between two SCSs.

Parameters
----------
input_arr1 : numpy.array

input_arr2 : numpy.array

Returns
-------
v : numpy.array
"""
def scs_diff(input_arr1, input_arr2):
    if input_arr1.size != 3 and input_arr2.size != 3:
        return 0
    
    axis_rater1 = np.array([input_arr1[0], input_arr1[1], input_arr1[2]])
    axis_rater2 = np.array([input_arr2[0], input_arr2[1], input_arr2[2]])

    v = np.arccos(np.dot(axis_rater1, axis_rater2) / (np.linalg.norm(axis_rater1) * np.linalg.norm(axis_rater2)))
    v = np.rad2deg(v)

    return v
