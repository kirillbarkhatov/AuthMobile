from django.urls import path

from authapp.apps import AuthappConfig
from authapp.views import IndexView, EnterInviteCodeView, UserListView
from users.views import PhoneLoginView, PhoneConfirmView


app_name = AuthappConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('phone-login/', PhoneLoginView.as_view(), name='phone_login'),
    path('phone-confirm/', PhoneConfirmView.as_view(), name='phone_confirm'),
    path('invite-code/', EnterInviteCodeView.as_view(), name='invite_code'),
    path('users/', UserListView.as_view(), name='users_list'),
]
