import random
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import CustomUser
from .tasks import custom_send_email



class TelegramAuthView(APIView):
    """
    Telegram orqali ro'yxatdan o'tish yoki tizimga kirish va JWT token bilan qaytarish
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        telegram_id = data.get("telegram_id")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        if not telegram_id:
            return Response({"error": "Telegram ID talab qilinadi"}, status=400)

        # Foydalanuvchini tekshirish; agar mavjud bo'lmasa, uni yaratamiz
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
        except CustomUser.DoesNotExist:
            user = CustomUser(telegram_id=telegram_id, first_name=first_name, last_name=last_name)
            user.save()

        # JWT tokenlarni yaratish
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Foydalanuvchi ma'lumotlari va tokenlarni qaytarish
        return Response({
            "user": RegisterSerializer(user).data,
            "tokens": tokens
        }, status=200)

def test_auth_tg(request):
    return render(request, 'auth.html')

# class RegisterView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully."}, status=201)
#         return Response(serializer.errors, status=400)

# class ActivateAccountView(APIView):
#     def post(self, request, *args, **kwargs):
#         confirmation = request.data.get('confirmation')
#         email = request.data.get('email')
        
#         try:
#             user = CustomUser.objects.get(email=email, confirmation=confirmation)
#             if not user.is_active:
#                 user.is_active = True
#                 user.confirmation = None  # Clear confirmation code after use
#                 user.save()

#                 # Return a success message, prompting user to login for tokens
#                 return Response({'detail': 'Account activated successfully. Please log in.'}, status=200)
#             else:
#                 return Response({'detail': 'Account already activated.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'Invalid confirmation code or email.'}, status=400)

# class ResendConfirmationView(APIView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         try:
#             user = CustomUser.objects.get(email=email, is_active=True)

#             new_confirmation_code = random.randint(10000, 99999)
#             user.confirmation = new_confirmation_code
#             user.save()

#             custom_send_email(
#                 'TestMaqsad resend',
#                 f'Resend confirmation code is: {new_confirmation_code}',
#                 [email]
#             )

#             return Response({'detail': 'Confirmation code has been resent to your email.'}, status=200)
#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'User with this email does not exist.'}, status=400)

# class LoginWithConfirmationCodeView(APIView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         confirmation = request.data.get('confirmation')

#         try:
#             user = CustomUser.objects.get(email=email, confirmation=confirmation)
#             # Activate the user account
#             user.is_active = True
#             user.confirmation = None  # Clear the confirmation code after successful login
#             user.save()

#             # Generate JWT tokens (using SimpleJWT)
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)

#             return Response({
#                 'detail': 'Account activated successfully.',
#                 'refresh': str(refresh),
#                 'access': access_token
#             }, status=200)

#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'Invalid email or confirmation code.'}, status=400)

class ProfileView(APIView):
    def get(self, request):
        return Response({"message": f"Your email {request.user.email}"})
