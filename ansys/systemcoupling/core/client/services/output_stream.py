import ansys.api.systemcoupling.v0.output_stream_pb2 as output_stream_pb2
import ansys.api.systemcoupling.v0.output_stream_pb2_grpc as output_stream_pb2_grpc


class OutputStreamService:
    def __init__(self, channel):
        self.__stub = output_stream_pb2_grpc.OutputStreamStub(channel)
        self.__stream = None

    def begin_streaming(self):
        """Begins streaming combined standard output streams from
        System Coupling.

        Yields
        ------
        str
             A line of output.
        """
        request = output_stream_pb2.StdStreamRequest()
        self.__stream = self.__stub.BeginStdStreaming(request)

        while True:
            try:
                yield next(self.__stream)
            except:
                break

    def end_streaming(self):
        """Cancels streaming of System Coupling output streams."""
        if self.__stream and not self.__stream.cancelled():
            self.__stream.cancel()
            self.__stream = None
