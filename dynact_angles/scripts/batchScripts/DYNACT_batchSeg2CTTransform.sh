#!/bin/bash -u
SCRIPT="/Users/mkuczyns/Projects/DYNACT/dynact_process/scripts/DYNACT_transform.py"

# DYNACT1_002
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_002/staticCT/DYNACT1_002a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_002/HR-pQCT/DYNACT1_002e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_002/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_002/staticCT_to_HR-pQCT/DYNACT1_002a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_002/staticCT/DYNACT1_002a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_002/HR-pQCT/DYNACT1_002e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_002/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_002/staticCT_to_HR-pQCT/DYNACT1_002a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_003
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_003/staticCT/DYNACT1_003a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_003/HR-pQCT/DYNACT1_003e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_003/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_003/staticCT_to_HR-pQCT/DYNACT1_003a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_003/staticCT/DYNACT1_003a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_003/HR-pQCT/DYNACT1_003e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_003/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_003/staticCT_to_HR-pQCT/DYNACT1_003a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_004
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_004/staticCT/DYNACT1_004a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_004/HR-pQCT/DYNACT1_004e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_004/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_004/staticCT_to_HR-pQCT/DYNACT1_004a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_004/staticCT/DYNACT1_004a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_004/HR-pQCT/DYNACT1_004e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_004/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_004/staticCT_to_HR-pQCT/DYNACT1_004a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_005
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_005/staticCT/DYNACT1_005a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_005/HR-pQCT/DYNACT1_005e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_005/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_005/staticCT_to_HR-pQCT/DYNACT1_005a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_005/staticCT/DYNACT1_005a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_005/HR-pQCT/DYNACT1_005e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_005/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_005/staticCT_to_HR-pQCT/DYNACT1_005a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_006
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/HR-pQCT/DYNACT1_006e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_HR-pQCT/DYNACT1_006a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/HR-pQCT/DYNACT1_006e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_HR-pQCT/DYNACT1_006a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_007
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_007/staticCT/DYNACT1_007a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_007/HR-pQCT/DYNACT1_007e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_007/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_007/staticCT_to_HR-pQCT/DYNACT1_007a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_007/staticCT/DYNACT1_007a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_007/HR-pQCT/DYNACT1_007e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_007/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_007/staticCT_to_HR-pQCT/DYNACT1_007a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_008
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_008/staticCT/DYNACT1_008a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_008/HR-pQCT/DYNACT1_008e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_008/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_008/staticCT_to_HR-pQCT/DYNACT1_008a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_008/staticCT/DYNACT1_008a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_008/HR-pQCT/DYNACT1_008e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_008/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_008/staticCT_to_HR-pQCT/DYNACT1_008a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_009
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/HR-pQCT/DYNACT1_009e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_HR-pQCT/DYNACT1_009a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/HR-pQCT/DYNACT1_009e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_HR-pQCT/DYNACT1_009a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

# DYNACT1_010
FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_010/staticCT/DYNACT1_010a_BP_MC1.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_010/HR-pQCT/DYNACT1_010e_MC1_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_010/staticCT_to_HR-pQCT/CT2XCT_MC1_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_010/staticCT_to_HR-pQCT/DYNACT1_010a_MC1_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd

FIXED="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_010/staticCT/DYNACT1_010a_BP_TRP.nii"
MOVING="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_010/HR-pQCT/DYNACT1_010e_TRP_SEG.nii"
TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_010/staticCT_to_HR-pQCT/CT2XCT_TRP_REG.tfm"
OUTPUT="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_010/staticCT_to_HR-pQCT/DYNACT1_010a_TRP_SEG.nii"
INTERP="nn"
INV="True"

cmd="python \"${SCRIPT}\" \"${FIXED}\" \"${MOVING}\" \"${TFM}\" -o \"${OUTPUT}\" -i \"${INTERP}\" -r \"${INV}\""
echo $cmd
eval $cmd