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
