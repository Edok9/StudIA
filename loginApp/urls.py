from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('unauthorized', views.unauthorized, name='unauthorized'),
    path('logged', views.logged, name='logged')
]