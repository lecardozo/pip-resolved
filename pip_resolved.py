import os
import subprocess
from argparse import ArgumentParser
from installer.sources import WheelFile
from contextlib import contextmanager


def get_requires_dist(wheel):
    with WheelFile.open(wheel) as file:
        metadata = file.read_dist_info("METADATA").split("\n")
    pattern = "Requires-Dist: "
    for line in metadata:
        if line.startswith(pattern):
            yield line.replace(pattern, "")


@contextmanager
def write_requirements(requirements):
    requirements_file = ".reqs"
    with open(requirements_file, "w") as f:
        for req in requirements:
            f.write(f"{req}\n")

    yield requirements_file
    os.remove(requirements_file)


def install_locked_requirements(requirements, wheel):
    with write_requirements(requirements) as requirements_file:
        subprocess.call(["pip", "install", "--no-deps", "-r", requirements_file, wheel])


def install(wheel):
    requirements = get_requires_dist(wheel)
    install_locked_requirements(requirements, wheel)


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")
    install_command = subparsers.add_parser(
        "install", help="Install your wheel with pre-resolved dependencies"
    )
    install_command.add_argument("wheel", help="Wheel file to be installed")
    args = parser.parse_args()
    if args.subparser == "install":
        install(wheel=args.wheel)
