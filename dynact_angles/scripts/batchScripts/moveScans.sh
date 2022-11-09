#!/bin/bash -u
OUTPUT_DIR="/Users/mkuczyns/OneDrive - University of Calgary/ManskeLabImages/DYNACT/landmarks/"
MAIN="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/"
cd $MAIN

for DIR in */;
do
    # XCT Images
    XCT_MC1="${MAIN}${DIR}HR-pQCT/${DIR%/}e_MC1.nii"
    XCT_MC1_LAND="${MAIN}${DIR}HR-pQCT/${DIR%/}e_MC1_LAND.nii"
    XCT_TRP="${MAIN}${DIR}HR-pQCT/${DIR%/}e_TRP.nii"
    XCT_TRP_LAND="${MAIN}${DIR}HR-pQCT/${DIR%/}e_TRP_LAND.nii"

    # Static CT directories
    CT_MC1="${MAIN}${DIR}staticCT/${DIR%/}a_BP_MC1.nii"
    CT_MC1_LAND="${MAIN}${DIR}staticCT/${DIR%/}a_MC1_LAND.nii"
    CT_TRP="${MAIN}${DIR}staticCT/${DIR%/}a_BP_TRP.nii"
    CT_TRP_LAND="${MAIN}${DIR}staticCT/${DIR%/}a_TRP_LAND.nii"

    # DYNACT directories
    DYNACT_B_MC1="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_MC1"
    DYNACT_B_MC1_LAND="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_MC1_LAND.nii"
    DYNACT_B_TRP="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_TRP"
    DYNACT_B_TRP_LAND="${MAIN}${DIR}dynamicCT/B/RESAMPLED/${DIR%/}b_TRP_LAND.nii"
    DYNACT_B_VOLUME1_RESAMPLED="${MAIN}${DIR}dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_B_VOLUME1_OUT="${OUTPUT_DIR}${DIR%/}b_Volume_1_Resampled.nii"

    DYNACT_C_MC1="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_MC1"
    DYNACT_C_MC1_LAND="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_MC1_LAND.nii"
    DYNACT_C_TRP="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_TRP"
    DYNACT_C_TRP_LAND="${MAIN}${DIR}dynamicCT/C/RESAMPLED/${DIR%/}c_TRP_LAND.nii"
    DYNACT_C_VOLUME1_RESAMPLED="${MAIN}${DIR}dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_C_VOLUME1_OUT="${OUTPUT_DIR}${DIR%/}c_Volume_1_Resampled.nii"

    DYNACT_D_MC1="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_MC1"
    DYNACT_D_MC1_LAND="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_MC1_LAND.nii"
    DYNACT_D_TRP="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_TRP"
    DYNACT_D_TRP_LAND="${MAIN}${DIR}dynamicCT/D/RESAMPLED/${DIR%/}d_TRP_LAND.nii"
    DYNACT_D_VOLUME1_RESAMPLED="${MAIN}${DIR}dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii"
    DYNACT_D_VOLUME1_OUT="${OUTPUT_DIR}${DIR%/}d_Volume_1_Resampled.nii"


    cmd="cp \"${DYNACT_B_VOLUME1_RESAMPLED}\" \"${DYNACT_B_VOLUME1_OUT}\""
    echo $cmd
    eval $cmd
    cmd="cp \"${DYNACT_C_VOLUME1_RESAMPLED}\" \"${DYNACT_C_VOLUME1_OUT}\""
    echo $cmd
    eval $cmd
    cmd="cp \"${DYNACT_D_VOLUME1_RESAMPLED}\" \"${DYNACT_D_VOLUME1_OUT}\""
    echo $cmd
    eval $cmd

    # cmd="cp \"${XCT_MC1_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    # cmd="cp \"${XCT_TRP_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    
    # cmd="cp \"${CT_MC1_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    # cmd="cp \"${CT_TRP_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd

    # cmd="cp \"${DYNACT_B_MC1_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    # cmd="cp \"${DYNACT_B_TRP_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd

    # cmd="cp \"${DYNACT_C_MC1_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    # cmd="cp \"${DYNACT_C_TRP_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd

    # cmd="cp \"${DYNACT_D_MC1_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd
    # cmd="cp \"${DYNACT_D_TRP_LAND}\" \"${OUTPUT_DIR}\""
    # echo $cmd
    # eval $cmd

done