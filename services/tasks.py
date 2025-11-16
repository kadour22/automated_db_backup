# from celery import shared_task
# from .models import backupJob
# from .services_job.backup_runner import run_postgres_backup

# @shared_task
# def run_manual_backup_task(job_id) :
#     job = backupJob.objects.get(id=job_id)
#     return run_postgres_backup(job)