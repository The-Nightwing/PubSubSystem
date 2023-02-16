import zmq
import sys



class Server:
    def __init__(self, port, address, name):
        self.context = zmq.Context()
        self.address = address
        self.port  = port
        self.name = name
        self.max_clients = 10
        self.clientList = []
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
                    self.clientList.append(message['uuid'])
                    self.res_socket.send_json({'message': 'SUCCESS'})
                else:
                    self.res_socket.send_json({'message': 'FAIL'})

            # Unregister Client From Server
            if message['request']=='unregister':
                print(" [x] REMOVE REQUEST FROM %r" % message['uuid'])
                if message['uuid'] in self.clientList:
                    self.clientList.remove(message['uuid'])
                    self.res_socket.send_json({'message': 'SUCCESS'})
                else:
                    self.res_socket.send_json({'message': 'FAIL'})

    


    def register(self):
        self.req_socket = self.context.socket(zmq.REQ)
        self.req_socket.connect(self.address)
        self.req_socket.send_json({'port': self.port, 'name': self.name, 'request':'register'})

        message = self.req_socket.recv_json()
        print(message['message'])


if __name__ == "__main__":
    server = Server(int(sys.argv[2]), "tcp://localhost:5555", sys.argv[1])
    server.send(b"Hello")