from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users.apps import UsersConfig
from users.views import RegisterView, VerifyCodeView, UserProfileView, SendSMSView


app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="authapp:index"),
        name="logout",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset/password_reset_form.html",
            email_template_name="password_reset/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path("send_sms/", SendSMSView.as_view(), name="send_sms"),
]
