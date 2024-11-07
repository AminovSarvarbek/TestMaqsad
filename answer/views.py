from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import UserAnswer
from quiz.models import Question, Topic
from .serializers import UserAnswerSerializer


class UserAnswerAPIView(APIView):
	def post(self, request):
		user = request.user
		data = request.data

		# Foydalanuvchi tanlagan javobni tekshirish
		selected_answer = data.get('selected_answer')
		question_id = data.get('question_id')
		if not selected_answer or not question_id:
		    return Response({"detail": "selected_answer and question_id is required."}, status=status.HTTP_400_BAD_REQUEST)

		# Savolni olishga harakat qilamiz, agar savol topilmasa, 404 xatoni qaytaramiz
		try:
		    question = Question.objects.get(id=question_id)
		except Question.DoesNotExist:
		    return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

		now = timezone.now()

		# Savol tugash vaqti mavjudmi va end_time'dan o'tmaganligini tekshirish
		if question.end_time and now > question.end_time:
			return Response({"detail": "Bu savolga javob berish muddati tugagan."}, status=status.HTTP_403_FORBIDDEN)

		if question.is_repeatable:
			# Foydalanuvchi bu savolga oldin javob berganmi va savol qayta javob berishga ruxsat berilmaganmi
			existing_answer = UserAnswer.objects.filter(user=user, question=question).first()
			if existing_answer:
				return Response({"detail": "Siz bu savolga oldin javob bergansiz, qayta javob bera olmaysiz."}, status=status.HTTP_403_FORBIDDEN)

		# Javob to'g'ri ekanligini tekshirish
		is_correct = selected_answer == question.correct_answer

		# Foydalanuvchi javobini yaratish
		user_answer = UserAnswer.objects.create(
		    user=user,
		    question=question,
		    selected_answer=selected_answer,
		    is_correct=is_correct
		)

		serializer = UserAnswerSerializer(user_answer)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserAnswersByTopicAPIView(APIView):
    def get(self, request, topic_id):
        user = request.user

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"detail": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()

        # Agar ko'rish muddati mavjud bo'lsa va undan oldin bo'lsa, javoblarni ko'rsatmaslik
        if topic.view_deadline and now < topic.view_deadline:
            return Response({"detail": "Bu Topicdagi natijalar ko'rish uchun hali ochilmagan."}, status=status.HTTP_403_FORBIDDEN)

        # Foydalanuvchining ushbu Topic bo'yicha bergan javoblarini olish
        user_answers = UserAnswer.objects.filter(user=user, question__topic=topic)

        if not user_answers.exists():
            return Response({"detail": "Siz bu Topicdagi savollarga hali javob bermagansiz."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAnswerSerializer(user_answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)