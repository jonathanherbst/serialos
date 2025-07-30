#! /bin/sh

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
project_dir="${script_dir}/.."
image_name="serialos/nfs-server"

archive_path="$1"
archive_file="$(basename $archive_path)"
archive_ext="${archive_file#*.}"
archive_docker="/archive.$archive_ext"

echo "archive ext: $archive_ext"

podman buildx build \
    -t "${image_name}" \
    -f "${script_dir}/Dockerfile" \
    "${script_dir}"

podman run --rm -it \
    --entrypoint="/bin/bash" \
    --user="serialos" \
    --userns=keep-id \
    -v "$archive_path:$archive_docker" \
    -p 11111:11111/tcp \
    "${image_name}" -c " \
        set -x && \
        sudo tar -xf $archive_docker -C /mnt && \
        sudo /usr/local/cargo/bin/cargo-nfs3-server --path /mnt/ \
    "
