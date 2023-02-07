import os
from typing import List

import appdirs

from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.session import Session
from ansys.systemcoupling.core.util.logging import LOG


def launch(
    *,
    port: int = None,
    working_dir: str = None,
    nprocs: int = None,
    sycnprocs: int = None,
    extra_args: List[str] = [],
) -> Session:
    """Start a local instance of System Coupling and connects to it.

    Parameters
    ----------
    port : int, optional
        Port on which to connect to System Coupling. If not specified,
        an available port will be sought and used.

    working_dir : str, optional
        The working directory of the System Coupling process. Defaults to
        the current directory of the client process.

    nprocs : int, optional
        The number of processes for coupling participants. If not provided,
        the System Coupling server will use its own default.

    sycnprocs : int, optional
        The number of processes for the coupling engine. If not provided,
        the System Coupling server will use its own default.

    extra_args : List[str]
        List of any additional arguments to be specified when the server
        process is launched. Defaults to empty list.

        If provided, this is concatenated as-is to the list of
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
    rpc.start_and_connect(
        port=port,
        working_dir=working_dir,
        nprocs=nprocs,
        sycnprocs=sycnprocs,
        extra_args=extra_args,
    )
    syc = Session(rpc)
    return syc


def launch_container(
    mounted_from: str = "./", mounted_to: str = "/working", network: str = None
) -> Session:
    """Start a System Coupling container instance and connect to it.

    `Note`: the container is currently only intended to be used for
    testing and development purposes.

    Returns
    -------
    ansys.systemcoupling.core.session.Session
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.start_container_and_connect(mounted_from, mounted_to, network)
    syc = Session(rpc)
    return syc


def connect(host: str, port: int) -> Session:  # pragma: no cover
    """Connect to instance of System Coupling already running in server mode.

    Parameters
    ----------
    host : str
        IP address of the system running the instance of System Coupling.

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
try:
    USER_DATA_PATH = appdirs.user_data_dir("ansys_systemcoupling_core")
    if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
    if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
        os.makedirs(EXAMPLES_PATH)

except:  # pragma: no cover
    pass

BUILDING_GALLERY = False
