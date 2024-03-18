from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from clientManager.models import Empresa
from loginApp.forms import CrearUsuarioForm, EditarUsuarioForm, CambioClaveAdminForm, ReporteriaForm, Ise_Vpn_Form, Ioc_Automatico_Form, Cambio_De_Ruta_Form
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud

formList = (
    Ise_Vpn_Form(),
    Ioc_Automatico_Form(),
    Cambio_De_Ruta_Form(),
)

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
    if request.method == "POST":
        sol = Solicitud()
        usuario = Usuario.objects.get(pk=request.user.id_usuario)
        sol.tipo_sol = request.POST["tipo_sol"]
        sol.id_usuario = usuario
        match sol.tipo_sol:
            case "Servicio VPN":
                form = Ise_Vpn_Form(request.POST)
                submit_caso_form(form, sol)
            case "IOC Automatico":
                form = Ioc_Automatico_Form(request.POST, request.FILES)
                submit_caso_form(form, sol)
            case "Cambio de Ruta":
                form = Cambio_De_Ruta_Form(request.POST)
                submit_caso_form(form, sol)
            case _:
                return redirect("home")
    return render(request, "home.html", {"formularios": formList})

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
def editarSolicitud(request, pk):
    if request.method == "POST":
        form = request.POST
        match form["tipo_solicitud"]:
            case "Servicio VPN":
                form = Ise_Vpn_Form(request.POST)
            case "IOC Automatico":
                form = Ioc_Automatico_Form(request.POST, request.FILES)
            case "Cambio de Ruta":
                form = Cambio_De_Ruta_Form(request.POST)
            case _:
                return redirect("estadoSolicitudes")
        if form.is_valid():
            form = form.cleaned_data
            Solicitud.objects.filter(id_sol = pk).update(campos_sol = form)
        return redirect("estadoSolicitudes")
    try:
        solicitud = Solicitud.objects.get(id_sol = pk)
        match solicitud.tipo_sol:
            case "Servicio VPN":
                formulario = Ise_Vpn_Form(initial=solicitud.campos_sol)
            case "IOC Automatico":
                formulario = Ioc_Automatico_Form(initial=solicitud.campos_sol)
            case "Cambio de Ruta":
                formulario = Cambio_De_Ruta_Form(initial=solicitud.campos_sol)  
            case _:
                return redirect("home")
        datos = {
            "formulario": formulario,
            "tipo_formulario": solicitud.tipo_sol
        }
        return render(request, "editarSolicitud.html", datos)
    except Solicitud.DoesNotExist:
        return redirect("estadoSolicitudes") 
     
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def reportes(request):
    if request.method == "POST":
        form = request.POST
        return redirect("reporteria")
    
    formulario = ReporteriaForm()
    return render(request, "reporteria.html", {"formulario":formulario})

def logoutProcess(request):
    logout(request)
    return render(request, "logout.html")

# Create your views here.

def submit_caso_form(form, sol):
    if form.is_valid():
        sol.campos_sol = form.cleaned_data
        if form.files:
            sol.adjunto_sol = form.files[f'{sol.tipo_sol}-adjunto']
            del(sol.campos_sol["adjunto"])
        sol.save()
        return redirect("home")
