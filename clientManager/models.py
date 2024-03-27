from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=25, verbose_name="Nombre de la Empresa")
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, verbose_name="Estado")
    nombre_sn = models.CharField(max_length=30, verbose_name="Nombre del Socio de Negocio")
    casos_disponibles = ArrayField(models.TextField(), editable=False, default=list)
class Dominio(DomainMixin):
    pass

# Create your models here.
