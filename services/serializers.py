from rest_framework import serializers
from .models import backupJob

class BackupJobSerializer(serializers.ModelSerializer) :
    class Meta :
        model  = backupJob
        fields = [
            "id", "name", "db_type", "db_name", "db_host", "db_port", 
            "db_user", "db_password", "schedule_type", "schedule_time",
            "keep_last", "is_active", "created_at"
        ]
        read_only_fields = ["id", "created_at"]