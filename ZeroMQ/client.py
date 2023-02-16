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
        print(message)
        return message['message']
    
    def joinServer(self, port):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(port))
        socket.send_json({'request': 'register', 'uuid': str(self.id)})

    def getArticles(self):
        pass

    def leaveServer(self, port):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(port))
        socket.send_json({'request': 'unregister', 'uuid': str(self.id)})
        
    def publishArticle(self):
        pass

    def printConnectedArticles(self):
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
                self.getArticles()
            elif choice == '3':
                port=input('Choose Server to Leave: ')
                self.leaveServer(port)
            elif choice == '4':
                self.getServerList()
                # self.channel.start_consuming()
            elif choice == '5':
                self.publishArticle()
            elif choice == '6':
                self.printConnectedServers()
            elif choice == '7':
                break
            else:
                print('Invalid choice')


if __name__ == '__main__':
    Client()