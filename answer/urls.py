from django.urls import path
from .views import UserAnswerAPIView, UserAnswersByTopicAPIView

urlpatterns = [
	path('submit-answer', UserAnswerAPIView.as_view()),
	path('topic-answers/<int:topic_id>', UserAnswersByTopicAPIView.as_view()),
]