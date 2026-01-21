# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from pathlib import Path
import subprocess  # nosec B404

from ansys.systemcoupling.core.syc_version import SYC_VERSION_DOT, normalize_version
from ansys.systemcoupling.core.util.logging import LOG

_MPI_VERSION_VAR = "FLUENT_INTEL_MPI_VERSION"
_MPI_VERSION = "2021"


def _major_minor_sp_from_version(version: str) -> tuple[int, int, str]:
    """Extract major, minor, and service pack suffix from version string."""
    version, sep, service_pack = version.partition("-sp")
    if version.startswith("v"):
        version = version[1:]
    if version.endswith(".0"):
        version = version[:-2]
    major, minor = normalize_version(version)
    return major, minor, f"{sep}{service_pack}"


def _image_tag(version: str) -> str:
    if version == "latest":
        return version
    major, minor, sp_suffix = _major_minor_sp_from_version(version)

    # We are tolerant of whether the suffix is actually included, but
    # force the use of latest service pack images where applicable.

    if not sp_suffix:
        if (major, minor) == (24, 2):
            sp_suffix = "-sp05"
        elif (major, minor) == (25, 1):
            sp_suffix = "-sp04"
        elif (major, minor) == (25, 2):
            sp_suffix = "-sp03"

    return f"v{major}.{minor}.0{sp_suffix}"


def _default_image_tag() -> str:
    return _image_tag(SYC_VERSION_DOT)


def start_container(
    mounted_from: str, mounted_to: str, network: str, port: int, version: str
) -> None:
    """Start a System Coupling container.

    Parameters
    ----------
    port : int
        gPRC server local port, mapped to the same port in container.
    """

    if version:
        image_tag = _image_tag(version)
    else:
        image_tag = os.getenv("SYC_IMAGE_TAG", _default_image_tag())

    # Now use the image tag as definitive source of version info to
    # decide on transport args.
    if not (use_new_transport_args := image_tag == "latest"):
        major, minor, sp_suffix = _major_minor_sp_from_version(image_tag)
        use_new_transport_args = sp_suffix or (major, minor) > (25, 2)

    if use_new_transport_args:
        args = [
            "-m",
            "cosimgui",
            "--grpc",
            "--host=0.0.0.0",
            f"--port={port}",
            "--transport-mode=insecure",
            "--allow-remote",
            "--ptrace",
        ]
    else:
        args = ["-m", "cosimgui", f"--grpcport=0.0.0.0:{port}", "--ptrace"]

    LOG.debug("Starting System Coupling docker container...")

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

    # Additional environment
    container_user = os.getenv("SYC_CONTAINER_USER")
    if container_user:
        idx = run_args.index("-p")
        run_args.insert(idx, container_user)
        run_args.insert(idx, "--user")
        # Licensing can't log to default location if user is not the default 'root'
        run_args.insert(idx, f"ANSYSLC_APPLOGDIR={mounted_to}")
        run_args.insert(idx, "-e")

    license_server = os.getenv("ANSYSLMD_LICENSE_FILE")
    if license_server:
        # This is especially necessary in the SYC_CONTAINER_USER case
        # because licensing can't log to default location if user is
        # not the default 'root'. However it might also be useful
        # in other cases to help diagnose license problems as it makes
        # the log files accessible on host.
        idx = run_args.index("-e")
        run_args.insert(idx, f"ANSYSLC_APPLOGDIR={mounted_to}")
        run_args.insert(idx, "-e")
        # timeout settings fix some license errors we were seeing
        run_args.insert(idx, "ANSYSCL_TIMEOUT_RESPONSE=300")
        run_args.insert(idx, "-e")
        run_args.insert(idx, "ANSYSLI_TIMEOUT_FLEXLM=60")
        run_args.insert(idx, "-e")

        run_args.insert(idx, f"ANSYSLMD_LICENSE_FILE={license_server}")
        run_args.insert(idx, "-e")

    if network:
        idx = run_args.index("-p")
        run_args.insert(idx, network)
        run_args.insert(idx, "--network")

    # Exclude Bandit check. No untrusted input to arguments.
    subprocess.run(run_args)  # nosec B603


def create_network(name):
    # Exclude Bandit checks:
    # No untrusted input to arguments.
    # Start process with partial path. (Python 'docker' package would be better
    # but doc runs become very unreliable when we try to use it.)
    subprocess.run(["docker", "network", "create", name])  # nosec B603, B607
