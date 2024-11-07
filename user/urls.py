from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ProfileView,
    TelegramAuthView,
    test_auth_tg,
    # RegisterView,
    # ActivateAccountView,
    # ResendConfirmationView,
    # LoginWithConfirmationCodeView
)
from .serializers import CustomTokenObtainPairSerializer


urlpatterns = [
    path('auth/telegram', TelegramAuthView.as_view(),),
    path('auth/', test_auth_tg),
    # path('register', RegisterView.as_view(), name='register'),
    # path('activate', ActivateAccountView.as_view(), name='activate'),
    # path('login', 
    #     TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('resend', ResendConfirmationView.as_view(), name='resend'),
    # path('login/email', LoginWithConfirmationCodeView.as_view(), name='login-with-email'),
    path('profile', ProfileView.as_view()),
]
