from .services_job.services import *
from rest_framework.views import APIView

class backup_api_list(APIView) :
    def get(self, request) :
        return backups_list()

