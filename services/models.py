from django.db import models

class backupJob(models.Model) :
    name = models.CharField(max_length=100)
    
    db_type = models.CharField(max_length=20, default='postgres')
    db_name = models.CharField(max_length=100)
    db_host = models.CharField(max_length=200)
    db_port = models.IntegerField(default=5432)
    db_user = models.CharField(max_length=100)
    db_password = models.CharField(max_length=300)

    SCHEDULE_CHOICES = (
        ("daily","Daily"),
        ("weekly","Weekly"),
        ("monthly","Monthly"),
        ("manual","Manual Only"),
    )

    schedule_type = models.CharField(max_length=100 , choices=SCHEDULE_CHOICES)
    schedule_time = models.TimeField(null=True, blank=True)

    keep_last = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and backupJob.objects.exists() :
            raise Exception('Only one backupJob instance allowed.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class backupHistory(models.Model) :
    backup_job = models.ForeignKey(backupJob, on_delete=models.CASCADE, related_name='histories')
    backup_date = models.DateTimeField(auto_now_add=True)
    backup_count = models.IntegerField(default=0)
    def __str__(self):
        return f"Backup for {self.backup_job.name} on {self.backup_date}"
    

