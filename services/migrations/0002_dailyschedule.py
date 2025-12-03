from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailySchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day_of_week",
                    models.CharField(
                        choices=[
                            ("monday", "Monday"),
                            ("tuesday", "Tuesday"),
                            ("wednesday", "Wednesday"),
                            ("thursday", "Thursday"),
                            ("friday", "Friday"),
                            ("saturday", "Saturday"),
                            ("sunday", "Sunday"),
                        ],
                        max_length=10,
                    ),
                ),
                ("schedule_time", models.TimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_schedules",
                        to="services.backupjob",
                    ),
                ),
            ],
            options={
                "ordering": ["job", "day_of_week", "schedule_time"],
                "unique_together": {("job", "day_of_week", "schedule_time")},
            },
        ),
    ]



