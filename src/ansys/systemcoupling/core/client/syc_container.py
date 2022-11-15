import os
import subprocess

_MPI_VERSION_VAR = "FLUENT_INTEL_MPI_VERSION"
_MPI_VERSION = "2021"


def start_container(port: int) -> None:
    """Start a System Coupling container.

    Parameters
    ----------
    port : int
        gPRC server local port, mapped to same port in container.
    """
    args = ["-m", "cosimgui", f"--grpcport=0.0.0.0:{port}"]
    image_tag = os.getenv("SYC_IMAGE_TAG", "v23.1.0")

    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--rm",
            "-p",
            f"{port}:{port}",
            # "-v",
            # f"{mounted_from}:{mounted_to}",
            "-e",
            f"{_MPI_VERSION_VAR}={_MPI_VERSION}",
            f"ghcr.io/pyansys/pysystem-coupling:{image_tag}",
        ]
        + args
    )
    return port
