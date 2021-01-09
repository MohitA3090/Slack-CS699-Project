import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from elasticsearch import Elasticsearch


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']
        if message_type == "delete":
            mid = text_data_json['message_id']
            es = Elasticsearch("192.168.43.177:9200")
            es.delete(index='messages', doc_type='message', id=mid)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': message_type,
                    'message_id': mid
                }
            )
        else:
            message = text_data_json['message']
            author = text_data_json['author']
            channel = text_data_json['channel']
            reply_to = text_data_json['reply_to']
            author_pk = text_data_json['author_pk']
            timestamp = str(timezone.now().strftime("%b %d %Y %H:%M"))
            text_data_json['timestamp'] = timestamp
            print(text_data_json)
            # store in elastic search #
            es = Elasticsearch("192.168.43.177:9200")
            record = es.index(index='messages', doc_type='message', body=text_data_json)
            print(record['_id'])
            # store in elastic search #
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': message_type,
                    'message': message,
                    'author': author,
                    'timestamp': timestamp,
                    'reply_to': reply_to,
                    'author_pk': author_pk,
                    'message_id': record['_id']
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        mid = event['message_id']
        if event['message_type'] == "delete":
            self.send(text_data=json.dumps({
                'message_type': "delete",
                'message_id': mid
            }))
        else:
            message = event['message']
            author = event['author']
            timestamp = event['timestamp']
            reply_to = event['reply_to']
            author_pk = event['author_pk']
            print(message)
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message_type': "insert",
                'message': message,
                'author': author,
                'author_pk': author_pk,
                'timestamp': timestamp,
                'reply_to':reply_to,
                'message_id':mid
            }))
