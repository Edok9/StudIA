from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from clientManager.models import Empresa
from loginApp.forms import CrearUsuarioForm, EditarUsuarioForm, CambioClaveAdminForm
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud


def index(request):
    if request.user.is_authenticated:
        return redirect("home")
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

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def usuarios(request):
    solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
    usuarios = Usuario.objects.all().order_by('id_usuario')
    datos = {"solicitudes": solicitudes,
             "usuarios": usuarios}
    return render(request, "listaUsuarios.html", datos)

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def crearUsuario(request):
    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            empresa = Empresa.objects.get(pk=request.tenant.id_empresa)
            usuario = form.save(commit=False)
            usuario.id_empresa = empresa
            usuario.set_password(usuario.password)
            usuario.save()
            return redirect("usuarios")
    solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
    formulario = CrearUsuarioForm()
    datos_solicitudes = {"solicitudes": solicitudes,
                         "formulario": formulario}
    return render(request, "crearUsuario.html", datos_solicitudes)

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def editarUsuario(request, pk):
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST)
        if form.is_valid():
            datos_formulario = form.cleaned_data
            Usuario.objects.filter(id_usuario = pk).update(**datos_formulario)
            return redirect("usuarios")
    try:
        usuario = Usuario.objects.get(id_usuario = pk)
        formulario = EditarUsuarioForm(instance=usuario)
        return render(request, "editarUsuario.html", {"formulario": formulario})
    except Usuario.DoesNotExist:
        return redirect("usuarios")        

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def editarClaveAdmin(request, pk):
    if request.method == "POST":
        form = CambioClaveAdminForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.get(id_usuario = pk)
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            usuario.set_password(nueva_contraseña)
            usuario.save()
            print(usuario.check_password(nueva_contraseña))
            update_session_auth_hash(request, usuario)
            return redirect('usuarios')
    try:
        usuario = Usuario.objects.get(id_usuario = pk)
        formulario = CambioClaveAdminForm()
        data = {"usuario": usuario,
                "formulario": formulario}
        return render(request, "editarClaveAdmin.html", data)
    except Usuario.DoesNotExist:
        return redirect("usuarios") 

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def borrarUsuario(request, pk):
    pass

def logoutProcess(request):
    logout(request)
    return render(request, "logout.html")

# Create your views here.
