#! /bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

TARGET=qemu

$script_dir/yocto-docker.sh "bitbake megaserial-image"
$script_dir/yocto-docker.sh "\
    qemu-img create -f qcow2 /home/megaserial/data-img.qcow2 1G && \
    runqemu megaserial-image slirp nographic qemuparams=\"-drive file=/home/megaserial/data-img.qcow2,format=qcow2,if=virtio\" \
"
#    sudo tar -xf tmp/deploy/images/qemux86-64/megaserial-image-qemux86-64.rootfs.tar.bz2 -C /nfs && \
