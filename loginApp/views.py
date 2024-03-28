from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from clientManager.models import Empresa
from .scripts.informe import gen_informe
from loginApp.forms import CrearUsuarioForm, EditarUsuarioForm, CambioClaveAdminForm, ReporteriaForm, FiltrodeFormulariosForm, form_dict
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud
from django.http import JsonResponse


def nueva_solicitud(request):
    if request.method == "POST":
        # Obtener el usuario actual
        usuario = request.user

        # Obtener el tipo de solicitud del formulario
        tipo_solicitud = request.POST.get("tipoSolicitud")

        # Crear un diccionario con los datos del formulario
        campos_sol = request.POST.dict()

        # Eliminar el tipo de solicitud del diccionario de campos_sol
        del campos_sol["tipoSolicitud"]

        # Eliminar el token CSRF del diccionario de campos_sol si está presente
        if "csrfmiddlewaretoken" in campos_sol:
            del campos_sol["csrfmiddlewaretoken"]

        # Crear una nueva instancia de Solicitud y guardarla en la base de datos
        nueva_solicitud = Solicitud.objects.create(
            tipo_sol=tipo_solicitud,
            campos_sol=campos_sol,
            id_usuario=usuario
        )

        # Redirigir a la página deseada después de guardar la solicitud
        return redirect("infoSolicitudes")

    else:
        return render(request, "nueva_solicitud.html")
    
def casos_de_uso(request):
    return render(request,'casos_de_uso.html')

def entel(request):
    return render(request,'entel.html')

def estado(request):
    return render(request,'estado.html')

def pruebas(request):
    return render(request,'pruebas.html')


def solicitudes(request):
    return render(request,'solicitudes.html')

def administrar(request):
    return render(request,'administrar.html')


def index(request):
    if request.user.is_authenticated:
        return redirect("solicitudes")
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
        if sol.tipo_sol in form_dict:
            tipo_form = form_dict[sol.tipo_sol]
            form = tipo_form(request.POST, request.FILES) if request.FILES else tipo_form(request.POST)
            submit_caso_form(form, sol)
        else:
            return redirect("home")
    empresa = Empresa.objects.get(pk=request.tenant.id_empresa)
    casos_empresa = empresa.casos_disponibles
    form_list = [f for n,f in form_dict.items() if n in casos_empresa]
    return render(request, "home.html", {"formularios": form_list})

@login_required
def verSolicitud(request, pk):
    solicitud = Solicitud.objects.get(pk=pk)
    tipo_solicitud = solicitud.tipo_sol
    if tipo_solicitud in form_dict:
        form = form_dict[tipo_solicitud](initial=solicitud.campos_sol)
        campos_form = form.fields
        if solicitud.adjunto_sol:
            solicitud.campos_sol["adjunto"] = solicitud.adjunto_sol
        for c in campos_form:
            form.fields[c].widget.attrs['disabled'] = True
        return render(request, "infoSolicitud.html", {"solicitud": form})
        
    return redirect("infoSolicitudes")

@login_required
def infoSolicitudes(request):
    try:
        solicitudes = Solicitud.objects.all().filter(id_usuario = request.user.id_usuario)
        return render(request, "listaSolicitudes.html", {"solicitudes": solicitudes})
    except Solicitud.DoesNotExist:
        return redirect('home')
    
#HAY QUE QUITAR ESTO, ESTA ES MEDIDA TEMPORAL E IMPLEMENTARLA EN CODE DE SEBA

    
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
    return render(request, "administrar.html", datos)

@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def crearUsuario(request):
    form = CrearUsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        empresa = Empresa.objects.get(pk=request.tenant.id_empresa)
        usuario = form.save(commit=False)
        usuario.id_empresa = empresa
        usuario.set_password(usuario.password)
        usuario.save()
        return redirect("usuarios")
    solicitudes = Solicitud.objects.filter(id_usuario = request.user.id_usuario)
    datos_solicitudes = {"solicitudes": solicitudes,
                         "formulario": form}
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
    form = CambioClaveAdminForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            usuario = Usuario.objects.get(id_usuario = pk)
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            usuario.set_password(nueva_contraseña)
            usuario.save()
            update_session_auth_hash(request, usuario)
            return redirect('usuarios')
    try:
        usuario = Usuario.objects.get(id_usuario = pk)
        data = {"usuario": usuario,
                "formulario": form}
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
        sol = Solicitud.objects.get(id_sol = pk)
        form = request.POST
        if form["tipo_solicitud"] in form_dict:
            tipo_form = form_dict[sol.tipo_sol]
            form = tipo_form(request.POST, request.FILES) if request.FILES else tipo_form(request.POST)
            submit_caso_form(form, sol)
        return redirect("estadoSolicitudes")
    try:
        sol = Solicitud.objects.get(id_sol = pk)
        if(sol.adjunto_sol):
            sol.campos_sol["adjunto"] = sol.adjunto_sol
        if sol.tipo_sol in form_dict:
            tipo_form = form_dict[sol.tipo_sol]
            form = tipo_form(initial=sol.campos_sol)
        else:
            return redirect("home")
        datos = {
            "formulario": form,
            "tipo_formulario": sol.tipo_sol
        }
        return render(request, "editarSolicitud.html", datos)
    except Solicitud.DoesNotExist:
        return redirect("estadoSolicitudes")
    
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def casosDeUso(request):
    empresa = Empresa.objects.get(pk=request.tenant.id_empresa)
    if request.method == "POST":
        data = request.POST.getlist("lista_formularios")
        empresa.casos_disponibles = data
        empresa.save()
        return redirect("casosDeUso")
    casos_empresa = empresa.casos_disponibles
    form = FiltrodeFormulariosForm(initial={"lista_formularios": casos_empresa})
    return render(request, "listaCasosdeUso.html", {"formulario": form})
     
@staff_member_required(redirect_field_name=None, login_url=reverse_lazy("home"))
def reportes(request):
    if request.method == "POST":
        form = request.POST
        response = HttpResponse()
        periodo = form["periodo_reportes"]
        formato = form["formato_reportes"]
        if formato == "pdf":
            response['Content-Disposition'] = "attachment; filename=reporte.pdf"
        else:
            response['Content-Disposition'] = "attachment; filename=reporte.csv"
        gen_informe(periodo, response, formato)
        return response
    
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
