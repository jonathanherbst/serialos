#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

command=${1:-start}
rootfs="$(realpath $ROOTFS)"
runqemu-export-rootfs $command $rootfs

# something like the following to test mounting this on your host computer
# sudo mount -o port=3049,mountport=3048,tcp,nfsvers=3 localhost:/workspaces/serialos/rootfs/beaglebone-black/serialos-bare-image/rootfs /mnt/