import os
from typing import List

import appdirs

from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.session import Session
from ansys.systemcoupling.core.util.logging import LOG

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
    rpc.start_container_and_connect(mounted_from, mounted_to, network)
    syc = Session(rpc)
    return syc


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
