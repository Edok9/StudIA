from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    # URLs para usuarios
    path('solicitud/<int:pk>', views.verSolicitud, name="verSolicitud"),
    path('solicitudes', views.estadoSolicitudes, name="estadoSolicitudes"),
    path('mis-solicitudes', views.solicitudesUsuario, name="infoSolicitudes"),
    path('borrarsolicitud/<int:pk>', views.borrarSolicitud, name="borrarSolicitud"),
    
    
    # URLs para admins
    path('usuarios', views.usuarios, name='usuarios'),
    path('casos', views.casosDeUso, name='casosDeUso'),
    path('crear/usuario', views.crearUsuario, name='crearUsuario'),
    path('editar/usuario/<int:pk>', views.editarUsuario, name="editarUsuario"),
    path('editar/solicitud/<int:pk>', views.editarSolicitud, name="editarSolicitud"),
    path('editar/clave/<int:pk>', views.editarClaveAdmin, name='editarClaveAdmin'),
    path('borrarusuario/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
    path('reportes', views.reportes, name='reporteria'),
]