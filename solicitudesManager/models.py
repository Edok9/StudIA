from django.db import models
from loginApp.models import Usuario
    
class Tipo_Solicitud(models.Model):
    id_tipo_sol = models.AutoField(primary_key=True)
    descripcion_t_sol = models.CharField(max_length=70, verbose_name = "Descripción")
    nombre_t_sol = models.CharField(max_length=25, verbose_name = "Nombre")

    class Meta:
        verbose_name = "Tipo de Solicitud"
        verbose_name_plural = "Tipos de Solicitudes"
        
    def __str__(self):
        return self.nombre_t_sol
   
    
class Dato_Salida(models.Model):
    id_datos_sal = models.AutoField(primary_key=True)
    estado_sal = models.CharField(max_length=40)
    fecha_resol = models.DateTimeField()

    class Meta:
        verbose_name = "Dato de Salida"
        verbose_name_plural = "Datos de Salida"

class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True)
    nombre_sol = models.CharField(max_length=30, verbose_name = "Nombre")
    descripcion_sol = models.CharField(max_length=70, verbose_name = "Descripción")
    estado_sol = models.CharField(max_length=1, verbose_name = "Estado", default="s")
    adjunto = models.FileField(upload_to='archivos/', blank=True, null=True)
    notas = models.CharField(max_length=30)
    created_at = models.DateTimeField(verbose_name = "Fecha de Creación", auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name = "Usuario")
    id_tipo_sol = models.ForeignKey(Tipo_Solicitud, on_delete=models.CASCADE, verbose_name = "Tipo de Solicitud")
    id_datos_sal = models.OneToOneField(Dato_Salida, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
    
    def __str__(self):
        return self.nombre_sol
# Create your models here.
