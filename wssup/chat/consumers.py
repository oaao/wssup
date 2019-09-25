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

        # obtain the 'room_name' URLparam from the URL route that opened the ws connection to the consumer
        # scope: information about a consumer's connection,
        #   including *args **kwargs from URL route and/or currently authed user
        self.room       = self.scope['url_route']['kwargs']['room_name']

        # will fail on names outside alphanumeric+hyphens+periods charset
        self.room_group = f'chat_{self.room}'

        # join the groom group
        # we currently have a synchronous consumer, but call a channel layer method (all of which are async)
        a2s(self.channel_layer.group_add)(
            self.room_group,
            self.channel_name
        )

        # if accept() is not called within the connect method,
        # then the connection is rejected and closed. can use this in future for auth check
        self.accept()

    def disconnect(self, close_code):

        # leave the room group
        a2s(self.channel_layer.group_discard)(
            self.room_group,
            self.channel_name
        )
        pass

    def receive(self, text_data):
        j   = json.loads(text_data)
        msg = j['message']

        # send msg to room group
        a2s(self.channel_layer.group_send)(
            self.room_group,
            {'type': 'chat_message', 'message': msg}
        )

    def chat_message(self, event):

        msg = event['message']

        # send a message to websocket
        self.send(text_data=json.dumps({'message': msg}))
