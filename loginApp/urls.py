from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    # URLs para usuarios
    path('solicitud/<int:pk>', views.infoSolicitud, name="infoSolicitud"),
    
    
    # URLs para admins
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.crearUsuario, name='crearUsuario'),
    path('editar/usuario/<int:pk>', views.editarUsuario, name="editarUsuario"),
    path('editar/clave/<int:pk>', views.editarClaveAdmin, name='editarClaveAdmin'),
    path('borrar/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
]