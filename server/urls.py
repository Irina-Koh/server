from django.urls import path
from server.apps import ServerConfig

from .views import IndexView

app_name = ServerConfig.name
urlpatterns = [
    path('', IndexView.as_view(), name='messages_list'),

]