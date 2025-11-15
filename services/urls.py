from django.urls import path
from . import views


urlpatterns = [
    path('', views.backup_api_list.as_view())
]