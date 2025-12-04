import os
import subprocess
from datetime import datetime


def run_postgres_backup(job, schema_name=None):
    """Run a PostgreSQL backup for a job, optionally for a tenant schema."""

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_label = schema_name if schema_name else job.name
    filename = f"{file_label}_{timestamp}.sql"

    # Create backup directory if missing
    backup_dir = "backups/"
    os.makedirs(backup_dir, exist_ok=True)
    file_path = os.path.join(backup_dir, filename)

    # Prepare pg_dump command
    command = [
        "pg_dump",
        "-h", job.db_host,
        "-p", str(job.db_port),
        "-U", job.db_user,
        "-d", job.db_name,   # Database name (important)
        "-F", "p",           # Plain SQL format
        "--no-owner",
        "--no-acl",
    ]

    # Add schema only if provided
    if schema_name:
        schema_name = schema_name.strip()
        if schema_name:
            command.extend(["-n", schema_name])

    # Export password for pg_dump
    env = os.environ.copy()
    env["PGPASSWORD"] = job.db_password

    try:
        with open(file_path, "w") as f:
            result = subprocess.run(
                command,
                stdout=f,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
            )

        # Check pg_dump errors
        if result.returncode != 0:
            return f"Backup error: {result.stderr}"

        # Detect empty/invalid file
        if os.path.getsize(file_path) < 500:
            return f"Warning: Backup file seems empty ({file_path})"

        return file_path

    except Exception as e:
        return f"Exception during backup: {str(e)}"
