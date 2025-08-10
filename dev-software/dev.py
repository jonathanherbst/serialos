import podman
from podman.domain.images import Image as PodmanImage
from podman.errors import exceptions

import argparse
import logging
import pathlib
import re
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

def run_qemu():
    yocto_shell("qemu", "bitbake serialos-bare-image")
    yocto_shell("qemu", " \
        qemu-img create -f qcow2 /home/yocto/data-img.qcow2 1G && \
        runqemu serialos-bare-image slirp nographic qemuparams=\"-drive file=/home/yocto/data-img.qcow2,format=qcow2,if=virtio\" \
    ")

class PodmanRun:
    def __init__(self, image: PodmanImage, user: str, command: str):
        self.image = image
        self.user = user
        self.command = command
        self.volumes: list[tuple[str, str]] = []
        self.ports: list[tuple[int, int]] = []
        self.environment: list[tuple[str, str]] = []

    def build_command(self):
        vol_args = " ".join(['-v "%s:%s"' % (host, guest) for (host, guest) in self.volumes])
        port_args = " ".join(['-p "%d:%d"' % (host, guest) for (host, guest) in self.ports])
        env_args = " ".join(['-e "%s=%s"' % (name, value) for (name, value) in self.environment])
        return '''podman run --rm -it \\
            --entrypoint="/bin/bash" \\
            --user="{user}" \\
            --userns=keep-id \\
            {volumes} \\
            {ports} \\
            {environment} \\
            {image_id} -c "{command}" \\
        '''.format(user=self.user, volumes=vol_args, ports=port_args, environment=env_args, image_id=self.image.id, command=self.command)

    def run_shell_bound(self):
        shell_cmd = self.build_command()
        return subprocess.run(shell_cmd, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def popen(self, **kwargs):
        shell_cmd = self.build_command()
        return subprocess.Popen(shell_cmd, shell=True, **kwargs)

class NFSServer:
    class Monitor:
        def __init__(self, process: subprocess.Popen):
            self.process = process
            self.ready = False

        def wait_ready(self):
            if not self.ready and self.process.stdout is not None:
                for line in self.process.stdout:
                    if "INFO nfs3_server::tcp: Listening on" in line:
                        self.ready = True
                        return

        def kill(self):
            self.process.kill()
            self.process.communicate()
            return self.process.returncode

    def __init__(self, archive_path: pathlib.Path):
        image = get_nfs_image()
        archive_path = archive_path.resolve()
        archive_guest = "/archive%s" % ''.join(archive_path.suffixes)
        command = '''set -x && \\
            sudo tar -xf %s -C /mnt && \\
            sudo /usr/local/cargo/bin/cargo-nfs3-server --path /mnt/ \\
        ''' % archive_guest

        self.runner = PodmanRun(image, "nfs", command)
        self.runner.volumes.append((str(archive_path), archive_guest))
        self.runner.ports.append((11111, 11111))
    
    @classmethod
    def run_shell_bound(cls, archive_path: pathlib.Path):
        server = cls(archive_path)
        return server.runner.run_shell_bound()

    @classmethod
    def run_monitor(cls, archive_path: pathlib.Path):
        server = cls(archive_path)
        return cls.Monitor(server.runner.popen(stdout=subprocess.PIPE))

def parse_args():
    parser = argparse.ArgumentParser(
            prog="dev.py",
            description="Dev tools for serialos",
    )

    commands = parser.add_subparsers(dest="command", required=True)
    shell_command = commands.add_parser("shell", help="Get a shell with the yocto environment setup")
    nfs_command = commands.add_parser("nfs", help="Create an nfs share with from a rootfs tar file")
    qemu_command = commands.add_parser("qemu", help="Run qemu with a normal image")

    _ = shell_command.add_argument("machine", help="Machine to setup the shell for", choices=yocto_machine.keys())

    _ = nfs_command.add_argument("archive", help="Path to an archive to share", type=pathlib.Path)

    return parser.parse_args()

def shell_cmd(_args):
    yocto_shell("qemu", "/bin/bash")

def nfs_cmd(args):
    NFSServer.run_shell_bound(args.archive)

def qemu_cmd(args):
    run_qemu()

if __name__ == "__main__":
    logging.basicConfig(stream = sys.stdout, level = logging.INFO)

    commands = {
        "shell": shell_cmd,
        "nfs": nfs_cmd,
        "qemu": qemu_cmd,
    }

    args = parse_args()
    commands[args.command](args)
