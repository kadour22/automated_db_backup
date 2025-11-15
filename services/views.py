from .services_job.services import *
from rest_framework.views import APIView
from .tasks import *
class backup_api_list(APIView) :
    def get(self, request,backup_id=None) :
        if backup_id is not None:
            return backup_detail_view(request,backup_id)
        
        return backups_list()
    def post(self,request):
        return create_manual_backup(request)
class ManualBackup(APIView):
    def post(self, request, job_id):
        run_back_task.delay(job_id)
        return Response({"message": "Backup started"})
