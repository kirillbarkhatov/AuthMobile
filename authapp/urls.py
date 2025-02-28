from django.urls import path

from authapp.apps import AuthappConfig
from authapp.views import IndexView


app_name = AuthappConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
