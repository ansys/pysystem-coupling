import os
from pathlib import Path
import subprocess

from ansys.systemcoupling.core.syc_version import SYC_VERSION_DOT, normalize_version

_MPI_VERSION_VAR = "FLUENT_INTEL_MPI_VERSION"
_MPI_VERSION = "2021"

_DEFAULT_IMAGE_TAG = f"v{SYC_VERSION_DOT}.0"


def _image_tag(version: str) -> str:
    major, minor = normalize_version(version)
    return f"v{major}.{minor}.0"


def start_container(
    mounted_from: str, mounted_to: str, network: str, port: int, version: str
) -> None:
    """Start a System Coupling container.

    Parameters
    ----------
    port : int
        gPRC server local port, mapped to the same port in container.
    """
    args = ["-m", "cosimgui", f"--grpcport=0.0.0.0:{port}"]

    if version:
        image_tag = _image_tag(version)
    else:
        image_tag = os.getenv("SYC_IMAGE_TAG", _DEFAULT_IMAGE_TAG)

    mounted_from = str(Path(mounted_from).absolute())

    run_args = [
        "docker",
        "run",
        "-d",
        "--rm",
        "-p",
        f"{port}:{port}",
        "-v",
        f"{mounted_from}:{mounted_to}",
        "-w",
        mounted_to,
        "-e",
        f"{_MPI_VERSION_VAR}={_MPI_VERSION}",
        "-e",
        f"AWP_ROOT=/ansys_inc",
        f"ghcr.io/ansys/pysystem-coupling:{image_tag}",
    ] + args

    if network:
        idx = run_args.index("-p")
        run_args.insert(idx, network)
        run_args.insert(idx, "--network")

    subprocess.run(run_args)
    return port


def create_network(name):
    subprocess.run(["docker", "network", "create", name])
