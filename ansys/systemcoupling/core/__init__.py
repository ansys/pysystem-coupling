from ansys.systemcoupling.core._version import __version__
try:
    from ansys.systemcoupling.core.analysis import SycAnalysis
    from ansys.systemcoupling.core.client.grpc_client import SycGrpc
except:
    print("IMPORTS FAILED")

def launch(host="127.0.0.1", port=50051, working_dir="."):
    rpc = SycGrpc()
    rpc.start_and_connect(host, port, working_dir)
    syc = SycAnalysis(rpc)
    return syc


def connect(host, port):
    rpc = SycGrpc()
    rpc.connect(host, port)
    syc = SycAnalysis(rpc)
    return syc
