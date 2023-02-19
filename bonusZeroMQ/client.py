import zmq
import uuid


class Client:
    def __init__(self):
        self.id = uuid.uuid4()
        self.connectedServers = []
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.menu()

    def getServerList(self):
        self.socket.send_json({'request': 'getServerList'})
        message = self.socket.recv_json()
        print("Server List: ")
        print()
        for x in message['list']:
            print("Server Name: " + x[0] + " Port: " + str(x[1]))
        print()
    
    def joinServer(self, port):
        if port in self.connectedServers:
            print('Already connected to this server')
            return
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(port))
        socket.send_json({'request': 'register', 'uuid': str(self.id)})
        message = socket.recv_json()
        if message['message'] == 'SUCCESS':
            self.connectedServers.append(port)
            print('Successfully Joined Server')
        else:
            print('FAIL')

    def getArticles(self, port, type, author, time):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(port))
        socket.send_json(
            {
                'request': 'getArticleList', 
                'uuid': str(self.id), 
                'article': 
                    {
                        'type': type, 
                        'author': author, 
                        'time': time, 
                    }
            }
        )
        message = socket.recv_json()

        if 'message' in message.keys() and message['message'] == 'FAIL':
            print('FAIL')
            return
        
        for x in message['list']:
            print(x)

    def leaveServer(self, port):
        if port in self.connectedServers:
            socket = self.context.socket(zmq.REQ)
            socket.connect("tcp://localhost:"+str(port))
            socket.send_json({'request': 'unregister', 'uuid': str(self.id)})
            message = socket.recv_json()
            if message['message'] == 'SUCCESS':
                self.connectedServers.remove(port)
            print(message['message'])
        else:
            print('FAIL')
        
    def publishArticle(self, port, type, author, content):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(port))
        socket.send_json(
            {
                'request': 'publishArticle', 
                'uuid': str(self.id), 
                'article': 
                    {
                        'type': type, 
                        'author': author, 
                        'content': content, 
                    }
            }
        )

        message = socket.recv_json()
        print(message['message'])

    def printConnectedServers(self):
        for server in self.connectedServers:
            print(server)

    def menu(self):
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
                port=input('Choose Server to Join: ')
                self.joinServer(port)

            elif choice == '2':
                port=input('Choose Server to Get Articles From: ')
                print('Enter Filter: ')
                type = input('Type: ')
                author = input('Author: ')
                time = input('Time (YYYY-MM-DD): ')
                if port in self.connectedServers:
                    self.getArticles(port, type, author, time)
                else:
                    print('Not connected to this server')

            elif choice == '3':
                port=input('Choose Server to Leave: ')
                if port in self.connectedServers:
                    self.leaveServer(port)
                else:
                    print('Not connected to this server')
            elif choice == '4':
                self.getServerList()
                # self.channel.start_consuming()
            elif choice == '5':
                port=input('Choose Server to publish On: ')
                type=input('Enter Article Type: ')
                author=input('Enter Author: ')
                content=input('Enter Content: ')
                if port in self.connectedServers:
                    self.publishArticle(port, type, author, content)
                else:
                    print('Not connected to this server')
        
            elif choice == '6':
                self.printConnectedServers()
            elif choice == '7':
                break
            else:
                print('Invalid choice')


if __name__ == '__main__':
    Client()