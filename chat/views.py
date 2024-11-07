from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Message

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def get_user_messages(request):
    messages = Message.objects.filter(user=request.user)

    if not messages.exists():
        return JsonResponse({
            'unseen_count': 0,
            'messages': []
        }, status=200)

    unseen_count = messages.filter(seen_by_user=False).count()

    paginator = CustomPagination()
    paginated_messages = paginator.paginate_queryset(messages, request)

    message_data = [
        {
            'id': message.id,
            'content': message.message,
            'timestamp': message.timestamp,
            'seen_by_user': message.seen_by_user
        }
        for message in paginated_messages
    ]

    if unseen_count > 0:
        messages.filter(seen_by_user=False).update(seen_by_user=True)

    return paginator.get_paginated_response({
        'unseen_count': unseen_count,
        'messages': message_data
    })

@api_view(['GET'])
def get_user_info(request):
    messages = Message.objects.filter(user=request.user)

    unseen_count = messages.filter(seen_by_user=False).count()
    total_messages_count = messages.count()

    return JsonResponse({
        'total_messages': total_messages_count,
        'unseen_count': unseen_count
    }, status=200)
