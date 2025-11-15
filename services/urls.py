from django.urls import path
from . import views


urlpatterns = [
    path('<int:backup_id>/', views.backup_api_list.as_view()),
    path('', views.backup_api_list.as_view())
]