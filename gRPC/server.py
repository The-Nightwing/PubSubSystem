import grpc
import a1_pb2
import a1_pb2_grpc
import time as ti
from concurrent import futures


class ArticleServer(a1_pb2_grpc.ArticleServerServicer):
    
    def __init__(self) -> None:
        super().__init__()
        self.MAX_CLIENTS = 100
        self.client_list = dict()
        self.article_list = []
    
    def JoinServer(self, request, context):
        print('JOIN REQUEST FROM ', request.name)
        if len(self.client_list) >= self.MAX_CLIENTS:
            return a1_pb2.Response(status=a1_pb2.Response.FAILURE)
        self.client_list[request.name] = request
        return a1_pb2.Response(status=a1_pb2.Response.SUCCESS)
        
    
    def LeaveServer(self, request, context):
        print('LEAVE REQUEST FROM ', request.name)
        if request.name in self.client_list.keys():
            self.client_list.pop(request.name)
            return a1_pb2.Response(status=a1_pb2.Response.SUCCESS)
        else:
            return a1_pb2.Response(status=a1_pb2.Response.FAILURE)
    
    def GetArticles(self, request, context):
        print('ARTICLE REQUEST FROM '+request.name)
        if request.name in self.client_list.keys():
            print(request.article)
            final_articles = self.article_list.copy()
            if request.article.author != None:
                final_articles = filter(lambda art: ArticleServer.filterByAuthor(art, request.article.author), final_articles)
            if request.article.time != None:
                final_articles = filter(lambda art: ArticleServer.filterByDate(art, request.article.time), final_articles)
            if request.article.type != None:
                final_articles = filter(lambda art: ArticleServer.filterByType(art, request.article.type), final_articles)
            x = final_articles
            for i in x:
                print(i)
            yield from final_articles
            
    
    def PublishArticle(self, request, context):
        print('ARTICLE PUBLISH FROM '+request.name)
        if request.name not in self.client_list.keys():
            return a1_pb2.Response(status=a1_pb2.Response.FAILURE)
        else:
            if request.article.author != None and request.article.type != None and request.article.time != None:
                request.article.time = int(ti.time())
                self.article_list.append(request.article)
                return a1_pb2.Response(status=a1_pb2.Response.SUCCESS)
            else:
                return a1_pb2.Response(status=a1_pb2.Response.FAILURE)
    
    def filterByAuthor(article, author):
        if article.author == author:
            return True
        else:
            return False
    def filterByDate(article, time):
        if article.time >= time:
            return True
        else:
            return False
    def filterByType(article,type):
        if article.type == type:
            return True
        else:
            return False

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = a1_pb2_grpc.RegistryServerStub(channel)
        response =  stub.Register(a1_pb2.Server(name='yoboi1', address='hello'))
        response =  stub.Register(a1_pb2.Server(name='yoboi2', address='hello'))
        response =  stub.Register(a1_pb2.Server(name='yoboi3', address='hello'))
        response = stub.GetServerList(a1_pb2.Request())
        for f in response:
            print(f)


def serve():
    name = input('Enter server name: ')
    port = input('Enter port number: ')
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = a1_pb2_grpc.RegistryServerStub(channel)
        response =  stub.Register(a1_pb2.Server(name=name, address=port))
        if response.status == a1_pb2.Response.SUCCESS:
            print('SUCCESS')
        else:
            print('FAILURE')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    a1_pb2_grpc.add_ArticleServerServicer_to_server(ArticleServer(),server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()
        
        
        
if __name__=='__main__':
    serve()