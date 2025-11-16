# local imports
from services.models import backupJob
from services.serializers import BackupJobSerializer
# rest framework import
from rest_framework.response import Response
from rest_framework import status
# django import
from django.shortcuts import get_object_or_404

# service functions :

# 1. list all backups
def backups_list() :
    backups = backupJob.objects.all()
    serializer = BackupJobSerializer(backups, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)

# 2. create manual backup
def create_manual_backup(request) :
    serializer = BackupJobSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data ,status=status.HTTP_201_CREATED)

# 3. retrieve backup details
def backup_detail_view(request,backup_id) :
    backup = get_object_or_404(backupJob,id=backup_id)
    serializer = BackupJobSerializer(backup) 
    return Response(serializer.data, status=status.HTTP_200_OK)

# 4. delete backup
def delete_backup(request,backup_id) :
    backup = get_object_or_404(backupJob,id=backup_id)
    backup.delete()
    return Response({"message":"Backup deleted successfully"}, status=status.HTTP_204_NO_CONTENT)