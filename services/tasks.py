from celery import shared_task
import subprocess
import tempfile
from .models import backupJob
from .services_job.backup_runner import run_postgres_backup

@shared_task
def run_back_task(job_id) :
    job = backupJob.objects.get(id=job_id)
    return run_postgres_backup(job)