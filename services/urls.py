from django.urls import path
from . import views

urlpatterns = [
    # List all backups or create a new one
    path('backups/', views.backup_api_list.as_view(), name='backups-list-create'),
    # Detail view (GET) or delete a specific backup
    path('backups/<int:backup_id>/', views.backup_api_list.as_view(), name='backup-detail-delete'),
    # Trigger manual backup task
    path('backups/<int:job_id>/run/', views.ManualBackup.as_view(), name='backup-run'),
]

