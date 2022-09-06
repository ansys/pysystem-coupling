from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.session import Analysis
from ansys.systemcoupling.core.util.logging import LOG


def launch(port: int = None, working_dir: str = None):
    """Start a local instance of System Coupling and connects to it.

    Parameters
    ----------
    port : int, optional
        Port on which to connect to System Coupling. If not specified,
        an available port will be sought and used.

    working_dir : str, optional
        The working directory of the System Coupling process. Defaults to
        the current directory of the client process.

    Returns
    -------
    ansys.systemcoupling.core.session.Analysis
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.start_and_connect(port, working_dir)
    syc = Analysis(rpc)
    return syc


def launch_container() -> Analysis:
    """Start a System Coupling container instance and connect to it.

    `Note`: the container is currently only intended to be used for
    testing and development purposes.

    Returns
    -------
    ansys.systemcoupling.core.session.Analysis
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.start_container_and_connect()
    syc = Analysis(rpc)
    return syc


def connect(host: str, port: int) -> Analysis:
    """Connect to instance of System Coupling already running in server mode.

    Parameters
    ----------
    host : str
        IP address of the system running the instance of System Coupling.

    port : int
        Port on which to connect to System Coupling.

    Returns
    -------
    ansys.systemcoupling.core.session.Analysis
        Session object, providing access to a set up and solve API controlling a
        remote System Coupling instance.
    """
    rpc = SycGrpc()
    rpc.connect(host, port)
    syc = Analysis(rpc)
    return syc
