import grpc
from grpc_status.rpc_status import from_call
import ansys.api.systemcoupling.v0.sycapi_pb2 as sycapi_pb2
import ansys.api.systemcoupling.v0.sycapi_pb2_grpc as sycapi_pb2_grpc

class CommandQueryService:
    def __init__(self, channel):
        self.__stub = sycapi_pb2_grpc.SycApiStub(channel)

    def execute_command(self, request):
        try:
            response, call = self.__stub.InvokeCommand.with_call(request)
            return response, call.trailing_metadata()
        except grpc.RpcError as rpc_error:
            status = from_call(rpc_error)
            msg = f"Command execution failed: {status.message} (code={status.code})"
            for detail in status.details:
                if detail.Is(sycapi_pb2.ErrorDetails.DESCRIPTOR):
                    info = sycapi_pb2.ErrorDetails()
                    detail.Unpack(info)
                    msg += (f"\n\nServer exception details:\n"
                            f"{info.exception_classname}\n{info.stack_trace}")
            raise RuntimeError(msg) from None

    def ping(self):
        request = sycapi_pb2.PingRequest()
        response = self.__stub.Ping(request)
        return True

    def quit(self):
        request = sycapi_pb2.QuitRequest()
        response = self.__stub.Quit(request)
        return True

