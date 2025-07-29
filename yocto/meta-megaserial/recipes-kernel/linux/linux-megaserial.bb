SUMMARY = "Megaserial Linux"
SECTION = "kernel"
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=6bc538ed5bd9a7fc9398086aedcd7e46"

inherit kernel

LINUX_VMAJOR = "6"
LINUX_VMINOR = "6"
LINUX_VPATCH = "91"
SRCREV = "525684d28fadc2bdae5424f28b219377bd5d4639"

LINUX_STABLE_BRANCH = "v6.6.32-ti-arm32-r7"
PV = "6.6.32+git"

LINUX_STABLE_GIT_URI ?= "git://github.com/beagleboard/linux.git;protocol=https"
SRC_URI = "${LINUX_STABLE_GIT_URI};branch=${LINUX_STABLE_BRANCH}"
S = "${WORKDIR}/git"

SRC_URI:append = " \
    file://defconfig \
"
