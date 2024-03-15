import csv
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud

def gen_informe():
    '''
    uhhh, de alguna manera recibir los parametros del formulario
    es un diccionario, deberia de pedir los campos en la funcion nomas
    luego pasar a filtrar
    uno es la fecha de las solicitudes
    otra es de obtener los usuarios (si/no)
    de primeras sacar solo el csv
    luego intentar implementar con pdf
    seguramente se filtrara por formato, si es un csv o un pdf
    investigar como trabajar con multiples archivos... zip? puede ser
    ay caramba
    '''
    pass

def to_csv():
    pass

def to_pdf():
    pass