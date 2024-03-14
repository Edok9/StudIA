from django.db import models
from loginApp.models import Usuario

class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True)
    estado_sol = models.CharField(max_length=25, verbose_name = "Estado", default="Pendiente")
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name = "Usuario")

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
    
    def __str__(self):
        return self.nombre_sol
    
class Xsoar_Ise_Vpn(models.Model):
    id_ise = models.AutoField(primary_key=True)
    accion = models.CharField(max_length=30)
    usuario = models.CharField(max_length=25)
    correo_usuario = models.CharField(max_length=25)
    fecha_expiracion = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    estado_caso = models.CharField(max_length=10)
    id_caso = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    
class Xsoar_Ioc_Automatico(models.Model):
    id_ioc = models.AutoField(primary_key=True)
    adjunto = models.FileField(upload_to="archivos/")
    notas = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    estado_caso = models.CharField(max_length=10)
    id_caso = models.OneToOneField(Solicitud, on_delete=models.CASCADE)

class Xsoar_Cambio_De_Ruta(models.Model):
    id_cambio = models.AutoField(primary_key=True)
    gateway = models.CharField(max_length=30)
    interfaz_salida = models.CharField(max_length=25)
    id_ruta = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    estado_caso = models.CharField(max_length=10)
    id_caso = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
# Create your models here.
