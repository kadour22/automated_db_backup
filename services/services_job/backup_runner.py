import os 
import subprocess
from datetime import datetime

def run_postgres_backup(job):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    filename = f"{job.name}_{timestamp}.sql"

    backup_dir = 'backups/'

    os.makedirs(backup_dir, exist_ok=True)
    file_path = os.path.join(backup_dir, filename)

    command = [
        "pg_dump",
        f"--dbname=postgres://{job.db_user}:{job.db_password}@{job.db_host}:{job.db_port}/{job.name}",
        "-F","p",
        "-f", file_path
    ]


    try:
        subprocess.check_call(command)
        return file_path
    except Exception as e:
        return str(e)