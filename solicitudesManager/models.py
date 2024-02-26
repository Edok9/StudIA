from django.db import models
from loginApp.models import Usuario
    
class Tipo_Solicitud(models.Model):
    id_tipo_sol = models.AutoField(primary_key=True)
    descripcion_t_sol = models.CharField(max_length=70)
    nombre_t_sol = models.CharField(max_length=25)
    estado_sol = models.CharField(max_length=1)
   
class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True)
    nombre_sol = models.CharField(max_length=30)
    tipo_sol = models.CharField(max_length=30)
    descripcion_sol = models.CharField(max_length=70)
    created_at = models.DateTimeField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_tipo_sol = models.OneToOneField(Tipo_Solicitud, on_delete=models.CASCADE)
    
class Dato_Entrada(models.Model):
    id_datos_ent = models.AutoField(primary_key=True)
    email_usuario = models.CharField(max_length=30)
    nombre_cuenta = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    adjunto = models.FileField(upload_to='archivos/')
    notas = models.CharField(max_length=30)
    id_tipo_sol = models.OneToOneField(Tipo_Solicitud, on_delete=models.CASCADE)
    
class Dato_Salida(models.Model):
    id_datos_sal = models.AutoField(primary_key=True)
    estado_sal = models.CharField(max_length=40)
    fecha_resol = models.DateTimeField()
    id_tipo_sol = models.OneToOneField(Tipo_Solicitud, on_delete=models.CASCADE)

# Create your models here.
