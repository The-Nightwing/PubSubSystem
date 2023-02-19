import time
import zmq
import sys

class RegistryServer:
    def __init__(self, port):
        self.port = port
        self.max_connections = 10
        self.current_connections = 0
        self.serverList = []
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:" + str(self.port))
        self.run()

    def run(self):
        while True:
            #  Wait for next request from client
            message = self.socket.recv_json()
            if message['request']=='register':
                if self.current_connections < self.max_connections:
                    print(' [x] REGISTER REQUEST FROM %r' % message['port'])
                    self.current_connections += 1
                    self.serverList.append([message['name'], message['port']])
                    self.socket.send_json({'message': 'SUCCESS'})
                else:
                    self.socket.send_json({'message': 'FAIL'})

            elif message['request']=='getServerList':
                print(' [x] GET SERVER LIST REQUEST FROM %r' % message['uuid'])
                self.socket.send_json({'list': self.serverList})

            time.sleep(1)

            #  Send reply back to client

if __name__=='__main__':
    server = RegistryServer(5555)