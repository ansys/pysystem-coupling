from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.analysis import SycAnalysis
from ansys.systemcoupling.core.client.grpc_client import SycGrpc
from ansys.systemcoupling.core.util.logging import LOG


def launch(host: str = None, port: int = None, working_dir: str = None):
    rpc = SycGrpc()
    rpc.start_and_connect(host, port, working_dir)
    syc = SycAnalysis(rpc)
    return syc


def launch_container():
    rpc = SycGrpc()
    rpc.start_container_and_connect()
    syc = SycAnalysis(rpc)
    return syc


def connect(host: str, port: int):
    rpc = SycGrpc()
    rpc.connect(host, port)
    syc = SycAnalysis(rpc)
    return syc
