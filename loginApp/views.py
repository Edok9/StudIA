from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud


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
            # Parche para redirecciones del decorador login_required, revisar si hay una mejor solucion
            next_url = request.GET.get('next', '')
            if next_url:
                return HttpResponse(status=302, headers={'Location': next_url})
            else:
                return redirect("home")
        else:
            try:
                user = Usuario.objects.get(email=email)
                errores["errorClave"] = error_clave
            except Usuario.DoesNotExist:
                errores["errorEmail"] = error_email
            return render(request, "login.html", errores)
    else:
        return render(request, "login.html")

@login_required
def home(request):
    solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
    datos_solicitudes = {"solicitudes": solicitudes}
    return render(request, "home.html", datos_solicitudes)

@login_required
def infoSolicitud(request, pk):
    try:
        solicitud = Solicitud.objects.get(id_sol = pk, id_usuario = request.user.id_usuario)
        solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
        datos_solicitudes = {
            "solicitudes": solicitudes,
            "solicitudUsuario": solicitud
            }
        return render(request, "infoSolicitud.html", datos_solicitudes)
    except Solicitud.DoesNotExist:
        return redirect('home')

@login_required
def test(request):
    return render(request, "test.html")

def logoutProcess(request):
    logout(request)
    return render(request, "logout.html")

# Create your views here.
