from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from loginApp.models import Usuario

def casos_de_uso(request):
    return render(request,'casos_de_uso.html')

def entel(request):
    return render(request,'entel.html')

def estado(request):
    return render(request,'estado.html')

def pruebas(request):
    return render(request,'pruebas.html')

def reporteria(request):
    return render(request,'reporteria.html')

def solicitudes(request):
    return render(request,'solicitudes.html')

def administrar(request):
    return render(request,'administrar.html')


def index(request):
    if request.method == "POST":
        email = request.POST["email"]
        clave = request.POST["clave"]
        error_email = "Email no encontrado"
        error_clave = "Contraseña incorrecta"
        errores = {}
        usuario = authenticate(request, email=email, clave=clave)
        if usuario is not None:
            login(request, usuario)
            return redirect("logged")
        else:
            try:
                user = Usuario.objects.get(email=email)
                errores["errorClave"] = error_clave
            except Usuario.DoesNotExist:
                errores["errorEmail"] = error_email
            return render(request, "login.html", errores)
    else:
        return render(request, "login.html")

def logged(request):
    if request.user.is_authenticated: # Check de la cookie llamada sessionid para ver si hay un usuario ingresado
        return render(request, "correct_login.html")
    else:
        return redirect("unauthorized")

def unauthorized(request):
    return render(request, "unauthorized.html")

# Create your views here.
