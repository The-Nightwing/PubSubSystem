import json
import pika
import uuid


class Client:

    def __init__(self):
        self.id = uuid.uuid4()
        self.connectedServers = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        self.init_consumer(0)
    
    def init_consumer(self,port):
        self.channel.queue_declare(queue='getServerList_incoming')
        self.channel.queue_bind(exchange='direct_logs',queue='getServerList_incoming', routing_key='getServerList_incoming')

        self.channel.queue_declare(queue='getServerList_outgoing')
        self.channel.queue_bind(exchange='direct_logs',queue='getServerList_outgoing', routing_key='getServerList_outgoing')

        self.channel.queue_declare(queue='register_incoming'+"_"+str(port))
        self.channel.queue_bind(exchange='direct_logs', queue='register_incoming'+"_"+str(port), routing_key='register_incoming'+"_"+str(port))

        self.channel.queue_declare(queue='register_outgoing'+"_"+str(port))
        self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing'+"_"+str(port), routing_key='register_outgoing'+"_"+str(port))

        self.channel.basic_consume(queue='getServerList_outgoing', on_message_callback=self.GetServerListCallback, auto_ack=True)
        self.channel.basic_consume(queue='register_outgoing'+"_"+str(port), on_message_callback=self.RegisterCallback, auto_ack=True)

    def RegisterCallback(self,ch,method,properties,body):
        body = json.loads(body)
        print(body)
        print(body['status'])
        if body['request']=='register':
            if (body['status']=='SUCCESS'):
                self.connectedServers.append(body['index'])
            self.channel.stop_consuming()
        elif (body['request']=='remove'):
            if (body['status']=='SUCCESS'):
                self.connectedServers.remove(body['index'])
            self.channel.stop_consuming()

    def JoinServer(self,port):
        self.init_consumer(port)
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(port), body=json.dumps(
            {'request': 'register', 'uuid': str(self.id)}))
        self.channel.start_consuming()

        pass

    def GetArticles(self):
        
        pass

    def LeaveServer(self,port):
        self.init_consumer(port)
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(port), body=json.dumps(
            {'request': 'remove', 'uuid': str(self.id)}))
        self.channel.start_consuming()
        pass

    def init_consume(self):
        self.channel.basic_consume(queue='getServerList_outgoing', on_message_callback=self.GetServerListCallback, auto_ack=True)

    def GetServerListCallback(self, ch, method, properties, body):
        body = json.loads(body)
        i=0
        for x in body['list']:
            print(str(i)+': '+x+'-'+body['list'][x])
            i+=1
        self.channel.stop_consuming()

    
    def GetServerList(self):
        self.channel.basic_publish(exchange='direct_logs', routing_key='getServerList_incoming', body=json.dumps(
            {'request': 'getServerList', 'uuid': str(self.id)}))
        self.init_consume()
        self.channel.start_consuming()

    def PublishArticle(self):
        getTitle = input('Enter title: ')
        getBody = input('Enter body: ')
        getAuthor = input('Enter author: ')
        body = {
            'title': getTitle,
            'body': getBody,
            'author': getAuthor
        }
        body = json.dumps(body)
        pass
    def printConnectedServers(self):
        print(self.connectedServers)


if __name__ == '__main__':
    client = Client()

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
            client.JoinServer(port)
        elif choice == '2':
            client.GetArticles()
        elif choice == '3':
            port=input('Choose Server to Leave: ')
            client.LeaveServer(port)
        elif choice == '4':
            client.GetServerList()
            # client.channel.start_consuming()
        elif choice == '5':
            client.PublishArticle()
        elif choice == '6':
            client.printConnectedServers()
        elif choice == '7':
            break
        else:
            print('Invalid choice')
