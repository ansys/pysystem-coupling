import socket
import subprocess


def _find_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def start_container() -> int:
    """Start a System Coupling container.

    Returns
    -------
    int
        gPRC server port exposed from the container.
    """
    port = _find_port()

    args = []  # TODO !!!
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
