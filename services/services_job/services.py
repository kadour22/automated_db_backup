from services.models import backupJob
from services.serializers import BackupJobSerializer
# rest framework import
from rest_framework.response import Response
from rest_framework import status
# django import
from django.shortcuts import get_object_or_404

def backups_list() :
    backups = backupJob.objects.all()
    # print(req)
    serializer = BackupJobSerializer(backups, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)

def create_manual_backup(request) :
    serializer = BackupJobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data ,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=404)

def backup_detail_view(request,backup_id) :
    backup = get_object_or_404(backupJob,id=backup_id)
    serializer = BackupJobSerializer(backup) 
    return Response(serializer.data, status.HTTP_200_OK)