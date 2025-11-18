
import os
# from channels.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automated_db_backup.settings')

application = get_asgi_application()
