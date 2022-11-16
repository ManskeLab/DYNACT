import SimpleITK as sitk

# Dictionary for interpolator types
interp_dict = {
    "nearestNeighbor": sitk.sitkNearestNeighbor,
    "linear": sitk.sitkLinear,
    "spline": sitk.sitkBSpline,
    "gaussian": sitk.sitkGaussian,
}

interp_dict_enum = {1: "nearestNeighbor", 2: "linear", 3: "spline", 4: "gaussian"}
