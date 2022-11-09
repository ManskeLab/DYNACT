#!/bin/bash -u
SCRIPT_TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/scripts/DYNACT_transform.py"

REG="/Users/mkuczyns/Projects/DYNACT/dynact_process/reg/"
MAIN="/Users/mkuczyns/Projects/DYNACT/dynact_process/models/"
cd $MAIN

for DIR in */;
do
    # Input XCT segmentation images (to be transformed)
    SEG_MC1="${REG}${DIR}staticCT_to_HR-pQCT/${DIR%/}a_MC1_SEG.nii"
    SEG_TRP="${REG}${DIR}staticCT_to_HR-pQCT/${DIR%/}a_TRP_SEG.nii"

    #-------------------------------------
    #           DYNACT1_B
    #-------------------------------------
    # Fixed (reference) DYNACT image
    DYNACT_IMG="${MAIN}${DIR}dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii"

    # CT to DYNACT transformation matrix
    TFM_MC1="${REG}${DIR}staticCT_to_dynamicCT/B/CT2DYNACT_MC1_REG.tfm"
    TFM_TRP="${REG}${DIR}staticCT_to_dynamicCT/B/CT2DYNACT_TRP_REG.tfm"

    # Output segmentation (after transformation)
    OUTPUT_SEG_MC1="${REG}${DIR}staticCT_to_dynamicCT/B/${DIR%/}b_MC1_SEG.nii"
    OUTPUT_SEG_TRP="${REG}${DIR}staticCT_to_dynamicCT/B/${DIR%/}b_TRP_SEG.nii"

    # MC1 Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_MC1}\" \"${TFM_MC1}\" -o \"${OUTPUT_SEG_MC1}\" -i nn"
    echo $cmd
    eval $cmd

    # TRP Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_TRP}\" \"${TFM_TRP}\" -o \"${OUTPUT_SEG_TRP}\" -i nn"
    echo $cmd
    eval $cmd


    #-------------------------------------
    #           DYNACT1_C
    #-------------------------------------
    # Fixed (reference) DYNACT image
    DYNACT_IMG="${MAIN}${DIR}dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii"

    # CT to DYNACT transformation matrix
    TFM_MC1="${REG}${DIR}staticCT_to_dynamicCT/C/CT2DYNACT_MC1_REG.tfm"
    TFM_TRP="${REG}${DIR}staticCT_to_dynamicCT/C/CT2DYNACT_TRP_REG.tfm"

    # Output segmentation (after transformation)
    OUTPUT_SEG_MC1="${REG}${DIR}staticCT_to_dynamicCT/C/${DIR%/}c_MC1_SEG.nii"
    OUTPUT_SEG_TRP="${REG}${DIR}staticCT_to_dynamicCT/C/${DIR%/}c_TRP_SEG.nii"

    # MC1 Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_MC1}\" \"${TFM_MC1}\" -o \"${OUTPUT_SEG_MC1}\" -i nn"
    echo $cmd
    eval $cmd

    # TRP Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_TRP}\" \"${TFM_TRP}\" -o \"${OUTPUT_SEG_TRP}\" -i nn"
    echo $cmd
    eval $cmd


    #-------------------------------------
    #           DYNACT1_D
    #-------------------------------------
    # Fixed (reference) DYNACT image
    DYNACT_IMG="${MAIN}${DIR}dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii"

    # CT to DYNACT transformation matrix
    TFM_MC1="${REG}${DIR}staticCT_to_dynamicCT/D/CT2DYNACT_MC1_REG.tfm"
    TFM_TRP="${REG}${DIR}staticCT_to_dynamicCT/D/CT2DYNACT_TRP_REG.tfm"

    # Output segmentation (after transformation)
    OUTPUT_SEG_MC1="${REG}${DIR}staticCT_to_dynamicCT/D/${DIR%/}d_MC1_SEG.nii"
    OUTPUT_SEG_TRP="${REG}${DIR}staticCT_to_dynamicCT/D/${DIR%/}d_TRP_SEG.nii"

    # MC1 Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_MC1}\" \"${TFM_MC1}\" -o \"${OUTPUT_SEG_MC1}\" -i nn"
    echo $cmd
    eval $cmd

    # TRP Transformation
    cmd="python \"${SCRIPT_TFM}\" \"${DYNACT_IMG}\" \"${SEG_TRP}\" \"${TFM_TRP}\" -o \"${OUTPUT_SEG_TRP}\" -i nn"
    echo $cmd
    eval $cmd

done

# SCRIPT_TFM="/Users/mkuczyns/Projects/DYNACT/dynact_process/scripts/DYNACT_XCT2CTReg.py"

# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/B/RESAMPLED/DYNACT1_006b_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_dynamicCT/B"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/C/RESAMPLED/DYNACT1_006c_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_dynamicCT/C"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/dynamicCT/D/RESAMPLED/DYNACT1_006d_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_006/staticCT/DYNACT1_006a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_006/staticCT_to_dynamicCT/D"
# eval $cmd

# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/B/RESAMPLED/DYNACT1_009b_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_MC1.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/B"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/C/RESAMPLED/DYNACT1_009c_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_MC1.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/C"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/D/RESAMPLED/DYNACT1_009d_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_MC1.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_MC1_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/D"
# eval $cmd

# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/B/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/B/RESAMPLED/DYNACT1_009b_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/B"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/C/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/C/RESAMPLED/DYNACT1_009c_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/C"
# eval $cmd
# cmd="python \"${SCRIPT_TFM}\" /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/D/RESAMPLED/Volume_1_Resampled.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/dynamicCT/D/RESAMPLED/DYNACT1_009d_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_BP_TRP.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/models/DYNACT1_009/staticCT/DYNACT1_009a_TRP_LAND.nii /Users/mkuczyns/Projects/DYNACT/dynact_process/reg/DYNACT1_009/staticCT_to_dynamicCT/D"
# eval $cmd

