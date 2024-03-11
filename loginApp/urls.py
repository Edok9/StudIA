from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
<<<<<<< HEAD
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.nuevoUsuario, name='nuevoUsuario'),
    path('solicitud/<int:pk>', views.infoSolicitud, name="infoSolicitud"),
    path('test/', test, name='test'),
    path('casos_de_uso/', casos_de_uso, name='casos_de_uso'),
    path('entel/', entel, name='entel'),
    path('estado/', estado, name='estado'),
    path('pruebas/', pruebas, name='pruebas'),
    path('reporteria/', reporteria, name='reporteria'),
    path('solicitudes/', solicitudes, name='solicitudes'),
    path('administrar/', administrar, name='administrar'),
    path('unauthorized', views.unauthorized, name='unauthorized'),
    path('logged', views.logged, name='logged')
=======
    # URLs para usuarios
    path('solicitud/<int:pk>', views.infoSolicitud, name="infoSolicitud"),
    
    
    # URLs para admins
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.crearUsuario, name='crearUsuario'),
    path('editar/usuario/<int:pk>', views.editarUsuario, name="editarUsuario"),
    path('editar/clave/<int:pk>', views.editarClaveAdmin, name='editarClaveAdmin'),
    path('borrar/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
>>>>>>> 5ee82f78e9c3f227e4f23b3fd8f58adbee15fe32
]