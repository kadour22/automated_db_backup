import os
import subprocess
from datetime import datetime

def run_postgres_backup(job, schema_name=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    file_label = schema_name if schema_name else job.name
    filename = f"{file_label}_{timestamp}.sql"

    backup_dir = 'backups/'
    os.makedirs(backup_dir, exist_ok=True)
    file_path = os.path.join(backup_dir, filename)

    command = [
        "pg_dump",
        "-h", job.db_host,
        "-p", str(job.db_port),
        "-U", job.db_user,
        "-d", job.db_name,     # FIXED (IMPORTANT)
        "-F", "p",
        "--no-owner",
        "--no-acl"
    ]

    # Add tenant schema if provided
    if schema_name and schema_name.strip():
        command.extend(["-n", schema_name])

    env = os.environ.copy()
    env['PGPASSWORD'] = job.db_password

    try:
        # Write using stdout redirection (safer than -f)
        with open(file_path, "w") as f:
            result = subprocess.run(
                command,
                env=env,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )

        if result.returncode != 0:
            return f"Backup error: {result.stderr}"

        # Validate file size
        if os.path.getsize(file_path) < 500:
            return f"Warning: Backup file seems empty ({file_path})"

        return file_path

    except Exception as e:
        return f"Exception during backup: {str(e)}"
