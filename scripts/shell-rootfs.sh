#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

if [ ! -d "$ROOTFS" ]; then
    $SCRIPT_DIR/populate-rootfs.sh
fi

SYSROOT_SETUP_SCRIPT=`which oe-find-native-sysroot 2> /dev/null`
if [ -z "$SYSROOT_SETUP_SCRIPT" ]; then
	echo "Error: Unable to find the oe-find-native-sysroot script"
	echo "Did you forget to source your build environment setup script?"
	exit 1
fi
. $SYSROOT_SETUP_SCRIPT qemu-helper-native

PSEUDO_LOCALSTATEDIR="$(realpath $ROOTFS).pseudo_state"
export PSEUDO_LOCALSTATEDIR

PSEUDO_OPTS="-P $OECORE_NATIVE_SYSROOT/usr"
$PSEUDO $PSEUDO_OPTS chroot $(realpath $ROOTFS)