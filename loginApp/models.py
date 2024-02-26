from django.contrib.auth.hashers import make_password
from django.db import models
from clientManager.models import Empresa

class Tipo_Usuario(models.Model):
    id_t_usuario = models.AutoField(primary_key=True)
    role = models.CharField(max_length=25)
    estado_activacion = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=25)


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField()
    password = models.CharField(max_length=25)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_t_usuario = models.ForeignKey(Tipo_Usuario, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        self.clave = make_password(self.clave)
        super().save(*args, **kwargs)
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def __str__(self):
        return self.nombre_usuario