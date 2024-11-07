import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message

User = get_user_model()

class ApiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.user_id}'

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
        data = json.loads(text_data)
        message = data['message']

        target_user = await self.get_target_user(self.user_id)
        admin_user = self.user if self.user.is_superuser else None

        msg_instance = await self.save_message(target_user, message, admin_user)

        # Set seen_by_admin to True if the message is from an admin
        if admin_user:
            msg_instance.seen_by_admin = True
            await sync_to_async(msg_instance.save)()  # Save the updated message instance

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg_instance.message,
                'timestamp': msg_instance.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_admin': bool(admin_user)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'timestamp': event['timestamp'],
            'is_admin': event['is_admin']
        }))

    async def get_target_user(self, user_id):
        try:
            return await sync_to_async(User.objects.get)(id=user_id)
        except User.DoesNotExist:
            return None

    async def save_message(self, user, message, admin):
        return await sync_to_async(Message.objects.create)(
            user=user,
            message=message,
            admin=admin
        )
