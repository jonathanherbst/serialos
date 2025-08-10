import podman
from podman.errors import exceptions

import argparse
import logging
import pathlib
import subprocess
import sys

mod_path = pathlib.Path(__file__).parent.resolve()
logger = logging.getLogger(__name__)

def find_git_root(path: pathlib.Path) -> pathlib.Path | None:
    if path.samefile("/"):
        return None
    elif not path.is_dir():
        return find_git_root(path.parent)
    elif not (path / ".git").exists():
        return find_git_root(path.parent)
    else:
        return path

def get_or_create_image(name: str, dockerfile: str):
    with podman.PodmanClient() as client:
        logger.info("looking for podman image %s" % name)
        try:
            image = client.images.get(name)
            dockerfile_mtime = (mod_path / dockerfile).stat().st_mtime
            image_mtime = image.history()[0]['Created']
            if dockerfile_mtime > image_mtime:
                logger.info("deleting old image")
                image.remove()
                image = None
        except exceptions.ImageNotFound:
            image = None

        if image is None:
            logger.info("creating a new image")
            image, logs = client.images.build(
                path = mod_path,
                tag = name,
                dockerfile = dockerfile,
            )

        logger.info("using podman image %s" % image.id)
        return image

def get_yocto_image():
    return get_or_create_image("serialos/yocto", "Dockerfile.yocto")

def get_nfs_image():
    return get_or_create_image("serialos/nfs", "Dockerfile.nfs")

yocto_machine = {
    'qemu': "qemux86-64",
    'rpi-zero2w64': "raspberrypi0-2w-64-serialos",
}

def yocto_shell(machine: str, command: str):
    image = get_yocto_image()
    project_dir = find_git_root(mod_path)
    shell_cmd = '''podman run --rm -it \\
            --entrypoint="/bin/bash" \\
            --user="yocto" \\
            --userns=keep-id \\
            -v "{project_dir}:/opt/project" \\
            -w /opt/project \\
            -e MACHINE={mach} \\
            -e DISTRO=megaserial \\
            -e ENABLE_UART=1 \\
            -e TERM=xterm-256color \\
            -e BBLAYERS=" \\
                /opt/project/yocto/poky/meta \\
                /opt/project/yocto/poky/meta-poky \\
                /opt/project/yocto/poky/meta-yocto-bsp \\
                /opt/project/yocto/meta-ti/meta-beagle \\
                /opt/project/yocto/meta-ti/meta-ti-bsp \\
                /opt/project/yocto/meta-raspberrypi \\
                /opt/project/yocto/meta-arm/meta-arm \\
                /opt/project/yocto/meta-arm/meta-arm-toolchain \\
                /opt/project/yocto/meta-megaserial \\
            " \\
            -e BB_ENV_PASSTHROUGH_ADDITIONS="BBLAYERS ENABLE_UART" \\
            {image_id} \\
            -c " \\
                set -x && \\
                cd /opt/project/yocto && \\
                . poky/oe-init-build-env && \\
                {command} \\
            "'''.format(project_dir=project_dir, mach=yocto_machine[machine], image_id=image.id, command=command)

    subprocess.run(shell_cmd, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def nfs_server(archive_path: pathlib.Path):
    archive_path = archive_path.resolve()
    image = get_nfs_image()
    extension = ''.join(archive_path.suffixes)
    shell_cmd = '''podman run --rm -it \\
            --entrypoint="/bin/bash" \\
            --user="nfs" \\
            -v "{archive_path}:/archive{extension}" \\
            -p 11111:11111/tcp \\
            {image_id} -c " \\
                set -x && \\
                sudo tar -xf /archive{extension} -C /mnt && \\
                sudo /usr/local/cargo/bin/cargo-nfs3-server --path /mnt/ \\
            " \\
    '''.format(archive_path=archive_path, extension=extension, image_id=image.id)

    subprocess.run(shell_cmd, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def parse_args():
    parser = argparse.ArgumentParser(
            prog="dev.py",
            description="Dev tools for serialos",
    )

    commands = parser.add_subparsers(dest="command", required=True)
    shell_command = commands.add_parser("shell", help="Get a shell with the yocto environment setup")
    nfs_command = commands.add_parser("nfs", help="Create an nfs share with from a rootfs tar file")

    _ = shell_command.add_argument("machine", help="Machine to setup the shell for", choices=yocto_machine.keys())

    _ = nfs_command.add_argument("archive", help="Path to an archive to share", type=pathlib.Path)

    return parser.parse_args()

def shell_cmd(_args):
    yocto_shell("qemu", "/bin/bash")

def nfs_cmd(args):
    nfs_server(args.archive)

if __name__ == "__main__":
    logging.basicConfig(stream = sys.stdout, level = logging.INFO)

    commands = {
        "shell": shell_cmd,
        "nfs": nfs_cmd,
    }

    args = parse_args()
    commands[args.command](args)
