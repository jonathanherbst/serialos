#! /bin/sh

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
project_dir="${script_dir}/.."
image_name="serialos/nfs-server"

podman buildx build \
    -t "${image_name}" \
    -f "${script_dir}/Dockerfile" \
    "${script_dir}"

podman run --rm -it \
    --entrypoint="/bin/bash" \
    --user="serialos" \
    --userns=keep-id \
    "${image_name}" -c " \
        set -x && \
        sudo service rpcbind start && \
        sudo service dbus start && \
        sudo ganesha.nfsd -L STDOUT -F \
    "
