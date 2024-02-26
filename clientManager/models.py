from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1)
    nombre_sn = models.CharField(max_length=30)

class Dominio(DomainMixin):
    pass

# Create your models here.
