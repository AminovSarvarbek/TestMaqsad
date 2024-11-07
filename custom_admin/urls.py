from django.urls import path
from django.conf import settings
from .views import (
    HomeView,
    QuestionListView,
    QuestionEditView,
    QuestionAddView,
    QuestionDeleteView,
    CustomUserListView,
    CustomUserEditView,
    CustomUserAddView,
    CustomUserDeleteView,
    login_view,
    logout_view,
    update_admin_profile,
    chat_user_list_view,
    chat_user_messages_view,
    upload_questions_from_excel
)
from . import crud_views

app_name = 'custom_admin'
urlpatterns = [
    path('login/', login_view, name='admin_login'),
    path('logout/', logout_view, name='admin_logout'),
    path('', HomeView.as_view(), name='home'),
    path('profile/update', update_admin_profile, name='admin_update'),

    path('questions/', QuestionListView.as_view(), name='questions'),
    path('question/<int:question_id>/', QuestionEditView.as_view(), name='update'),
    path('question/add/', QuestionAddView.as_view(), name='add'),
    path('questions/upload/', upload_questions_from_excel, name='upload_questions'),
    path('question/delete/<int:question_id>/', QuestionDeleteView.as_view(), name='question_delete'),

    path('users/', CustomUserListView.as_view(), name='users'),
    path('user/<int:user_id>/', CustomUserEditView.as_view(), name='user_update'),
    path('user/add/', CustomUserAddView.as_view(), name='user_add'),
    path('user/delete/<int:user_id>/', CustomUserDeleteView.as_view(), name='user_delete'),

    path('chat/users/', chat_user_list_view, name='chat_user_list'),
    path('chat/user/<int:user_id>/', chat_user_messages_view, name='chat_user_messages'),

    # for crud any model
    path('<str:app_label>/<str:model_name>/', crud_views.dynamic_model_list, name='dynamic_model_list'),
    path('<str:app_label>/<str:model_name>/add/', crud_views.dynamic_model_form, name='dynamic_model_add'),
    path('<str:app_label>/<str:model_name>/<int:pk>/', crud_views.dynamic_model_form, name='dynamic_model_edit'),
    path('<str:app_label>/<str:model_name>/<int:pk>/delete/', crud_views.dynamic_model_delete, name='dynamic_model_delete'),
]
