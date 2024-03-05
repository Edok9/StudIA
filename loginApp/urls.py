from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.nuevoUsuario, name='nuevoUsuario'),
    path('solicitud/<int:pk>', views.infoSolicitud, name="infoSolicitud"),
    path('test', views.test, name='test'),
]