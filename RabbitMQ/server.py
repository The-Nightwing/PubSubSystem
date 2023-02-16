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
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        self.registerToRegistery()
        self.channel.start_consuming()
    
    def registerToRegistery(self):
        message = { 
            'request': 'register', 
            'port': self.port
        }
        self.channel.basic_publish(exchange='direct_logs', routing_key='unique_id', body=json.dumps({'id': self.port}))
        print(" [x] Sent %r" % message)

    def toRegistercallback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)

    def toGetListcallback(self,ch, method, properties, body):
        body = json.loads(body)
        print('f')
        for x in body['list']:
            print(x)

    def toRegister(self):
        self.channel.queue_declare(queue='unique_id')
        self.channel.queue_bind(exchange='direct_logs', queue='unique_id', routing_key='unique_id')

        self.channel.queue_declare(queue='register_incoming'+"_"+str(self.port))
        self.channel.queue_bind(exchange='direct_logs', queue='register_incoming'+"_"+str(self.port), routing_key='register_incoming'+"_"+str(self.port))

        self.channel.queue_declare(queue='register_outgoing'+"_"+str(self.port))
        self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing'+"_"+str(self.port), routing_key='register_outgoing'+"_"+str(self.port))
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(self.port), body=json.dumps(self.message))

        self.channel.basic_consume(
            queue='register_outgoing'+"_"+str(self.port), on_message_callback=self.toRegistercallback, auto_ack=True
        )

    def toGetServerList(self):
        self.channel.queue_declare(queue='getServerList_incoming')
        self.channel.queue_bind(exchange='direct_logs', queue='getServerList_incoming', routing_key='getServerList_incoming')

        self.channel.queue_declare(queue='getServerList_outgoing')
        self.channel.queue_bind(exchange='direct_logs', queue='getServerList_outgoing', routing_key='getServerList_outgoing')
        self.channel.basic_publish(exchange='direct_logs', routing_key='getServerList_incoming', body=json.dumps({'request': 'getServerList', 'port': self.port}))

        self.channel.basic_consume(
            queue='getServerList_outgoing', on_message_callback=self.toGetListcallback, auto_ack=True
        )
    def toGetArticles(self):
        pass

    def connectClient(self):

        pass

    def endClient(self):
        self.connection.close()
        

if __name__ == '__main__':
    while True:
        Server(sys.argv[1])