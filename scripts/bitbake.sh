#! /bin/bash

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/yocto-env"

bitbake $@