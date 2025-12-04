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

    def __str__(self):
        return self.name
    

class BackFile(models.Model):
    job = models.ForeignKey(backupJob, on_delete=models.CASCADE, related_name='files')
    backup_file = models.FileField(upload_to='backups/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.job.name}"