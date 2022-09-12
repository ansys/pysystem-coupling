import ansys.api.systemcoupling.v0.process_pb2 as sycprocess_pb2
import ansys.api.systemcoupling.v0.process_pb2_grpc as sycprocess_pb2_grpc


class SycProcessService:
    def __init__(self, channel):
        self.__stub = sycprocess_pb2_grpc.ProcessStub(channel)

    def ping(self):
        request = sycprocess_pb2.PingRequest()
        response = self.__stub.Ping(request)
        return True

    def quit(self):
        request = sycprocess_pb2.QuitRequest()
        response = self.__stub.Quit(request)
        return True
