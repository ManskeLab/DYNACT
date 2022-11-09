import vtk
import math
import argparse

# Parse input arguments
# parser = argparse.ArgumentParser()
# parser.add_argument( 'M_LDT1', nargs='+' )
# parser.add_argument( 'M_MDT1', nargs='+' )
# parser.add_argument( 'M_CPB1', nargs='+' )
# parser.add_argument( 'TM1J1', nargs='+' )
# parser.add_argument( 'TM2J1', nargs='+' )
# parser.add_argument( 'TSTJ1', nargs='+' )
# parser.add_argument( 'TDET1', nargs='+' )

# parser.add_argument( 'M_LDT2', nargs='+' )
# parser.add_argument( 'M_MDT2', nargs='+' )
# parser.add_argument( 'M_CPB2', nargs='+' )
# parser.add_argument( 'TM1J2', nargs='+' )
# parser.add_argument( 'TM2J2', nargs='+' )
# parser.add_argument( 'TSTJ2', nargs='+' )
# parser.add_argument( 'TDET2', nargs='+' )

# args = parser.parse_args()

M_LDT1 = [ -102.650314331054, -113.015510559082, 8.847512245178 ] 
M_MDT1 = [ -98.960060119629, -97.369956970215, 12.981774330139 ] 
M_CPB1 = [ -84.494674682617, -116.824440002441, 40.786403656006 ] 
TM1J1 = [ -85.209465026855, -115.114242553710, 43.175067901611 ] 
TM2J1 = [ -84.940010070801, -106.117385864257, 46.095413208008 ] 
TSTJ1 = [ -76.794143676758, -114.498680114746, 50.378868103027 ] 
TDET1 = [ -88.692207336426, -121.883331298828, 44.359535217285 ] 

M_LDT2 = [ -101.839218139648, -113.645011901855, 8.918854713440 ] 
M_MDT2 = [ -98.269767761230, -97.452728271484, 13.065807342529 ] 
M_CPB2 = [ -85.666976928711, -117.207519531250, 41.261981964111 ] 
TM1J2 = [ -85.083656311035, -115.728401184082, 42.996093750000 ] 
TM2J2 = [ -84.621154785156, -106.257041931152, 46.056427001953 ] 
TSTJ2 = [ -76.785011291504, -114.451118469238, 50.320217132568 ] 
TDET2 = [ -88.787956237793, -121.882133483886, 44.553859710693 ] 

'''MC1'''
tubercle_mid1 = [ (M_LDT1[0] + M_MDT1[0])/2, (M_LDT1[1] + M_MDT1[1])/2, (M_LDT1[2] + M_MDT1[2])/2 ]
tubercle_mid2 = [ (M_LDT2[0] + M_MDT2[0])/2, (M_LDT2[1] + M_MDT2[1])/2, (M_LDT2[2] + M_MDT2[2])/2 ]

# Vectors
Y_MC11 = [ (M_CPB1[0] - tubercle_mid1[0]), (M_CPB1[1] - tubercle_mid1[1]), (M_CPB1[2] - tubercle_mid1[2]) ]
Y_MC12 = [ (M_CPB2[0] - tubercle_mid2[0]), (M_CPB2[1] - tubercle_mid2[1]), (M_CPB2[2] - tubercle_mid2[2]) ]

X_MC11 = [0,0,0]
vtk.vtkMath.Cross([ tubercle_mid1[0] - M_MDT1[0], tubercle_mid1[1] - M_MDT1[1], tubercle_mid1[2] - M_MDT1[2] ], Y_MC11, X_MC11)
X_MC12 = [0,0,0]
vtk.vtkMath.Cross([ tubercle_mid2[0] - M_MDT2[0], tubercle_mid2[1] - M_MDT2[1], tubercle_mid2[2] - M_MDT2[2] ], Y_MC12, X_MC12)

Z_MC11 = [0,0,0]
vtk.vtkMath.Cross(X_MC11, Y_MC11, Z_MC11)
Z_MC12 = [0,0,0]
vtk.vtkMath.Cross(X_MC12, Y_MC12, Z_MC12)


'''TRP'''
Z_TRP1 = [ (TDET1[0] - TM2J1[0]), (TDET1[1] - TM2J1[1]), (TDET1[2] - TM2J1[2]) ]
Z_TRP2 = [ (TDET2[0] - TM2J2[0]), (TDET2[1] - TM2J2[1]), (TDET2[2] - TM2J2[2]) ]

X_TRP1 = [0,0,0]
vtk.vtkMath.Cross( [ (TSTJ1[0] - TM1J1[0]), (TSTJ1[1] - TM1J1[1]), (TSTJ1[2] - TM1J1[2]) ], Z_TRP1, X_TRP1)
X_TRP2 = [0,0,0]
vtk.vtkMath.Cross( [ (TSTJ2[0] - TM1J2[0]), (TSTJ2[1] - TM1J2[1]), (TSTJ2[2] - TM1J2[2]) ], Z_TRP2, X_TRP2)

Y_TRP1 = [0,0,0]
vtk.vtkMath.Cross( Z_TRP1, X_TRP1, Y_TRP1 )
Y_TRP2 = [0,0,0]
vtk.vtkMath.Cross( Z_TRP2, X_TRP2, Y_TRP2 )


'''ANGLES'''
# theta = atan2(norm(cross(v1,v2)), dot(v1,v2)) 
# xAngle_MC1 = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(X_MC11, X_MC12) )
xAngle_MC1 = math.degrees(math.acos(vtk.vtkMath.Dot(X_MC11 , X_MC12) / (vtk.vtkMath.Norm(X_MC11) * vtk.vtkMath.Norm(X_MC12)) ))
# yAngle_MC1 = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(Y_MC11 , Y_MC12) )
yAngle_MC1 = math.degrees(math.acos(vtk.vtkMath.Dot(Y_MC11 , Y_MC12) / (vtk.vtkMath.Norm(Y_MC11) * vtk.vtkMath.Norm(Y_MC12)) ))
# zAngle_MC1 = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(Z_MC11 , Z_MC12) )
zAngle_MC1 = math.degrees(math.acos(vtk.vtkMath.Dot(Z_MC11 , Z_MC12) / (vtk.vtkMath.Norm(Z_MC11) * vtk.vtkMath.Norm(Z_MC12)) ))

# xAngle_TRP = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(X_TRP1, X_TRP2) )
xAngle_TRP = math.degrees(math.acos(vtk.vtkMath.Dot(X_TRP1 , X_TRP2) / (vtk.vtkMath.Norm(X_TRP1) * vtk.vtkMath.Norm(X_TRP2)) ))
# yAngle_TRP = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(Y_TRP1 , Y_TRP2) )
yAngle_TRP = math.degrees(math.acos(vtk.vtkMath.Dot(Y_TRP1 , Y_TRP2) / (vtk.vtkMath.Norm(Y_TRP1) * vtk.vtkMath.Norm(Y_TRP2)) ))
# zAngle_TRP = vtk.vtkMath.DegreesFromRadians( vtk.vtkMath.AngleBetweenVectors(Z_TRP1 , Z_TRP2) )
zAngle_TRP = math.degrees(math.acos(vtk.vtkMath.Dot(Z_TRP1 , Z_TRP2) / (vtk.vtkMath.Norm(Z_TRP1) * vtk.vtkMath.Norm(Z_TRP2)) ))

print('MC1:')
print('ANGLE BETWEEN X1 AND X2: {}'.format(xAngle_MC1))
print('ANGLE BETWEEN Y1 AND Y2: {}'.format(yAngle_MC1))
print('ANGLE BETWEEN Z1 AND Z2: {}'.format(zAngle_MC1))
print()
print('TRP:')
print('ANGLE BETWEEN X1 AND X2: {}'.format(xAngle_TRP))
print('ANGLE BETWEEN Y1 AND Y2: {}'.format(yAngle_TRP))
print('ANGLE BETWEEN Z1 AND Z2: {}'.format(zAngle_TRP))