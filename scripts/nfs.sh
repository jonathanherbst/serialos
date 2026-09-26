#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

command=${1:-start}
rootfs="$(realpath $ROOTFS)"
runqemu-export-rootfs $command $rootfs