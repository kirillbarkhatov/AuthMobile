from django.urls import path

from authapp.apps import AuthappConfig
from authapp.views import IndexView, EnterInviteCodeView, UserListView
from users.views import PhoneLoginView, PhoneConfirmView
from django.contrib.auth import views as auth_views


app_name = AuthappConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('phone-login/', PhoneLoginView.as_view(), name='phone_login'),
    path('phone-confirm/', PhoneConfirmView.as_view(), name='phone_confirm'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('invite-code/', EnterInviteCodeView.as_view(), name='invite_code'),
    path('users/', UserListView.as_view(), name='users_list'),
]
