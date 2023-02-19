import grpc
import a1_pb2
import a1_pb2_grpc
from concurrent import futures


class RegistryServer(a1_pb2_grpc.RegistryServerServicer):
    def __init__(self) -> None:
        super().__init__()
        self.serverlist = []
        self.MAX_SERVERS = 25
    
    def Register(self, request, context):
        print('JOIN REQUEST FROM localhost:',request.address)
        if len(self.serverlist) >= self.MAX_SERVERS:
            return a1_pb2.Response(status=a1_pb2.Response.FAILURE)
        self.serverlist.append(request)
        return a1_pb2.Response(status=a1_pb2.Response.SUCCESS)
    
    def GetServerList(self, request, context):
        print('SERVER LIST REQUEST FROM ',context.peer())
        for server in self.serverlist:
            yield server
    
    
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    a1_pb2_grpc.add_RegistryServerServicer_to_server(RegistryServer(),server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()
    
    
if __name__=='__main__':
    serve()