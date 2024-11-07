from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Subject, Topic, Question
from .serializers import SubjectSerializer, TopicSerializer, QuestionSerializer

class SubjectAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopicAPIView(APIView):
    def get(self, request, subject_id):
        topics = Topic.objects.filter(subject=subject_id)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionPagination(PageNumberPagination):
    page_size = 10

class QuestionAPIView(APIView):
    pagination_class = QuestionPagination

    def get(self, request, topic_id):
        now = timezone.now()
        # Hozirgi vaqt end_time ga qadar bo'lgan savollarni olish
        questions = Question.objects.filter(
            (Q(end_time__isnull=True) | Q(end_time__gte=now)) & 
            (Q(start_time__isnull=True) | Q(start_time__lte=now)),
            topic=topic_id  
        ).order_by('-id')
        paginator = self.pagination_class()
        paginated_questions = paginator.paginate_queryset(questions, request)

        serializer = QuestionSerializer(paginated_questions, many=True)
        return paginator.get_paginated_response(serializer.data)