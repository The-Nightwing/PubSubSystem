import pika
import json


class RegistryServer:
    def __init__(self, port):
        self.port = port
        self.serverPortList = []
        self.serverNameList = []
        self.max_servers = 10
        self.current_count_servers = 0
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='direct_logs', exchange_type='direct')
        self.init_consume()
        self.channel.start_consuming()

    def init_consume(self):
        for x in range(0,self.max_servers):
            self.channel.queue_declare(queue='register_incoming_'+str(x))
            self.channel.queue_bind(exchange='direct_logs', queue='register_incoming_'+str(x), routing_key='register_incoming_'+str(x))

            self.channel.queue_declare(queue='register_outgoing_'+str(x))
            self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing_'+str(x), routing_key='register_outgoing_'+str(x))

        self.channel.queue_declare(queue='unique_id')
        self.channel.queue_bind(exchange='direct_logs', queue='unique_id', routing_key='unique_id')

        self.channel.queue_declare(queue='unique_id_outgoing')
        self.channel.queue_bind(exchange='direct_logs', queue='unique_id_outgoing', routing_key='unique_id_outgoing')

        self.channel.queue_declare(queue='getServerList_incoming')
        self.channel.queue_bind( exchange='direct_logs', queue='getServerList_incoming', routing_key='getServerList_incoming')
        
        self.channel.queue_declare(queue='getServerList_outgoing')
        self.channel.queue_bind( exchange='direct_logs', queue='getServerList_outgoing', routing_key='getServerList_outgoing')
        
        self.channel.queue_declare(queue='error')
        self.channel.queue_bind( exchange='direct_logs', queue='error', routing_key='error')
        
        self.channel.basic_consume(queue='unique_id', on_message_callback=self.registerServer, auto_ack=True)
        self.channel.basic_consume(queue='getServerList_incoming', on_message_callback=self.getServerList, auto_ack=True)

    def registerServer(self, ch, method, properties, body):
        body = json.loads(body)
        port=body['port']
        name=body['name']

        if body['request'] == "register":
            print("JOIN REQUEST FROM LOCALHOST:"+str(port))
            if self.serverPortList.count(port) > 0:
                # print("SERVER ALREADY REGISTERED")
                self.channel.basic_publish(exchange='direct_logs', routing_key='unique_id_outgoing', body=json.dumps({'port': port, 'code':"SUCCESS", 'message':self.serverPortList.index(port)}))
            elif self.current_count_servers < self.max_servers :
                self.current_count_servers += 1
                self.serverPortList.append(port)
                self.serverNameList.append(name)
                self.channel.basic_publish(exchange='direct_logs', routing_key='unique_id_outgoing', body=json.dumps({'port': port, 'code':"SUCCESS", 'message': self.current_count_servers -1}))
            else:
                self.channel.basic_publish(exchange='direct_logs', routing_key='error', body=json.dumps({'port': port, 'code':"FAIL", 'message':"Registry Server Full"}))

    def getServerList(self, ch, method, properties, body):
        body = json.loads(body)
        if body['request'] == "getServerList":
            print("SERVER LIST REQUEST FROM LOCALHOST:"+str(body['uuid']))
            response={}
            i=0
            for x in self.serverPortList:
                servs = {
                    "Server": str(self.serverNameList[i]),
                    "Port":str(x),
                    'index': i
                }
                response[i] = servs
                i+=1
            self.channel.basic_publish(
                exchange='direct_logs', routing_key='getServerList_outgoing', body=json.dumps({'list': response}))


if __name__ == "__main__":
    server = RegistryServer(8800)
    print("Registry Server Started")
