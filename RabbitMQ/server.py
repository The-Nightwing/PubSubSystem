from datetime import date
import pika
import sys
import json


class Server:
    def __init__(self, name, port):
        self.clientList = []
        self.max_clients = 10
        self.port = port
        self.name = name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.articles = []
        self.assignedPort=0
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
        self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing'+"_"+str(self.assignedPort), routing_key='register_outgoing'+"_"+str(self.assignedPort))
        
        self.channel.basic_consume(queue='register_incoming'+"_"+str(self.assignedPort), on_message_callback=self.incomingCallback, auto_ack=True)
        # self.channel.basic_consume(queue='register_outgoing'+"_"+str(self.assignedPort), on_message_callback=self.toRegistercallback, auto_ack=True)

    def registerToRegistery(self):
        self.message = {
            'request': 'register',
            'name': self.name,
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
        # print(body)
        if body['port']==self.port:
            self.assignedPort=body['message']
            print(" [x] Received %r" % body['code'])
            # self.channel.stop_consuming()
            self.init_consumer()
            self.channel.stop_consuming()
            # self.channel.start_consuming()

    def incomingCallback(self, ch, method, properties, body):
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
            print(" [x] LEAVE REQUEST FROM %r" % body['uuid'])
            if self.clientList.count(body['uuid']) > 0:
                # print(self.clientList)
                self.clientList.remove(body['uuid'])
                # print(self.clientList)
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
        if body['request']=='publishArticle':
            print(" [x] ARTICLES PUBLISH FROM %r" % body['uuid'])
            if self.clientList.count(body['uuid']) > 0:
                body['article']['time'] =str(date.today())

                self.articles.append(body['article'])
                self.message = {
                    'request': 'publishArticle',
                    'port': self.port,
                    'status': 'SUCCESS',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
            else:
                self.message = {
                    'request': 'publishArticle',
                    'port': self.port,
                    'status': 'FAIL',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
        if body['request']=='getArticles':
            print(" [x] ARTICLES REQUEST FROM %r" % body['uuid'] )
            if self.clientList.count(body['uuid']) > 0:
                response = {}
                # print(body)
                
                if body['article']['type'] != '' and body['article']['author'] != '' and body['article']['time'] != '':
                        response = {'list': [x for x in self.articles if x['type'] == body['article']['type'] and x['author'] == body['article']['author'] and x['time'] > body['article']['time']]}

                elif body['article']['type']=='' and body['article']['author'] != '' and body['article']['time'] != '':
                        #filter on basis of author and time
                        response = {'list': [x for x in self.articles if x['author'] == body['article']['author'] and x['time'] > body['article']['time']]}

                elif body['article']['type'] != '' and body['article']['author'] == '' and body['article']['time'] != '':
                        #filter on basis of author
                        response = {'list': [x for x in self.articles if x['type'] == body['article']['type'] and x['time'] > body['article']['time']]}

                elif body['article']['type'] == '' and body['article']['author'] == '' and body['article']['time'] == '':
                        #default filter to check output
                        response = {'list': [x for x in self.articles]}
                else:
                        response = {'list': []}
                self.message = {
                    'request': 'getArticles',
                    'port': self.port,
                    'status': 'SUCCESS',
                    'index': self.assignedPort,
                    'type': body['article']['type'],
                    'author': body['article']['author'],
                    'time': body['article']['time'],
                    'articles': response
                }
                # print(self.message)
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))
            else:
                self.message = {
                    'request': 'getArticles',
                    'port': self.port,
                    'status': 'FAIL',
                    'index': self.assignedPort
                }
                self.channel.basic_publish(exchange='direct_logs', routing_key='register_outgoing'+"_"+str(self.assignedPort), body=json.dumps(self.message))

if __name__ == '__main__':
    server = Server(name=sys.argv[1], port=sys.argv[2])
    server.start()
    if not server.error:   
        server.init_consumer()
        server.channel.start_consuming()
    else:
        print("ERROR WHILE CONNECTING TO REGISTER SERVER")
