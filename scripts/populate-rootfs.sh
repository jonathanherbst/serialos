#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

rootfs_tar=$PROJECT_DIR/yocto/build/tmp/deploy/images/$MACHINE/$IMAGE-$MACHINE.rootfs.tar.zst
if [[ $1 == "rebuild" ]] || [ ! -f $rootfs_tar ]; then 
    $SCRIPT_DIR/bitbake.sh $IMAGE
fi

if [[ $1 == "rebuild" ]]; then
    rm -rf $ROOTFS*
fi

mkdir -p $ROOTFS
if [[ $TARGET == qemu* ]] && [ ! -f "$ROOTFS/../data-img.qcow2" ]; then
    qemu-img create -f qcow2 $ROOTFS/../data-img.qcow2 1G
fi
runqemu-extract-sdk $rootfs_tar $ROOTFS