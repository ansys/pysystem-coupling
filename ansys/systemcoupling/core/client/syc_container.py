import subprocess


def start_container(port: int) -> None:
    """Start a System Coupling container.

    Parameters
    ----------
    port : int
        gPRC server local port, mapped to same port in container.
    """
    args = ["-m", "cosimgui", f"--grpcport=0.0.0.0:{port}"]

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
            "ghcr.io/pyansys/pysystem-coupling",
        ]
        + args
    )
    return port