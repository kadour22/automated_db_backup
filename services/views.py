from .services_job.services import *
from rest_framework.views import APIView
from .tasks import *

class backup_api_list(APIView) :
    # detail && list view
    def get(self, request,backup_id=None) :
        if backup_id is not None:
            return backup_detail_view(request,backup_id)
        else:
            return backups_list()
    # create view
    def post(self,request):
        return create_manual_backup(request)
    # delete view
    def delete(self, request, backup_id):
        return delete_backup(request,backup_id)
    
class ManualBackup(APIView):
    def post(self, request, job_id):
        tenant_domain = request.tenant.domains.first().domain  
        run_manual_backup_task.delay(job_id, tenant_domain)
        return Response({"message": "Backup started"})
