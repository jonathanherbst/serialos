#! /bin/sh

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

BITBAKE_ARGS="$@"

$script_dir/yocto-docker.sh "bitbake $BITBAKE_ARGS"

