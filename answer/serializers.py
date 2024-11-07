from rest_framework import serializers
from .models import UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['user', 'question', 'selected_answer', 'is_correct', 'answered_at']
