from django.contrib import admin
from .models import Domain, Client
from django_tenants.admin import TenantAdminMixin

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin) :
    list_display = ["name"]


@admin.register(Domain)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin) :
    pass
