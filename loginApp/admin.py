from django.contrib import admin
from .models import Usuario, Tipo_Usuario
from solicitudesManager.models import Solicitud

admin.site.register(Usuario)
admin.site.register(Tipo_Usuario)
admin.site.register(Solicitud)
# Register your models here.
