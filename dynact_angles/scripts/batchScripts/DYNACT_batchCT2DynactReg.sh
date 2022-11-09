#!/bin/bash -u
SCRIPT_REG="/Users/mkuczyns/Projects/DYNACT/dynact_process/scripts/DYNACT_XCT2CTReg.py"
OUTPUT_DIR="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/"

MAIN="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/"
cd $MAIN

for DIR in */;
do
    # Static CT directories
    CT_MC1="${MAIN}${DIR}staticCT/${DIR%/}a_BP_MC1.nii"
    CT_MC1_LAND="${MAIN}${DIR}staticCT/${DIR%/}a_MC1_LAND.nii"
    CT_TRP="${MAIN}${DIR}staticCT/${DIR%/}a_BP_TRP.nii"
    CT_TRP_LAND="${MAIN}${DIR}staticCT/${DIR%/}a_TRP_LAND.nii"

    # DYNACT directories
    DYNACT_B_MC1="${MAIN}${DIR}dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_B_MC1_LAND="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_MC1_LAND.nii"
    DYNACT_B_TRP="${MAIN}${DIR}dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_B_TRP_LAND="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_TRP_LAND.nii"

    DYNACT_C_MC1="${MAIN}${DIR}dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_C_MC1_LAND="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_MC1_LAND.nii"
    DYNACT_C_TRP="${MAIN}${DIR}dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_C_TRP_LAND="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_TRP_LAND.nii"

    DYNACT_D_MC1="${MAIN}${DIR}dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_D_MC1_LAND="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_MC1_LAND.nii"
    DYNACT_D_TRP="${MAIN}${DIR}dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_D_TRP_LAND="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_TRP_LAND.nii"

    # Output
    OUTPUT_REG_B="${OUTPUT_DIR}${DIR}staticCT_to_dynamicCT/B"
    OUTPUT_REG_C="${OUTPUT_DIR}${DIR}staticCT_to_dynamicCT/C"
    OUTPUT_REG_D="${OUTPUT_DIR}${DIR}staticCT_to_dynamicCT/D"


    # MC1
    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_B_MC1}\" \"${DYNACT_B_MC1_LAND}\" \"${CT_MC1}\" \"${CT_MC1_LAND}\" \"${OUTPUT_REG_B}\""
    echo $cmd
    eval $cmd

    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_C_MC1}\" \"${DYNACT_C_MC1_LAND}\" \"${CT_MC1}\" \"${CT_MC1_LAND}\" \"${OUTPUT_REG_C}\""
    echo $cmd
    eval $cmd

    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_D_MC1}\" \"${DYNACT_D_MC1_LAND}\" \"${CT_MC1}\" \"${CT_MC1_LAND}\" \"${OUTPUT_REG_D}\""
    echo $cmd
    eval $cmd


    # TRP
    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_B_TRP}\" \"${DYNACT_B_TRP_LAND}\" \"${CT_TRP}\" \"${CT_TRP_LAND}\" \"${OUTPUT_REG_B}\""
    echo $cmd
    eval $cmd

    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_C_TRP}\" \"${DYNACT_C_TRP_LAND}\" \"${CT_TRP}\" \"${CT_TRP_LAND}\" \"${OUTPUT_REG_C}\""
    echo $cmd
    eval $cmd

    cmd="python \"${SCRIPT_REG}\" \"${DYNACT_D_TRP}\" \"${DYNACT_D_TRP_LAND}\" \"${CT_TRP}\" \"${CT_TRP_LAND}\" \"${OUTPUT_REG_D}\""
    echo $cmd
    eval $cmd

done