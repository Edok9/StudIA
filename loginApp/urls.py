from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    # URLs para usuarios
    path('solicitudes', views.infoSolicitudes, name="solicitudes"),
    path('estadoSolicitudes', views.infoSolicitudes, name="estadoSolicitudes"),
    path('infoSolicitudes', views.infoSolicitudes, name="infoSolicitudes"),
    
    
    # URLs para admins
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.crearUsuario, name='crearUsuario'),
    path('editar/usuario/<int:pk>', views.editarUsuario, name="editarUsuario"),
    path('editar/clave/<int:pk>', views.editarClaveAdmin, name='editarClaveAdmin'),
    path('borrar/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.crearUsuario, name='nuevoUsuario'),
    path('solicitud/<int:pk>', views.infoSolicitudes, name="infoSolicitud"),
    path('casos_de_uso/', casos_de_uso, name='casos_de_uso'),
    path('entel/', entel, name='entel'),
    path('estado/', estado, name='estado'),
    path('pruebas/', pruebas, name='pruebas'),
    path('reporteria/', reporteria, name='reporteria'),
    path('solicitudes/', solicitudes, name='solicitudes'),
    path('administrar/', administrar, name='administrar'),
]