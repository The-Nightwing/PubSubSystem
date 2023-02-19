import grpc
import a1_pb2
import a1_pb2_grpc
import uuid
import time
import datetime




client_name = str(uuid.uuid4())
channel = grpc.insecure_channel('localhost:50051')
stub = a1_pb2_grpc.RegistryServerStub(channel)
server_list = dict()
connected_server_list = dict()

def eventLoop():
    global client_name
    global channel
    global stub
    global server_list
    global connected_server_list
    while True:
        print('1. Join Server')
        print('2. Get Articles')
        print('3. Leave Server')
        print('4. Get Server List')
        print('5. Publish Article')
        print('6. Print Connected Servers')
        print('7. Exit')

        choice = input('Enter your choice: ')
        
        if choice == '1':
            name = input('Choose Server to Join: ')
            if name in server_list.keys():
                response = server_list[name].JoinServer(a1_pb2.Client(name = client_name, address=''))
                if response.status == a1_pb2.Response.SUCCESS:
                    connected_server_list[name] = server_list[name]
                    print('SUCCESS')
                else:
                    print('FAILURE')

        elif choice == '2':
            name=input('Choose Server to Get Articles From: ')
            print('Enter Filter: ')
            type = input('Type(default SPORTS): ')
            if type=='SPORTS':
                type = a1_pb2.Article.SPORTS
            elif type=='FASHION':
                type = a1_pb2.Article.FASHION
            elif type=='POLITICS':
                type = a1_pb2.Article.POLITICS
            elif type=='':
                type = a1_pb2.Article.SPORTS
            else:
                print('wrong type')
                continue
            author = input('Author: ')
            ti = input('Time (DD/MM/YYYY): ')
            if author=='':
                author = None
            if ti=='':
                ti = None
            else:
                ti = int(time.mktime(datetime.datetime.strptime(ti, "%d/%m/%Y").timetuple()))
            if name in connected_server_list.keys():
                response = connected_server_list[name].GetArticles(a1_pb2.ArticleRequest(name = client_name, article = a1_pb2.Article(type=type,author=author,time=ti, content='cccccc')))
                for r in response:
                    print(r)

        elif choice == '3':
            name=input('Choose Server to Leave: ')
            if name in connected_server_list.keys():
                response = connected_server_list[name].LeaveServer(a1_pb2.Client(name = client_name, address=''))
                if response.status == a1_pb2.Response.SUCCESS:
                    connected_server_list.pop(name)
                    print('SUCCESS')
                else:
                    print('FAILURE')
        elif choice == '4':
            response = stub.GetServerList(a1_pb2.Request())
            for r in response:
                server_list[r.name] = a1_pb2_grpc.ArticleServerStub(grpc.insecure_channel('localhost:'+r.address))
                print(r.name +' localhost:'+ r.address)
            
        elif choice == '5':
            name=input('Choose Server to publish On: ')
            type=input('Enter Article Type(SPORTS, FASHION, POLITICS): ')
            if type=='SPORTS':
                type = a1_pb2.Article.SPORTS
            elif type=='FASHION':
                type = a1_pb2.Article.FASHION
            elif type=='POLITICS':
                type = a1_pb2.Article.POLITICS
            else:
                print('wrong type')
                continue
            author=input('Enter Author: ')
            content=input('Enter Content: ')
            if name in connected_server_list.keys():
                response = connected_server_list[name].PublishArticle(a1_pb2.ArticleRequest(name=client_name,article=a1_pb2.Article(type=type,author=author,content=content,time=0)))
                if response.status == a1_pb2.Response.SUCCESS:
                    print('SUCCESS')
                else:
                    print('FAILURE')
            else:
                print('Not connected to this server')
    
        elif choice == '6':
            for f in connected_server_list:
                print(f)
        elif choice == '7':
            break
        else:
            print('Invalid choice')
        
        
if __name__=='__main__':
    eventLoop()