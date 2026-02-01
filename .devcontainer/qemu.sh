#! /bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

TARGET=qemu

. $script_dir/env

$script_dir/yocto-docker.sh "bitbake serialos-image"
$script_dir/yocto-docker.sh "\
    qemu-img create -f qcow2 /home/serialos/data-img.qcow2 1G && \
    runqemu-extract-sdk /opt/serialos/yocto/build/tmp/deploy/images/$MACHINE/serialos-image-$MACHINE.rootfs.tar.bz2 /home/serialos/nfs && \
    runqemu $MACHINE /home/serialos/nfs slirp nographic qemuparams=\"-drive file=/home/serialos/data-img.qcow2,format=qcow2,if=virtio\" \
"
# $script_dir/yocto-docker.sh "\
#     qemu-img create -f qcow2 /home/serialos/data-img.qcow2 1G && \
#     runqemu serialos-image slirp nographic qemuparams=\"-drive file=/home/serialos/data-img.qcow2,format=qcow2,if=virtio\" \
# "
#    sudo tar -xf tmp/deploy/images/qemux86-64/serialos-image-qemux86-64.rootfs.tar.bz2 -C /nfs && \
