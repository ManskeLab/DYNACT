#!/bin/bash -u
SCRIPT_REG="/home/mkuczyns/Downloads/landmarks/DYNACT_XCT2CTReg.py"
OUTPUT_DIR="/home/mkuczyns/Downloads/landmarks/reg/"

MAIN="/home/mkuczyns/Downloads/landmarks/models/"
cd $MAIN

for DIR in */;
do
    # XCT Images
    XCT_MC1="${MAIN}${DIR}${DIR%/}e_MC1.nii"
    XCT_MC1_LAND="${MAIN}${DIR}${DIR%/}e_MC1_LAND.nii"
    XCT_TRP="${MAIN}${DIR}${DIR%/}e_TRP.nii"
    XCT_TRP_LAND="${MAIN}${DIR}${DIR%/}e_TRP_LAND.nii"

    # Static CT directories
    CT_MC1="${MAIN}${DIR}${DIR%/}a_BP_MC1.nii"
    CT_MC1_LAND="${MAIN}${DIR}${DIR%/}a_MC1_LAND.nii"
    CT_TRP="${MAIN}${DIR}${DIR%/}a_BP_TRP.nii"
    CT_TRP_LAND="${MAIN}${DIR}${DIR%/}a_TRP_LAND.nii"

    # DYNACT directories
    DYNACT_B_MC1="${MAIN}${DIR}/${DIR%/}b_MC1.nii"
    DYNACT_B_MC1_LAND="${MAIN}${DIR}/${DIR%/}b_MC1_LAND.nii"
    DYNACT_B_TRP="${MAIN}${DIR}/${DIR%/}b_TRP.nii"
    DYNACT_B_TRP_LAND="${MAIN}${DIR}/${DIR%/}b_TRP_LAND.nii"

    DYNACT_C_MC1="${MAIN}${DIR}/${DIR%/}c_MC1.nii"
    DYNACT_C_MC1_LAND="${MAIN}${DIR}/${DIR%/}c_MC1_LAND.nii"
    DYNACT_C_TRP="${MAIN}${DIR}/${DIR%/}c_TRP.nii"
    DYNACT_C_TRP_LAND="${MAIN}${DIR}/${DIR%/}c_TRP_LAND.nii"

    DYNACT_D_MC1="${MAIN}${DIR}/${DIR%/}d_MC1.nii"
    DYNACT_D_MC1_LAND="${MAIN}${DIR}/${DIR%/}d_MC1_LAND.nii"
    DYNACT_D_TRP="${MAIN}${DIR}/${DIR%/}d_TRP.nii"
    DYNACT_D_TRP_LAND="${MAIN}${DIR}/${DIR%/}d_TRP_LAND.nii"

    # Output
    OUTPUT_REG="${OUTPUT_DIR}${DIR}"


    # MC1
    cmd="python \"${SCRIPT_REG}\" \"${XCT_MC1}\" \"${XCT_MC1_LAND}\" \"${CT_MC1}\" \"${CT_MC1_LAND}\" \"${OUTPUT_REG}\""
    echo $cmd
    eval $cmd


    # TRP
    cmd="python \"${SCRIPT_REG}\" \"${XCT_TRP}\" \"${XCT_TRP_LAND}\" \"${CT_TRP}\" \"${CT_TRP_LAND}\" \"${OUTPUT_REG}\""
    echo $cmd
    eval $cmd

done