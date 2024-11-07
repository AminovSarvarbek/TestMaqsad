from django.urls import path
from .views import SubjectAPIView, TopicAPIView, QuestionAPIView

urlpatterns = [
    path('subjects', SubjectAPIView.as_view(), name='subjects-api'),
    path('topics/<int:subject_id>', TopicAPIView.as_view(), name='topics-api'),
    path('questions/<int:topic_id>', QuestionAPIView.as_view(), name='questions-api'),
]
