from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

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
