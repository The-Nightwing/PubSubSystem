import pika
import json



class RegistryServer:
        def __init__(self, port):
            self.port = port
            self.serverList = []
            self.max_servers = 2
            self.current_count_servers = 0
            self.register_incoming = ""
            self.register_outgoing =  ""
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

            self.channel.queue_declare(queue='unique_id')
            self.channel.queue_bind(exchange='direct_logs', queue='unique_id', routing_key='unique_id')
            self.channel.basic_consume(queue='unique_id', on_message_callback=self.createUniqueQueue, auto_ack=True)

            # self.channel.queue_declare(queue=self.register_incoming)
            # self.channel.queue_bind(exchange='direct_logs', queue=self.register_incoming, routing_key=self.register_incoming)

            # self.channel.queue_declare(queue=self.register_outgoing)
            # self.channel.queue_bind(exchange='direct_logs', queue=self.register_outgoing, routing_key=self.register_outgoing)

            # self.channel.basic_consume(queue=self.register_incoming, on_message_callback=self.registerServer, auto_ack=True)

            self.channel.queue_declare(queue='getServerList_incoming')
            self.channel.queue_declare(queue='getServerList_outgoing')

            self.channel.queue_bind(exchange='direct_logs', queue='getServerList_incoming', routing_key='getServerList_incoming')
            self.channel.queue_bind(exchange='direct_logs', queue='getServerList_outgoing', routing_key='getServerList_outgoing')

            self.channel.basic_consume(queue='getServerList_incoming', on_message_callback=self.getServerList, auto_ack=True)
            
            self.channel.start_consuming()            

        def createUniqueQueue(self, ch, method, properties, body):
            body = json.loads(body)
            id_ = body['id']

            self.register_incoming = "register_incoming_"+str(id_)
            self.register_outgoing = "register_outgoing_"+str(id_)

            self.channel.queue_declare(queue=self.register_incoming)
            self.channel.queue_bind(exchange='direct_logs', queue=self.register_incoming, routing_key=self.register_incoming)

            self.channel.queue_declare(queue=self.register_outgoing)
            self.channel.queue_bind(exchange='direct_logs', queue=self.register_outgoing, routing_key=self.register_outgoing)

            self.channel.basic_consume(queue=self.register_incoming, on_message_callback=self.registerServer, auto_ack=True)


        def registerServer(self, ch, method, properties, body):
            print("ss")
            #decode
            body  = json.loads(body)
            print(body)
            if body['request'] == "register":
                if self.current_count_servers < self.max_servers:
                    self.current_count_servers += 1
                    self.serverList.append(body['port'])
                    print("JOIN REQUEST FROM LOCALHOST:"+str(body['port']))
                    self.channel.basic_publish(exchange='direct_logs', routing_key=self.register_outgoing, body="SUCCESS")
                else:
                    self.channel.basic_publish(exchange='direct_logs', routing_key=self.register_outgoing, body="FAIL")
        
        def getServerList(self, ch, method, properties, body):
            body = json.loads(body)
            if body['request'] == "getServerList":
                print("SERVER LIST REQUESTED FROM LOCALHOST:"+str(body['port']))
                self.channel.basic_publish(exchange='direct_logs', routing_key='getServerList_outgoing', body=json.dumps({'list': self.serverList}))
        
            

if __name__ == "__main__":
    server = RegistryServer(8800)
    print("Registry Server Started")