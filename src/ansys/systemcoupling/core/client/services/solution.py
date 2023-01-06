import ansys.api.systemcoupling.v0.error_pb2 as syc_error_pb2
import ansys.api.systemcoupling.v0.solution_pb2 as solution_pb2
import ansys.api.systemcoupling.v0.solution_pb2_grpc as solution_pb2_grpc
import grpc
from grpc_status.rpc_status import from_call


class SolutionService:
    def __init__(self, channel):
        self.__stub = solution_pb2_grpc.SolutionStub(channel)

    def solve(self):
        request = solution_pb2.SolveRequest()
        try:
            self.__stub.Solve(request)
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

    def interrupt(self, reason):
        request = solution_pb2.InterruptRequest(reason=reason)
        self.__stub.Interrupt(request)

    def abort(self, reason):
        request = solution_pb2.AbortRequest(reason=reason)
        self.__stub.Abort(request)
