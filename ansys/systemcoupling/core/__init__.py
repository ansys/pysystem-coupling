from ansys.systemcoupling.core._version import __version__
from ansys.systemcoupling.core.client.rpc_client import SycRpc


def launch_syc(working_dir='.'):
    syc = SycRpc()
    syc.start_and_connect(working_dir)
    return syc
    
    
def connect_to_syc(host, port):
    syc = SycRpc()
    syc.connect(host, port)
    return syc
