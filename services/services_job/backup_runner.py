import os 
import subprocess
from datetime import datetime

def run_postgres_backup(job, schema_name=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if schema_name:
        filename = f"{schema_name}_{timestamp}.sql"
    else:
        filename = f"{job.name}_{timestamp}.sql"
    
    backup_dir = 'backups/'
    os.makedirs(backup_dir, exist_ok=True)
    file_path = os.path.join(backup_dir, filename)
    
    # Build command
    command = [
        "pg_dump",
        "-h", job.db_host,
        "-p", str(job.db_port),
        "-U", job.db_user,
        "-d", job.name,
        "-F", "p",
        "-f", file_path,
        "--no-owner",
        "--no-acl"
    ]
    
    # Only add schema flag if schema_name is provided AND not empty
    if schema_name and schema_name.strip():
        # Try with schema pattern matching
        command.extend(["-n", schema_name])
    
    # Set password via environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = job.db_password
    
    try:
        result = subprocess.run(
            command, 
            env=env,
            capture_output=True, 
            text=True,
            check=False  # Don't raise exception, we'll check manually
        )
        
        # Check return code
        if result.returncode != 0:
            # Try without schema filter as fallback
            if schema_name:
                print(f"Schema backup failed, trying full database backup...")
                command_no_schema = [c for c in command if c not in ["-n", schema_name]]
                result = subprocess.run(
                    command_no_schema,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False
                )
        
        if result.returncode != 0:
            return f"Backup failed: {result.stderr}\nCommand: {' '.join(command)}"
        
        # Verify file was created and has content
        if not os.path.exists(file_path):
            return f"Error: Backup file was not created at {file_path}"
        
        file_size = os.path.getsize(file_path)
        if file_size < 500:
            return f"Warning: Backup file is only {file_size} bytes. This might be empty."
        
        return file_path
        
    except Exception as e:
        return f"Exception during backup: {str(e)}"