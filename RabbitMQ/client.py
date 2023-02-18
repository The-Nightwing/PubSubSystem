import json
import pika
import uuid


class Client:

    def __init__(self):
        self.id = uuid.uuid4()
        self.connectedServers = {}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.ServerList = {}
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        self.init_consumer(0)
    
    def init_consumer(self,port):
        index = 0
        if port in self.ServerList.keys():
            index = self.ServerList[port]
        self.channel.queue_declare(queue='getServerList_incoming')
        self.channel.queue_bind(exchange='direct_logs',queue='getServerList_incoming', routing_key='getServerList_incoming')

        self.channel.queue_declare(queue='getServerList_outgoing')
        self.channel.queue_bind(exchange='direct_logs',queue='getServerList_outgoing', routing_key='getServerList_outgoing')

        self.channel.queue_declare(queue='register_incoming'+"_"+str(index))
        self.channel.queue_bind(exchange='direct_logs', queue='register_incoming'+"_"+str(index), routing_key='register_incoming'+"_"+str(index))

        self.channel.queue_declare(queue='register_outgoing'+"_"+str(index))
        self.channel.queue_bind(exchange='direct_logs', queue='register_outgoing'+"_"+str(index), routing_key='register_outgoing'+"_"+str(index))

        self.channel.basic_consume(queue='getServerList_outgoing', on_message_callback=self.GetServerListCallback, auto_ack=True)
        self.channel.basic_consume(queue='register_outgoing'+"_"+str(index), on_message_callback=self.outgoingCallback, auto_ack=True)

    def outgoingCallback(self,ch,method,properties,body):
        body = json.loads(body)
        # print(body)
        print(body['status'])
        if body['request']=='register':
            if (body['status']=='SUCCESS'):
                self.connectedServers[body['port']] = body['index']
            self.channel.stop_consuming()

        elif (body['request']=='remove'):
            if (body['status']=='SUCCESS'):
                del self.connectedServers[body['port']]
            self.channel.stop_consuming()

        elif (body['request']=='getArticles'):
            if (body['status']=='SUCCESS'):
                print('FOR %r, %r, %r' % (body['type'], body['author'], body['time']))
                res=body['articles']['list']
                for x in res:
                    print('Type: '+x['type']+'\nAuthor: '+x['author']+'\nTime: '+x['time']+'\nBody: '+x['body']+'\n')
            self.channel.stop_consuming()

        elif (body['request']=='publishArticle'):
            # if (body['status']=='SUCCESS'):
                # print('Article published')
            self.channel.stop_consuming()

    def JoinServer(self,port):
        self.init_consumer(port)
        index =  self.ServerList[port]
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(index), body=json.dumps(
            {'request': 'register', 'uuid': str(self.id)}))
        self.channel.start_consuming()
        pass

    def LeaveServer(self,port):
        self.init_consumer(port)
        if port not in self.connectedServers.keys():
            print('Not connected to server')
            return
        index =  self.connectedServers[port]
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(index), body=json.dumps(
            {'request': 'remove', 'uuid': str(self.id)}))
        self.channel.start_consuming()
        pass

    def init_consume(self):
        self.channel.basic_consume(queue='getServerList_outgoing', on_message_callback=self.GetServerListCallback, auto_ack=True)

    def GetServerListCallback(self, ch, method, properties, body):
        body = json.loads(body)
        # print(body)
        for x in body['list'].keys():
            res=body['list'][x]
            print('Server:'+res['Server'] +' - localhost:'+res['Port'])
            self.ServerList[res['Port']] = res['index']
        self.channel.stop_consuming()

    def GetServerList(self):
        self.channel.basic_publish(exchange='direct_logs', routing_key='getServerList_incoming', body=json.dumps(
            {'request': 'getServerList', 'uuid': str(self.id)}))
        self.init_consume()
        self.channel.start_consuming()

    def PublishArticle(self):
        getType = input('Enter type: ')
        getBody = input('Enter body: ')
        getAuthor = input('Enter author: ')
        self.printConnectedServers()
        getServerPort = input('Enter server port: ')
        if getType == '' or getBody == '' or getAuthor == '' or getServerPort == '':
            print('Invalid input')
            return
        body = {
            'request': 'publishArticle',
            'uuid': str(self.id),
            'article' : {
            'type': getType,
            'body': getBody,
            'author': getAuthor
            }
        }
        body = json.dumps(body)
        index = self.connectedServers[getServerPort]
        self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(index), body=body)
        self.init_consumer(getServerPort)
        self.channel.start_consuming()

    def GetArticles(self):
        self.printConnectedServers()
        port = input('Enter server port to Get Articles from: ')
        type = input('Type: ')
        author = input('Author: ')
        time = input('Time (YYYY-MM-DD): ')
        if port in self.connectedServers.keys():
            index = self.connectedServers[port]
            body = {
                'request': 'getArticles',
                'uuid': str(self.id),
                'article': {
                'type': type,
                'author': author,
                'time': time
                }
            }
            body = json.dumps(body)
            self.channel.basic_publish(exchange='direct_logs', routing_key='register_incoming'+"_"+str(index), body=body)
            self.init_consumer(port)
            self.channel.start_consuming()
        else:
            print('Not connected to server')
            return

    def printConnectedServers(self):
        for i in self.connectedServers:
            print("Connected to Port: %r" %i)

if __name__ == '__main__':
    client = Client()

    while True:
        print('\n1. Join Server')
        print('2. Get Articles')
        print('3. Leave Server')
        print('4. Get Server List')
        print('5. Publish Article')
        print('6. Print Connected Servers')
        print('7. Exit\n')
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
