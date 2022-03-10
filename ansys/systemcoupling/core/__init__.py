from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.syc_api import SycApi
from ansys.systemcoupling.core.client.grpc_client import SycGrpc

def launch_syc(host='127.0.0.1', port=50051, working_dir='.'):
    rpc = SycGrpc()
    rpc.start_and_connect(host, port, working_dir)
    syc = SycApi(rpc)
    return syc


def connect_to_syc(host, port):
    rpc = SycGrpc()
    rpc.connect(host, port)
    syc = SycApi(rpc)
    return syc
