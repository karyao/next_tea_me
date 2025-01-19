import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, Friendship

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Ensure consistent room naming regardless of who initiates
        usernames = self.room_name.split('_')
        usernames.sort()  # Sort to ensure same room name regardless of sender/receiver
        self.room_group_name = f"chat_{'_'.join(usernames)}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver']

        # Save message to database
        await self.save_message(message, receiver_username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
                'receiver': receiver_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver']
        }))

    @database_sync_to_async
    def save_message(self, message, receiver_username):
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(
            sender=self.scope['user'],
            receiver=receiver,
            content=message
        )

waiting_user = None

class FriendshipConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global waiting_user

        # Extract user information from query parameters (or another method)
        self.username = self.scope['query_string'].decode().split('=')[1]  # Example: ws://host/ws/friendship/?username=John

        if waiting_user is None:
            # No one is waiting, so make this user wait
            waiting_user = {
                'consumer': self,
                'username': self.username
            }
            await self.accept()
            await self.send(json.dumps({
                'message': 'Waiting for a teabag...'
            }))
        else:
            # Pair with the waiting user
            partner = waiting_user
            waiting_user = None  # Clear the waiting user

            # Accept connections for both users
            await self.accept()
            #test
            await partner['consumer'].send(json.dumps({
                'redirect': f'/add_friend/?partner={self.username}'
            }))
            await self.send(json.dumps({
                'redirect': f'/add_friend/?partner={partner["username"]}'
            }))

    async def disconnect(self, close_code):
        # Notify the frontend to redirect
        try:
            await self.send(text_data=json.dumps({"redirect": "/brew_page/"}))
        except:
            pass  # WebSocket might already be closed, ignore errors

    async def receive(self, text_data):
        # Handle incoming WebSocket data
        data = json.loads(text_data)
        message = data.get('message', '')
        await self.send(text_data=json.dumps({"message": f"Received: {message}"}))
