from services.models import backupJob
from services.serializers import BackupJobSerializer

from rest_framework.response import Response
from rest_framework import status

def backups_list() :
    backups = backupJob.objects.all()
    serializer = BackupJobSerializer(backups, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)