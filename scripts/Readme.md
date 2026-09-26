# Scripts

This directory contains a bunch of scripts for interacting with the build system.

## bitbake.sh <bitbake_args>

Run a bitbake command on the build system.

## populate-rootfs.sh [rebuild]

Populate a rootfs directory for use with qemu or nfs in the `rootfs` directory.

## shell-rootfs.sh

Get a chrooted shell into the rootfs directory so the rootfs can be modified with the users and permissions in qemu and nfs.

## nfs.sh

Host the rootfs as an NFS share

## qemu.sh

Run an image in QEMU

## yocto-env

This is a script meant to source instead of run to setup the build environment, most of the scripts source this file internally.
