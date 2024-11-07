import jwt
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
from user.models import CustomUser  # CustomUser modelini import qilish

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = self.get_token_from_query(scope)

        # Agar foydalanuvchi admin panelda kirgan bo'lsa
        if scope.get("user") and scope["user"].is_authenticated:
            return await super().__call__(scope, receive, send)

        # Agar JWT token bo'lsa
        if token:
            user = await self.get_user_by_token(token)
            if user is not None:
                scope["user"] = user

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_by_token(self, token: str) -> CustomUser:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return CustomUser.objects.get(id=payload['user_id'])  # CustomUser modelidan foydalanish
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return None

    def get_token_from_query(self, scope):
        if 'query_string' in scope:
            query_string = scope['query_string'].decode()
            for param in query_string.split('&'):
                if param.startswith('token='):
                    return param.split('=')[1]
        return None
