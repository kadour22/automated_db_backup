from rest_framework import serializers
from .models import backupJob

class BackupJobSerializer(serializers.ModelSerializer) :
    class Meta :
        model  = backupJob
        fields = [
            "db_type","db_name","db_host","db_port","db_user","db_password","schedule_type"
        ]


        {
            "db_type":"postgres",
            "db_name":"backup_db",
            "db_host":"localhost",
            "db_port":"5432",
            "db_user":"postgres",
            "db_password":"zaza",
            "schedule_type":"manual"
        }