from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from clientManager.models import Empresa
from loginApp.forms import CrearUsuarioForm, EditarUsuarioForm, CambioClaveAdminForm, CasoDeUsoForm, ReporteriaForm
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud, Tipo_Solicitud


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
    return render(request, "home.html")

@login_required
def infoSolicitudes(request):
    try:
        solicitudes = Solicitud.objects.all().filter(id_usuario = request.user.id_usuario)
        return render(request, "listaSolicitudes.html", {"solicitudes": solicitudes})
    except Solicitud.DoesNotExist:
        return redirect('home')
    
@login_required
def borrarSolicitud(request, pk):
    solicitud = Solicitud.objects.get(id_sol = pk)
    solicitud.delete()
    return redirect("estadoSolicitudes")

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def usuarios(request):
    solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
    usuarios = Usuario.objects.all().order_by('id_usuario')
    datos = {"solicitudes": solicitudes,
             "usuarios": usuarios}
    return render(request, "listaUsuarios.html", datos)

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def casosDeUso(request):
    casos = Tipo_Solicitud.objects.all().order_by('id_tipo_sol')
    return render(request, "listaCasosDeUso.html", {"casos": casos})

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
def crearCaso(request):
    if request.method == "POST":
        form = CasoDeUsoForm(request.POST)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.save()
            return redirect("casosDeUso")
    formulario = CasoDeUsoForm()
    return render(request, "crearCasoDeUso.html", {"formulario": formulario})

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
def editarCaso(request, pk):
    if request.method == "POST":
        form = CasoDeUsoForm(request.POST)
        if form.is_valid():
            datos_formulario = form.cleaned_data
            Tipo_Solicitud.objects.filter(id_tipo_sol = pk).update(**datos_formulario)
            return redirect("casosDeUso")
    try:
        caso = Tipo_Solicitud.objects.get(id_tipo_sol = pk)
        formulario = CasoDeUsoForm(instance=caso)
        return render(request, "editarCasodeUso.html", {"formulario": formulario})
    except Tipo_Solicitud.DoesNotExist:
        return redirect("casosDeUso")
    
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def editarClaveAdmin(request, pk):
    if request.method == "POST":
        form = CambioClaveAdminForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.get(id_usuario = pk)
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            usuario.set_password(nueva_contraseña)
            usuario.save()
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
    usuario = Usuario.objects.get(id_usuario = pk)
    
    # Impedir que el usuario se elimine a si mismo a la fuerza
    if request.user.id_usuario == usuario.id_usuario:
        return redirect("usuarios")
    
    usuario.delete()
    return redirect("usuarios")

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def borrarCaso(request, pk):
    caso = Tipo_Solicitud.objects.get(id_tipo_sol = pk)
    caso.delete()
    return redirect("casosDeUso")

'''
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def editarSolicitud(request, pk):
    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            datos_formulario = form.cleaned_data
            Por alguna razon si actualizo sin esto, se borra los datos del campo "adjunto"
            Pero no creo que sea necesario modificar este campo por parte del admin
            Igual lo dejo en caso que sea necesario
            if not request.FILES:
                solicitud = Solicitud.objects.get(id_sol = pk)
                datos_formulario["adjunto"] = solicitud.adjunto
            Solicitud.objects.filter(id_sol = pk).update(**datos_formulario)
            return redirect("estadoSolicitudes")
    try:
        solicitud = Solicitud.objects.get(id_sol = pk)
        formulario = SolicitudForm(instance=solicitud)
        return render(request, "editarSolicitud.html", {"formulario": formulario})
    except Solicitud.DoesNotExist:
        return redirect("estadoSolicitudes")     
'''
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def reportes(request):
    if request.method == "POST":
        form = request.POST
        print(form)
        return redirect("reporteria")
    
    formulario = ReporteriaForm()
    return render(request, "reporteria.html", {"formulario":formulario})

def logoutProcess(request):
    logout(request)
    return render(request, "logout.html")

# Create your views here.
