#! /bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

TARGET=qemu

$script_dir/yocto-docker.sh "bitbake megaserial-image"
$script_dir/yocto-docker.sh "ip addr && runqemu megaserial-image slirp nographic"
