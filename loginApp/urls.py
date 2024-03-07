from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
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
]