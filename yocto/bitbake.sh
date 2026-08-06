#! /usr/bin/env bash

yocto_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
build_dir="${yocto_dir}/build"

export MACHINE=${MACHINE:-beagle-serialos}
export DISTRO=${DISTRO:-serialos}
export BBLAYERS=" \
    ${yocto_dir}/poky/meta \
    ${yocto_dir}/poky/meta-poky \
    ${yocto_dir}/poky/meta-yocto-bsp \
    ${yocto_dir}/meta-ti/meta-beagle \
    ${yocto_dir}/meta-ti/meta-ti-bsp \
    ${yocto_dir}/meta-raspberrypi \
    ${yocto_dir}/meta-arm/meta-arm \
    ${yocto_dir}/meta-arm/meta-arm-toolchain \
    ${yocto_dir}/meta-serialos \
"
BB_ENV_PASSTHROUGH_ADDITIONS="BBLAYERS"

source "${yocto_dir}/poky/oe-init-build-env" "${build_dir}"

bitbake "$@"
