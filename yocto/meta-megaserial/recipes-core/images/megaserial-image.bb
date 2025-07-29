SUMMARY = "A small image just capable of allowing a device to boot."

IMAGE_LINGUAS = " "
LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE ?= "8192"

IMAGE_FEATURES:append = " \
    ssh-server-dropbear \
"

IMAGE_INSTALL = " \
    packagegroup-core-boot \
    ${MEGASERIAL_EXTRA_INSTALL} \
"

MEGASERIAL_EXTRA_INSTALL = " \
    screen \
    btrfs-tools \
"
