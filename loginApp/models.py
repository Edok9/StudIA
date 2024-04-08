from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def _create_user(self, nombre_usuario, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta ingresar el email')
    
        email = self.normalize_email(email)
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, nombre_usuario, email=None, password=None, **extra_fields):
        return self._create_user(nombre_usuario, email, password, **extra_fields)
    
    def create_superuser(self, nombre_usuario, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        return self._create_user(nombre_usuario, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25, verbose_name="Nombre de Usuario")
    email = models.EmailField(max_length=25, unique=True)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField(verbose_name="Horario de Atención")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    last_login = models.DateTimeField(null=True, verbose_name="Ultimo Ingreso")
    is_active=models.BooleanField(default=True, verbose_name="Cuenta activada")
    is_staff=models.BooleanField(default=False, verbose_name="Cuenta de administrador")

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['nombre_usuario', 'telefono', 'cargo', 'horario_atencion']
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    # Funciones de caracteristicas de usuario
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def check_password(self, password):
        return check_password(password, self.password)
    
    def __str__(self):
        return self.nombre_usuario
    