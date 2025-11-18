from celery import shared_task
from django_tenants.utils import schema_context
from customers.models import Domain
from .services_job.backup_runner import run_postgres_backup

@shared_task
def run_manual_backup_task(job_id, tenant_domain):
    try:
        # Get tenant from domain (public schema)
        domain = Domain.objects.select_related('tenant').get(domain=tenant_domain)
        tenant = domain.tenant
        
        # Access job info within tenant schema
        with schema_context(tenant.schema_name):
            from .models import backupJob
            job = backupJob.objects.get(id=job_id)
            
            # Run backup using job's DB credentials
            # schema_name is optional - only use if tenant is using shared DB with schema isolation
            # If tenant has their own DB, schema_name will be None and entire DB will be backed up
            result = run_postgres_backup(job, schema_name=None)
            
            if result.endswith('.sql'):
                return f"Backup successful: {result}"
            else:
                return f"Backup failed: {result}"
                
    except Domain.DoesNotExist:
        return f"Error: Domain {tenant_domain} not found"
    except Exception as e:
        return f"Error: {str(e)}"