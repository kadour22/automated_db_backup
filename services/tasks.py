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
            
            # Run backup with the tenant's schema name
            result = run_postgres_backup(job, schema_name=tenant.schema_name)
            
            if result.endswith('.sql'):
                return f"Backup successful: {result}"
            else:
                return f"Backup failed: {result}"
                
    except Domain.DoesNotExist:
        return f"Error: Domain {tenant_domain} not found"
    except Exception as e:
        return f"Error: {str(e)}"