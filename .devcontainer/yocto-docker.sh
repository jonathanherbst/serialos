#! /bin/sh

DOCKER="${DOCKER:=podman}"
TARGET="${TARGET:=qemu}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
project_dir="${script_dir}/.."
docker_project_dir="/opt/megaserial/"
dockerfile="${script_dir}/Dockerfile"
image_name="megaserial/bbb-builder"

MACHINE=""
case "$TARGET" in
    "qemu")
        MACHINE=qemux86-64
        ;;
    "rpi-zero2w64")
        MACHINE="raspberrypi0-2w-64-serialos"
        ;;
    "bb-black")
        MACHINE="beagleboneblack-megaserial"
        ;;
esac

echo "Building for target: $TARGET, machine: $MACHINE"

${DOCKER} buildx build \
    -t "${image_name}" \
    -f "${script_dir}/Dockerfile" \
    "${project_dir}"

COMMAND="$@"

DOCKER_EXTRA="--userns=keep-id"

${DOCKER} run --rm -it \
    --entrypoint="/bin/bash" \
    --user="megaserial" \
    $DOCKER_EXTRA \
    -v "${project_dir}:${docker_project_dir}" \
    -w "${docker_project_dir}" \
    -e MACHINE="$MACHINE" \
    -e DISTRO="megaserial" \
    -e ENABLE_UART=1 \
    -e TERM="xterm-256color" \
    -e BBLAYERS=" \
        ${docker_project_dir}/yocto/poky/meta \
        ${docker_project_dir}/yocto/poky/meta-poky \
        ${docker_project_dir}/yocto/poky/meta-yocto-bsp \
        ${docker_project_dir}/yocto/meta-ti/meta-beagle \
        ${docker_project_dir}/yocto/meta-ti/meta-ti-bsp \
        ${docker_project_dir}/yocto/meta-raspberrypi \
        ${docker_project_dir}/yocto/meta-arm/meta-arm \
        ${docker_project_dir}/yocto/meta-arm/meta-arm-toolchain \
        ${docker_project_dir}/yocto/meta-megaserial \
    " \
    -e BB_ENV_PASSTHROUGH_ADDITIONS="BBLAYERS ENABLE_UART" \
    "${image_name}" -c " \
        set -x && \
        cd ${docker_project_dir}/yocto && \
        . poky/oe-init-build-env && \
        $COMMAND \
    "
