from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, VerifyCodeView, UserProfileView


app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
