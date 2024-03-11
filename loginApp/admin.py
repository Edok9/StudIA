from django.contrib import admin
from .models import Usuario
from solicitudesManager.models import Solicitud, Tipo_Solicitud, Dato_Entrada, Dato_Salida

admin.site.register(Usuario)
admin.site.register(Solicitud)
admin.site.register(Tipo_Solicitud)
admin.site.register(Dato_Entrada)
admin.site.register(Dato_Salida)
# Register your models here.
