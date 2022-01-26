from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.syc_api import SycApi
from ansys.systemcoupling.core.client.rpc_client import SycRpc

def launch_syc(working_dir='.'):
    rpc = SycRpc()
    rpc.start_and_connect(working_dir)
    syc = SycApi(rpc)
    return syc


def connect_to_syc(host, port):
    rpc = SycRpc()
    rpc.connect(host, port)
    syc = SycApi(rpc)
    return syc
