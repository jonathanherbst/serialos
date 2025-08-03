import podman
from podman.errors import exceptions

import logging
import os
import pathlib
import subprocess
import sys

mod_path = pathlib.Path(__file__).parent.resolve()
logger = logging.getLogger(__name__)

def find_git_root(path: pathlib.Path):
    if path.samefile("/"):
        return None
    elif not path.is_dir():
        return find_git_root(path.parent)
    elif not (path / ".git").exists():
        return find_git_root(path.parent)
    else:
        return path

def get_yocto_image():
    with podman.PodmanClient() as client:
        name = "serialos/yocto-builder"
        logger.info("looking for podman image %s" % name)
        try:
            image = client.images.get(name)
            dockerfile_mtime = (mod_path / "Dockerfile.yocto").stat().st_mtime
            image_mtime = image.history()[0]['Created']
            if dockerfile_mtime > image_mtime:
                logger.info("found an old image")
                image.remove()
                image = None
        except exceptions.ImageNotFound:
            image = None

        if image is None:
            logger.info("creating a new image")
            image, logs = client.images.build(
                path = mod_path,
                tag = "serialos/yocto-builder",
                dockerfile = "./Dockerfile.yocto",
            )

        logger.info("using podman image %s" % image.id)
        return image

yocto_machine = {
    'qemu': "qemux86-64"
}

def yocto_shell(machine):
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
                /bin/bash \\
            "'''.format(project_dir=project_dir, mach=yocto_machine[machine], image_id=image.id)

    subprocess.run(shell_cmd, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

if __name__ == "__main__":
    logging.basicConfig(stream = sys.stdout, level = logging.INFO)
    yocto_shell("qemu")
