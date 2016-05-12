#!/usr/bin/env bash

echo "[INFO] Running Generate Template from Summary ..."

# Create Temp Folder
TMP_DIR=$(mktemp -d)

# Copy all contents into Temp Folder
for dir in summary/*/
do
    DIR=${dir%*/}
    echo "[INFO] Copying ${DIR##*/} ..."
    cp -r ${DIR}/* ${TMP_DIR}/
done

# Remove all files (timeunit and time) in Temp Folder
pushd ${TMP_DIR}/
    echo '[INFO] Removing the "timeunit" and "time" folders and files ...'
    find . -name "*.time" -type f -delete
    find . -name "*.time.*" -type f -delete
    find . -name "*.timeunit" -type d -delete
popd

# Copy Temp to Template folder
echo "[INFO] Copying result to template folder ..."
mkdir -p template
cp -r ${TMP_DIR}/* template/

# Remove Temp Folder
rm -rf "${TMP_DIR}"

tree template
echo "[INFO] Generate Template from Summary Done."
