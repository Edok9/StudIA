from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from clientManager.models import Empresa

class Tipo_Usuario(models.Model):
    id_t_usuario = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=25)
    estado_activacion = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=25)
    
    def __str__(self):
        return self.role


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_t_usuario = models.ForeignKey(Tipo_Usuario, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    
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