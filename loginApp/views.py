from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from clientManager.models import Empresa
from .scripts.informe import gen_informe
from .scripts.formularios import procesar_form, revision_form
from loginApp.forms import CrearUsuarioForm, EditarUsuarioForm, CambioClaveAdminForm, ReporteriaForm, FiltrodeFormulariosForm, form_dict
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud
from django.http import JsonResponse
from datetime import date
import json 


@login_required
def nueva_solicitud(request):
    if request.method == "POST":
        usuario = request.user
        tipo_solicitud = request.POST.get("tipoSolicitud")
        
        # Trabajar con el diccionario de campos, excluyendo campos no necesarios
        campos_sol = {key: value for key, value in request.POST.items() if key not in ["csrfmiddlewaretoken", "tipoSolicitud"]}

        # Crear una nueva instancia de Solicitud sin guardarla aún
        nueva_solicitud = Solicitud(
            tipo_sol=tipo_solicitud,
            campos_sol=campos_sol,
            id_usuario=usuario
        )

        # Verificar si hay un archivo adjunto y guardarlo
        if 'adjunto' in request.FILES:
            nueva_solicitud.adjunto_sol = request.FILES['adjunto']
        
        # Guardar la nueva solicitud con todos los datos
        nueva_solicitud.save()

        return redirect("infoSolicitudes")
    else:
        return render(request, "nueva_solicitud.html")
    
@login_required    
def estado_solicitudes(request):
    search_term = request.GET.get('search', '').strip()
    if search_term:
        solicitudes = Solicitud.objects.filter(estado_sol__icontains=search_term) | Solicitud.objects.filter(tipo_sol__icontains=search_term)
    else:
        solicitudes = Solicitud.objects.all()
    
    return render(request, 'infoSolicitudes.html', {'solicitudes': solicitudes})

def solicitudes_empresa(request):
    return render(request,'solicitudes_empresa.html')

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
    usuario = request.user  
    form = None
    tipo_form = None
   
    empresa = request.tenant  
    casos_empresa = empresa.casos_disponibles if hasattr(empresa, 'casos_disponibles') else []

    if request.method == "POST":
        tipo_form = request.POST.get("tipo_sol")
        if tipo_form in form_dict:
            form_class = form_dict[tipo_form]
            form = form_class(request.POST, request.FILES) if request.FILES else form_class(request.POST)

            if form.is_valid():
                sol = Solicitud(tipo_sol=tipo_form, id_usuario=usuario)
                sol = procesar_form(form, sol)

                lista_sol = Solicitud.objects.filter(estado_sol="Pendiente", tipo_sol=tipo_form)
                if revision_form(sol, lista_sol):
                    sol.save()
                    messages.success(request, "Solicitud guardada con éxito")
                    return redirect("home")
                else:
                    messages.error(request, "Una solicitud similar existe en curso")
            else:
                messages.error(request, "Por favor corrija los errores en el formulario.")
        else:
            messages.error(request, "Tipo de solicitud no válido.")

    form_list = [f() for name, f in form_dict.items() if name in casos_empresa]

    context = {
        "formularios": form_list,
        "current_form": form,  # Pasar el formulario actual (puede ser None)
        "tipo_form": tipo_form,  # Ayuda a mantener seleccionado el formulario actual después de un POST fallido
    }
    return render(request, "home.html", context)


@login_required
def verSolicitud(request, pk):
    solicitud = Solicitud.objects.get(pk=pk)
    tipo_solicitud = solicitud.tipo_sol
    if tipo_solicitud in form_dict:
        form = form_dict[tipo_solicitud](initial=solicitud.campos_sol)
        campos_form = form.fields
        if "fecha_expiracion" in solicitud.campos_sol:
            # Arreglar de date a datetime para mostrarlo
            pass
        if solicitud.adjunto_sol:
            solicitud.campos_sol["adjunto"] = solicitud.adjunto_sol
        for c in campos_form:
            form.fields[c].widget.attrs['disabled'] = True
        return render(request, "infoSolicitud.html", {"solicitud": form})
        
    return redirect("infoSolicitudes")

@login_required
def estadoSolicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, "listaSolicitudes.html", {"solicitudes": solicitudes})

@login_required
def solicitudesUsuario(request):
    try:
        solicitudes = Solicitud.objects.all().filter(id_usuario = request.user.id_usuario)
        return render(request, "listaMisSolicitudes.html", {"solicitudes": solicitudes})
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
    sol = get_object_or_404(Solicitud, id_sol=pk)
    estados_posibles = ['Pendiente', 'En Proceso', 'Completo']  # Ejemplo de estados

    if request.method == "POST":
        # Obtener el estado de la solicitud del formulario
        estado_sol = request.POST.get('estado_sol')

        tipo_form = sol.tipo_sol  # Usar el tipo de solicitud ya existente
        if tipo_form in form_dict and estado_sol in estados_posibles:
            form_class = form_dict[tipo_form]
            form = form_class(request.POST, request.FILES, initial=sol.campos_sol)

            if form.is_valid():
                # Actualizar el estado de la solicitud con el nuevo valor
                sol.estado_sol = estado_sol

                # Procesar y actualizar la instancia de Solicitud con los nuevos datos del formulario
                sol = procesar_form(form, sol)
                lista_sol = Solicitud.objects.filter(estado_sol="Pendiente", tipo_sol=tipo_form).exclude(id_sol=pk)

                if revision_form(sol, lista_sol):
                    sol.save()
                    messages.success(request, "Solicitud actualizada con éxito")
                    return redirect("estadoSolicitudes")
                else:
                    messages.error(request, "Una solicitud similar existe en curso")
            else:
                messages.error(request, "Por favor corrija los errores en el formulario.")
        else:
            messages.error(request, "Tipo de solicitud no válido o estado de solicitud no válido.")
    else:
        # Prellenar el formulario con datos existentes de la solicitud, incluido su estado
        if sol.tipo_sol in form_dict:
            tipo_form = form_dict[sol.tipo_sol]
            form = tipo_form(initial=sol.campos_sol)

    context = {
        'formulario': form,
        'tipo_formulario': sol.tipo_sol,
        'estado_sol': sol.estado_sol,
        'estados_posibles': estados_posibles,
    }
    return render(request, "editarSolicitud.html", context)
    
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

 

