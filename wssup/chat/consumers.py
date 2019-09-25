import json

from asgiref.sync               import async_to_sync as a2s
from channels.generic.websocket import WebsocketConsumer


class Consumer(WebsocketConsumer):
    """
    Synchronous websocket consumer.
        - accepts all connections
        - receives messages from its client
        - echoes those messages back to the same client
        - does NOT broadcast msgs to other clients in the 'room'

    NOTE TO FUTURE SELF:
    If writing an asynchronous consumer, be extremely attentive
    to avoid directly performing any blocking operations
    such as accessing a Django model.
    """

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        j   = json.loads(text_data)
        msg = j['message']

        self.send(text_data=json.dumps({'message': msg}))
