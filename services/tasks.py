from celery import shared_task
from django.utils import timezone
from .models import backupJob
import subprocess
from datetime import timedelta


@shared_task
def run_scheduled_backups():
    now = timezone.localtime()
    current_time = now.time()
    current_weekday = now.weekday()  # Monday = 0
    day_of_month = now.day

    jobs = backupJob.objects.filter(is_active=True)

    for job in jobs:

        # DAILY
        if job.schedule_type == "daily":
            if job.schedule_time and job.schedule_time.hour == current_time.hour and job.schedule_time.minute == current_time.minute:
                backup_database(job.id)

        # WEEKLY (run on Monday)
        if job.schedule_type == "weekly":
            if current_weekday == 0 and job.schedule_time.hour == current_time.hour and job.schedule_time.minute == current_time.minute:
                backup_database(job.id)

        # MONTHLY (run on day 1)
        if job.schedule_type == "monthly":
            if day_of_month == 1 and job.schedule_time.hour == current_time.hour and job.schedule_time.minute == current_time.minute:
                backup_database(job.id)
@shared_task
def backup_database(job_id):
    job = backupJob.objects.get(id=job_id)

    filename = f"{job.name}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sql"
    filepath = f"/home/abdelkader/backups/{filename}"

    # Example for Postgres
    command = [
        "pg_dump",
        f"--dbname=postgresql://{job.db_user}:{job.db_password}@{job.db_host}:{job.db_port}/{job.db_name}",
        "-f",
        filepath,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Backup created: {filepath}")
    except Exception as e:
        print(f"Backup failed: {e}")

    # Keep only last N backups
    cleanup_old_backups(job)
