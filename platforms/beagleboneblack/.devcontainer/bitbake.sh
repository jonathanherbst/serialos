#! /bin/sh

DOCKER=podman

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
project_dir="${script_dir}/.."
docker_project_dir="/opt/megaserial/"
dockerfile="${script_dir}/Dockerfile"
image_name="megaserial/bbb-builder"

${DOCKER} build \
    -t "${image_name}" \
    -f "${script_dir}/Dockerfile" \
    "${project_dir}"

BITBAKE_ARGS="$@"

${DOCKER} run --rm -it \
    --entrypoint="/bin/bash" \
    --user="megaserial" \
    --userns=keep-id \
    -v "${project_dir}:${docker_project_dir}" \
    -w "${docker_project_dir}" \
    -e MACHINE="beaglebone" \
    -e BBLAYERS=" \
        ${docker_project_dir}/poky/meta \
        ${docker_project_dir}/poky/meta-poky \
        ${docker_project_dir}/poky/meta-yocto-bsp \
        ${docker_project_dir}/meta-ti/meta-beagle \
        ${docker_project_dir}/meta-ti/meta-ti-bsp \
        ${docker_project_dir}/meta-arm/meta-arm \
        ${docker_project_dir}/meta-arm/meta-arm-toolchain \
    " \
    -e BB_ENV_PASSTHROUGH_ADDITIONS="BBLAYERS" \
    "${image_name}" -c " \
        set -x && \
        cd ${docker_project_dir} && \
        ls -lh && \
        . poky/oe-init-build-env && \
        bitbake $BITBAKE_ARGS \
    "