import os
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager
import zipfile


def get_requires_dist(wheel):
    with zipfile.ZipFile(wheel) as file:
        metadata_filename = [
            i.filename for i in file.filelist if "dist-info/METADATA" in i.filename
        ]
        if not metadata_filename:
            raise FileNotFoundError("Couldn't find METADATA file on distribution")
        metadata = file.read(metadata_filename[0]).decode().split("\n")

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
        subprocess.check_call(
            ["pip", "install", "--no-deps", "-r", requirements_file, wheel]
        )


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
