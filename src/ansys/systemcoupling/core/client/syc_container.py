import os
from pathlib import Path
import subprocess

_MPI_VERSION_VAR = "FLUENT_INTEL_MPI_VERSION"
_MPI_VERSION = "2021"


def start_container(
    mounted_from: str, mounted_to: str, network: str, port: int
) -> None:
    """Start a System Coupling container.

    Parameters
    ----------
    port : int
        gPRC server local port, mapped to the same port in container.
    """
    args = ["-m", "cosimgui", f"--grpcport=0.0.0.0:{port}"]
    image_tag = os.getenv("SYC_IMAGE_TAG", "v23.1.0")

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
        f"ghcr.io/pyansys/pysystem-coupling:{image_tag}",
    ] + args

    if network:
        idx = run_args.index("-p")
        run_args.insert(idx, network)
        run_args.insert(idx, "--network")

    subprocess.run(run_args)
    return port


def create_network(name):
    subprocess.run(["docker", "network", "create", name])
