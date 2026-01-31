#! /bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

. $script_dir/env

$script_dir/yocto-docker.sh "bitbake serialos-image"
$script_dir/yocto-docker.sh "\
    runqemu-extract-sdk /opt/serialos/yocto/build/tmp/deploy/images/$MACHINE/serialos-image-$MACHINE.rootfs.tar.bz2 /home/serialos/nfs && \
    runqemu-export-rootfs start /home/serialos/nfs && \
    /bin/bash \
"

# mounting the rootfs: sudo mount -o port=3049,nfsvers=3,proto=tcp,mountport=3048 -t nfs localhost:/home/serialos/nfs /mnt/usb/