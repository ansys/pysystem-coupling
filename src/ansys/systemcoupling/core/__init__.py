# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
from typing import List

import appdirs

from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.session import Session
from ansys.systemcoupling.core.util.logging import LOG

import ansys.platform.instancemanagement as pypim

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))


def launch(
    *,
    port: int = None,
    working_dir: str = None,
    nprocs: int = None,
    sycnprocs: int = None,
    version: str = None,
    start_output: bool = False,
    extra_args: List[str] = [],
) -> Session:
    """Start a local instance of System Coupling and connect to it.

    Parameters
    ----------
    port : int, optional
        Port on which to connect to System Coupling. The default is
        ``None``, in which case an available port is found and used.
    working_dir : str, optional
        Path for the working directory of the System Coupling process.
        The default is ``None``, in which case the current directory of
        the client process is used.
    nprocs : int, optional
        Number of processes for coupling participants. The default is
        ``None``, in which case the System Coupling server uses its own default.
    sycnprocs : int, optional
        Number of processes for the System Coupling engine. The default is
        ``None``, in which case the System Coupling server uses its own default.
    version : str, optional
        String specifying the version of System Coupling to use. For example,
        to use System Coupling from the Ansys "2024 R1" release, specify ``"241"``.
        (The forms ``"24.1"`` and ``"24_1"`` are also acceptable.)
        The version will be sought in the standard installation location. The
        default is ``None``, which is equivalent to specifying
        ``"251"`` ("2025 R1" release), unless either of the environment
        variables ``SYSC_ROOT`` or ``AWP_ROOT`` has been set. It is considered
        to be an error if either these is set *and* ``version`` is provided.
    start_output: bool, optional
        Boolean to specify if the user wants to stream system coupling output.
        The default is ``False``, in which case the output stream is kept hidden.
        If ``True``, the output information is printed to standard output.
    extra_args : List[str]
        List of any additional arguments to specify when the server
        process is launched. The default is ``[]``. If a list of additional
        arguments is provided, it is concatenated as-is to the list of
        arguments already being passed when the process is started. If
        an argument has an associated value, the argument name and its
        value should be specified as two consecutive items of the list.

    Returns
    -------
    ansys.systemcoupling.core.session.Session
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    if pypim.is_configured():
        LOG.info(
            "Starting System Coupling remotely. Any launch arguments other "
            "than 'version' and 'start_output' are ignored."
        )
        rpc.start_pim_and_connect(version, start_output)
    else:
        rpc.start_and_connect(
            port=port,
            working_dir=working_dir,
            nprocs=nprocs,
            sycnprocs=sycnprocs,
            version=version,
            start_output=start_output,
            extra_args=extra_args,
        )
    return Session(rpc)


def launch_container(
    mounted_from: str = "./",
    mounted_to: str = "/working",
    network: str = None,
    version: str = None,
) -> Session:
    """Start a System Coupling container instance and connect to it.

    .. note::
       The container is currently only intended to be used for
       testing and development purposes.

    Returns
    -------
    ansys.systemcoupling.core.session.Session
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.start_container_and_connect(mounted_from, mounted_to, network, version=version)
    return Session(rpc)


def launch_remote(
    version: str = None,
) -> Session:
    """Launch System Coupling remotely using `PyPIM <https://pypim.docs.pyansys.com>`.

    When calling this function, you must ensure that you are in an
    environment where ``PyPIM`` is configured. You can use the :func:
    `pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that ``PyPIM`` is configured.

    Parameters
    ----------
    version : str, optional
        The System Coupling product version. See :func:`launch<core.launch>`
        for details of supported version strings.

    Returns
    -------
    ansys.systemcoupling.core.session.Session
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.start_pim_and_connect(version)
    return Session(rpc)


def connect(host: str, port: int) -> Session:  # pragma: no cover
    """Connect to an instance of System Coupling already running in server mode.

    Parameters
    ----------
    host : str
        IP address of the system running the System Coupling instance.
    port : int
        Port on which to connect to System Coupling.

    Returns
    -------
    ansys.systemcoupling.core.session.Session
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.connect(host, port)
    syc = Session(rpc)
    return syc


# Set up data directory
USER_DATA_PATH = appdirs.user_data_dir(
    appname="ansys_systemcoupling_core", appauthor="Ansys"
)
if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
    os.makedirs(USER_DATA_PATH)

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
    os.makedirs(EXAMPLES_PATH)

BUILDING_GALLERY = False
