import pika
import sys
import json


class Server:
    def __init__(self, port):
        self.clientList = []
        self.max_clients = 10
        self.port = port
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.assignedPort=20
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='direct_logs', 
            exchange_type='direct'
        )
        self.error=False

    def start(self):
        self.init_consumer()
        self.channel.queue_declare(queue='error')
        self.channel.queue_bind(exchange='direct_logs', queue='error', routing_key='error')

        self.channel.queue_declare(queue='unique_id_outgoing')
        self.channel.queue_bind(exchange='direct_logs', queue='unique_id_outgoing', routing_key='unique_id_outgoing')
        
        self.channel.basic_consume(queue='unique_id_outgoing', on_message_callback=self.toRegistercallback, auto_ack=True)
        self.channel.basic_consume(queue='error', on_message_callback=self.errorcallback, auto_ack=True)
        
        self.registerToRegistery()
        self.channel.start_consuming()
    
    def init_consumer(self):
        self.channel.queue_declare(queue='unique_id')
        self.channel.queue_bind(exchange='direct_logs', queue='unique_id', routing_key='unique_id')
        
        self.channel.queue_declare(queue='register_incoming'+"_"+str(self.assignedPort))
        self.channel.queue_bind(exchange='direct_logs', queue='register_incoming'+"_"+str(self.assignedPort), routing_key='register_incoming'+"_"+str(self.assignedPort))

        self.channel.queue_declare(queue='register_outgoing'+"_"+str(self.assignedPort))
        self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing'+"_"+str(self.port), routing_key='register_outgoing'+"_"+str(self.assignedPort))
        
        self.channel.basic_consume(queue='register_incoming'+"_"+str(self.assignedPort), on_message_callback=self.registerClientCallback, auto_ack=True)
        # self.channel.basic_consume(queue='register_outgoing'+"_"+str(self.assignedPort), on_message_callback=self.toRegistercallback, auto_ack=True)

    def registerToRegistery(self):
        self.message = {
            'request': 'register',
            'port': self.port
        }
        self.channel.basic_publish(exchange='direct_logs', routing_key='unique_id', body=json.dumps(self.message))
        print(" [x] Sent %r" % self.port)

    def errorcallback(self, ch, method, properties, body):
        body=json.loads(body)
        if body['port']==self.port:
            print(" [x] Received %r" % body['code'])
            self.error=True
            self.channel.stop_consuming()

    def toRegistercallback(self, ch, method, properties, body):
        body=json.loads(body)
        print(body)
        if body['port']==self.port:
            self.assignedPort=body['message']
            print(" [x] Received %r" % body['code'])
            # self.channel.stop_consuming()
            self.init_consumer()
            self.channel.stop_consuming()
            # self.channel.start_consuming()

    def registerClientCallback(self, ch, method, properties, body):
        body=json.loads(body)
        if body['request']=='register':
            print(" [x] JOIN REQUEST FROM %r" % body['uuid'])
            if len(self.clientList) < self.max_clients:
                self.clientList.append(body['uuid'])
                self.message = {
                    'request': 'register',
                    'port': self.port,
                    'status': 'SUCCESS',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
            else:
                self.message = {
                    'request': 'register',
                    'port': self.port,
                    'status': 'FAIL',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
        if body['request']=='remove':
            print(" [x] REMOVE REQUEST FROM %r" % body['uuid'])
            if self.clientList.count(body['uuid']) > 0:
                self.clientList.remove(body['uuid'])
                self.message = {
                    'request': 'remove',
                    'port': self.port,
                    'status': 'SUCCESS',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
            else:
                self.message = {
                    'request': 'remove',
                    'port': self.port,
                    'status': 'FAIL',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))

    def toGetArticles(self):
        pass

    def connectClient(self):
        pass

    def endClient(self):
        self.connection.close()


if __name__ == '__main__':
    server = Server(sys.argv[1])
    server.start()
    server.init_consumer()
    server.channel.start_consuming()
        # if server.error:
            # break
