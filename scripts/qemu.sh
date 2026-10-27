#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

set -x

if [ ! -d "$ROOTFS" ]; then
    $SCRIPT_DIR/populate-rootfs.sh $@
fi

data_img="$(realpath $ROOTFS/../data-img.qcow2)"
if [ -f $data_img ]; then
    qemuparams="-drive file=$data_img,format=qcow2,if=virtio"
fi

rootfs="$(realpath $ROOTFS)"
runqemu $rootfs slirp nographic qemuparams="$qemuparams"