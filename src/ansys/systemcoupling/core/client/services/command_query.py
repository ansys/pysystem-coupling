import ansys.api.systemcoupling.v0.command_pb2_grpc as command_pb2_grpc
import ansys.api.systemcoupling.v0.error_pb2 as syc_error_pb2
import grpc
from grpc_status.rpc_status import from_call


class CommandQueryService:
    def __init__(self, channel):
        self.__stub = command_pb2_grpc.CommandStub(channel)

    def execute_command(self, request):
        try:
            response, call = self.__stub.InvokeCommand.with_call(request)
            return response, call.trailing_metadata()
        except grpc.RpcError as rpc_error:
            status = from_call(rpc_error)
            msg = f"Command execution failed: {status.message} (code={status.code})"
            for detail in status.details:
                if detail.Is(syc_error_pb2.ErrorDetails.DESCRIPTOR):
                    info = syc_error_pb2.ErrorDetails()
                    detail.Unpack(info)
                    msg += (
                        f"\n\nServer exception details:\n"
                        f"{info.exception_classname}\n{info.stack_trace}"
                    )
            raise RuntimeError(msg) from None
