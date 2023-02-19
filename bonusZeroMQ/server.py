import zmq
import sys

from datetime import date

class Server:
    def __init__(self, port, address, name):
        self.context = zmq.Context()
        self.address = address
        self.port  = port
        self.name = name
        self.max_clients = 10
        self.clientList = []
        self.articleList = []

        self.connectedServers = []
        self.connectedServers.append(port)
        self.res_socket = self.context.socket(zmq.REP)
        self.res_socket.bind("tcp://*:"+str(port))

        self.register()
        self.listen()

    def listen(self):
        while True:
            message = self.res_socket.recv_json()

            # Register Client To Server
            if message['request']=='register':
                if len(self.clientList)<self.max_clients:
                    print(" [x] REGISTER REQUEST FROM CLIENT %r" % message['uuid'])
                    self.clientList.append(message['uuid'])
                    self.res_socket.send_json({'message': 'SUCCESS'})
                else:
                    self.res_socket.send_json({'message': 'FAIL'})

            # Unregister Client From Server
            if message['request']=='unregister':
                if message['uuid'] in self.clientList:
                    print(" [x] REMOVE REQUEST FROM %r" % message['uuid'])
                    self.clientList.remove(message['uuid'])
                    self.res_socket.send_json({'message': 'SUCCESS'})
                else:
                    self.res_socket.send_json({'message': 'FAIL'})

            if message['request']=='publishArticle':
                if message['uuid'] in self.clientList:
                    print(" [x] PUBLISH REQUEST FROM %r" % message['uuid'])
                    message['article']['time'] = str(date.today())
                    self.articleList.append(message['article'])

                    #if any of the fields is empty, the article is not published
                    if message['article']['type'] == '' or message['article']['author'] == '' or message['article']['content'] == '' or len(message['article']['content'])>200:
                        self.res_socket.send_json({'message': 'FAIL'})
                    else:
                        self.res_socket.send_json({'message': 'SUCCESS'})
                else:
                    self.res_socket.send_json({'message': 'FAIL'})

            if message['request']=='getArticleList':
                if message['uuid'] in self.clientList:
                    print(" [x] ARTICLE LIST REQUEST FROM %r" % message['uuid'])
                    print("Request For", message['article']);
                    articles = []
                    if len(self.connectedServers)>0:
                        print('Connected Servers: ', self.connectedServers)
                        for server in self.connectedServers:
                            if server not in message['connectedServers']:
                                articles = []
                                socket = self.context.socket(zmq.REQ)
                                print(server)
                                socket.connect("tcp://localhost"+":"+str(server))
                                print(server)
                                socket.send_json({'article': message['article'], 'request': 'getArticleList', 'uuid': message['uuid'], 'connectedServers': self.connectedServers})
                                message = socket.recv_json()
                                for art in message['list']:
                                    print(art)
                                    articles.append(art)
                    
                    for art in articles:
                        self.articleList.append(art)
                    
                # if the client request server for all articles of type sports by author jack publish after 1st january 2023, then return those articles only from articleList, the json recieved has time as string, and the time in articleList is datetime object so we need to convert the time in message to datetime object before comparing
                    if message['article']['type'] == '' and message['article']['author'] == '' and message['article']['time'] == '':
                        self.res_socket.send_json({'list': self.articleList})
                    if message['article']['type'] != '' and message['article']['author'] != '' and message['article']['time'] != '':
                        self.res_socket.send_json({'list': [x for x in self.articleList if x['type'] == message['article']['type'] and x['author'] == message['article']['author'] and x['time'] > message['article']['time']]})

                    elif message['article']['type']=='' and message['article']['author'] != '' and message['article']['time'] != '':
                        #filter on basis of author and time
                        self.res_socket.send_json({'list': [x for x in self.articleList if x['author'] == message['article']['author'] and x['time'] > message['article']['time']]})

                    elif message['article']['type'] != '' and message['article']['author'] == '' and message['article']['time'] != '':
                        #filter on basis of author
                        self.res_socket.send_json({'list': [x for x in self.articleList if x['type'] == message['article']['type'] and x['time'] > message['article']['time']]})
                    elif message['article']['type']=='' and message['article']['author']=='' and message['article']['time']!='':
                        self.res_socket.send_json({'message': 'FAIL'})

                else:
                    self.res_socket.send_json({'message': 'FAIL'})


    def register(self):
        print('Do you want to connect to more servers? (y/n)')
        choice = input()
        if choice == 'y':
            print('Enter the port number of the server you want to connect to')
            port = input("enter port comma separated: ")
            port = port.split(',')
            port = [int(x) for x in port]
            for p in port:
                self.connectedServers.append(p)

        self.req_socket = self.context.socket(zmq.REQ)
        self.req_socket.connect(self.address)
        self.req_socket.send_json({'port': self.port, 'name': self.name, 'request':'register'})

        message = self.req_socket.recv_json()
        print(message['message'])


if __name__ == "__main__":
    server = Server(int(sys.argv[2]), "tcp://localhost:5555", sys.argv[1])