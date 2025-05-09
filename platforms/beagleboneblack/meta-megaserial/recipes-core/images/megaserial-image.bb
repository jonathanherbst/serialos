SUMMARY = "A small image just capable of allowing a device to boot."

IMAGE_LINGUAS = " "
LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE ?= "8192"
IMAGE_ROOTFS_EXTRA_SPACE:append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 4096", "", d)}"

IMAGE_INSTALL = " \
    packagegroup-core-boot \
    ${MEGASERIAL_EXTRA_INSTALL} \
"

MEGASERIAL_EXTRA_INSTALL = " \
    packagegroup-core-ssh-dropbear \
    screen \
"