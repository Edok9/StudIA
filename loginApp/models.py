from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from clientManager.models import Empresa

class UsuarioManager(BaseUserManager):
    def _create_user(self, usuario, email, clave, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(nombre_usuario=usuario, email=email, **extra_fields)
        user.set_password(clave)
        user.save(using=self._db)
        return user
    
    def create_user(self, nombre=None, email=None, clave=None, **extra_fields):
        return self._create_user(self, nombre, email, clave, **extra_fields)
    
    def create_superuser(self, nombre=None, email=None, clave=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(self, nombre, email, clave, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_usuario = models.CharField(max_length=25, verbose_name="Nombre de Usuario")
    email = models.EmailField(max_length=25, unique=True)
    telefono = models.IntegerField()
    cargo = models.CharField(max_length=25)
    horario_atencion = models.IntegerField(verbose_name="Horario de Atención")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Ultimo Ingreso")
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    
    is_active=models.BooleanField(default=True, verbose_name="Cuenta activada")
    is_staff=models.BooleanField(default=False, verbose_name="Cuenta de administrador")
    is_superuser=models.BooleanField(default=False, verbose_name="Cuenta de superusuario")

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
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