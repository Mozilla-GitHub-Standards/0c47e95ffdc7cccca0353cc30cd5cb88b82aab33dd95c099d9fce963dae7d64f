#!/usr/bin/env bash

# Create Temp Folder
TMP_DIR=$(mktemp -d)


echo "[INFO] Running Generate Template from Summary Folder ..."
# Copy all contents into Temp Folder
for dir in summary/*/
do
    DIR=${dir%*/}
    echo "[INFO] Copying ${DIR##*/} ..."
    cp -r ${DIR}/* ${TMP_DIR}/
done


echo "[INFO] Running Generate Template from Bugzilla Folder ..."
# Copy all contents into Temp Folder
for dir in bugzilla/*/
do
    DIR=${dir%*/}
    echo "[INFO] Copying ${DIR##*/} ..."
    cp -r ${DIR}/* ${TMP_DIR}/
done


# Remove all files (timeunit and time) in Temp Folder
pushd ${TMP_DIR}/
    echo '[INFO] Removing the "timeunit" and "time" folders and files ...'
    find . -type d -name "*.timeunit" -delete
    find . -type f -name "*.time" -delete
    find . -type f -name "*.time.*" -delete
    find . -type f -regex ".*[0-9]\{1,\}\([.][0-9]\{1,3\}\)\{1,2\}$" -delete
popd

# Copy Temp to Template folder
echo "[INFO] Copying result to template folder ..."
mkdir -p template
cp -r ${TMP_DIR}/* template/

echo "[INFO] Creating placeholders ..."
find template/ -name "*::*" -print0 | xargs -0 -I % touch %/placeholder

# Remove Temp Folder
rm -rf "${TMP_DIR}"

#tree template
echo "[INFO] Generate Template from Summary Done."
echo '[INFO] Run "$ tree template/" to check the result.'

