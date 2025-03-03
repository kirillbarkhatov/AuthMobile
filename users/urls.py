from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import RegisterView, SendSMSView, UserProfileView, VerifyCodeView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("send_sms/", SendSMSView.as_view(), name="send_sms"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
