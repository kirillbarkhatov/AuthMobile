from django.contrib.auth import views as auth_views
from django.urls import path

from authapp.apps import AuthappConfig
from authapp.views import EnterInviteCodeView, IndexView, UserListView
from users.views import PhoneConfirmView, PhoneLoginView

app_name = AuthappConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("phone-login/", PhoneLoginView.as_view(), name="phone_login"),
    path("phone-confirm/", PhoneConfirmView.as_view(), name="phone_confirm"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("invite-code/", EnterInviteCodeView.as_view(), name="invite_code"),
    path("users/", UserListView.as_view(), name="users_list"),
]
