from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from clientManager.models import Empresa

class Tipo_Usuario(models.Model):
    id_t_usuario = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=25)
    estado_activacion = models.CharField(max_length=25, verbose_name = "Estado de Activación")
    descripcion = models.CharField(max_length=25, verbose_name = "Descripción")
    
    class Meta:
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuarios"
        
    def __str__(self):
        return self.rol


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25, verbose_name="Nombre de Usuario")
    email = models.EmailField(max_length=25)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField(verbose_name="Horario de Atención")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Ultimo Ingreso")
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    id_t_usuario = models.ForeignKey(Tipo_Usuario, on_delete=models.CASCADE, verbose_name="Tipo de Usuario")

    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    # Encriptado de contraseña al guardar en el panel de admin
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    # Funciones de caracteristicas de usuario
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
    def check_password(self, password):
        return check_password(password, self.password)
    
    def __str__(self):
        return self.nombre_usuario