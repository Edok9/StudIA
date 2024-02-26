from django.contrib import admin
from .models import Usuario
from solicitudesManager.models import Solicitud

admin.site.register(Usuario)
admin.site.register(Solicitud)
# Register your models here.
