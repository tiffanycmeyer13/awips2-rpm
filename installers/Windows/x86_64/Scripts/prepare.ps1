﻿#
# Script to extract the core ZIP file then CAVE and AlertViz zip files,
# then calls the script to assemble CAVE.
#
# SCRIPT HISTORY
#
# Date          Ticket#  Engineer    Description
# ------------- -------- ----------- ------------------------------------------------------
# Mar 11, 2015  4221     dlovely     Migration from AWIPS2_baseline plus added INNO Support
# Jun 26, 2015  4295     dlovely     Removed AlertViz and assemble CAVE
#

Set-Variable -name BUILD_ZIP -value $args[0]

$prepareDirectory = Split-Path ${A2_PREPARE_CAVE_DIR} -leaf
$prepareDirectoryContainer = Split-Path ${A2_PREPARE_CAVE_DIR} -parent
if ( Test-Path ${A2_PREPARE_CAVE_DIR} ) {
    Remove-Item -recurse -force ${A2_PREPARE_CAVE_DIR}
    if ($? -ne $true) { EXIT 1; }
}
New-Item -path $prepareDirectoryContainer `
    -name $prepareDirectory -type directory | Out-Null
if ($? -ne $true) { EXIT 1; }

pushd .
cd ${A2_PREPARE_CAVE_DIR}

# Extract the main zip.
& "$JAVA_JDK_DIR\bin\jar.exe" xvf ${A2_START_DIR}\${BUILD_ZIP}
if ( $? -ne $true ) {
    echo "FATAL: Failed to unzip ${BUILD_ZIP}".
    EXIT 1
}

popd

EXIT 0
