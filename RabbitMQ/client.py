import json
import pika
import uuid

class Client:

    def __init__(self):
        self.id = uuid.uuid4()
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        

    def JoinServer(self):
        pass

    def GetArticles(self):
        pass

    def LeaveServer(self):
        pass

    def GetServerList(self):
        pass

    def PublishArticle(self):
        getTitle = input('Enter title: ')
        getBody = input('Enter body: ')
        getAuthor = input('Enter author: ')
        body={
            'title': getTitle,
            'body': getBody,
            'author': getAuthor
        }
        body = json.dumps(body)
        pass




if __name__ == '__main__':
    client = Client()
    
    while True:
        print('1. Join Server')
        print('2. Get Articles')
        print('3. Leave Server')
        print('4. Get Server List')
        print('5. Publish Article')
        print('6. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            client.JoinServer()
        elif choice == '2':
            client.GetArticles()
        elif choice == '3':
            client.LeaveServer()
        elif choice == '4':
            client.GetServerList()
        elif choice == '5':
            client.PublishArticle()
        elif choice == '6':
            break
        else:
            print('Invalid choice')
    