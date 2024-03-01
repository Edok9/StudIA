from django.db import models
from loginApp.models import Usuario
    
class Tipo_Solicitud(models.Model):
    id_tipo_sol = models.AutoField(primary_key=True)
    descripcion_t_sol = models.CharField(max_length=70, verbose_name = "Descripción")
    nombre_t_sol = models.CharField(max_length=25, verbose_name = "Nombre")
    estado_sol = models.CharField(max_length=1, verbose_name = "Estado")

    class Meta:
        verbose_name = "Tipo de Solicitud"
        verbose_name_plural = "Tipos de Solicitudes"
        
    def __str__(self):
        return self.nombre_t_sol
   
class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True)
    nombre_sol = models.CharField(max_length=30, verbose_name = "Nombre")
    tipo_sol = models.CharField(max_length=30, verbose_name = "Tipo")
    descripcion_sol = models.CharField(max_length=70, verbose_name = "Descripción")
    created_at = models.DateTimeField(verbose_name = "Fecha de Creación")
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name = "Usuario")
    id_tipo_sol = models.ForeignKey(Tipo_Solicitud, on_delete=models.CASCADE, verbose_name = "Tipo de Solicitud")

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
    
    def __str__(self):
        return self.nombre_sol
    
class Dato_Entrada(models.Model):
    id_datos_ent = models.AutoField(primary_key=True)
    email_usuario = models.CharField(max_length=30)
    nombre_cuenta = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    adjunto = models.FileField(upload_to='archivos/')
    notas = models.CharField(max_length=30)
    id_tipo_sol = models.OneToOneField(Tipo_Solicitud, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Dato de Entrada"
        verbose_name_plural = "Datos de Entrada"
    
class Dato_Salida(models.Model):
    id_datos_sal = models.AutoField(primary_key=True)
    estado_sal = models.CharField(max_length=40)
    fecha_resol = models.DateTimeField()
    id_tipo_sol = models.OneToOneField(Tipo_Solicitud, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Dato de Salida"
        verbose_name_plural = "Datos de Salida"

# Create your models here.
