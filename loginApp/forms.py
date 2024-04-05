from django import forms
from .models import Usuario
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

design = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"


class CambioClaveUsuarioForm(forms.Form):
    pass

class ReporteriaForm(forms.Form):
    opciones = (
        ("24h", "24 Horas" ),
        ("7d", "7 Días"),
        ("1m", "1 Mes"),
    )
    formatos = (
        ("csv", "CSV"),
        ("pdf", "PDF"),
    )
    periodo_reportes = forms.ChoiceField(choices=opciones, label="Periodo de Reportes")
    formato_reportes = forms.ChoiceField(choices=formatos, label="Formato de los Reportes")

class Ise_Vpn_Form(forms.Form):
    acciones = (
        ("Nada", "------"),
        ("Extension de cuenta", "Extension de cuenta"),
        ("Cambio de contraseña", "Cambio de contraseña"),
        ("Deshabilitación de cuenta", "Deshabilitación de cuenta"),
    )
    accion = forms.ChoiceField(choices=acciones, label="Accion", widget=forms.Select(attrs={'class': 'form-select'}))
    usuario = forms.CharField(label="Usuario de VPN", widget=forms.TextInput(attrs={'class': 'form-input'}))
    correo_usuario = forms.EmailField(label="Correo del Usuario", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    fecha_expiracion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}), label="Fecha de Expiración", required=False)

    prefix = "Servicio VPN"
    
    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        # Validación específica para el campo usuario
        if not re.match(r'^[a-zA-Z]{3,}$', usuario):
            raise ValidationError(_('El usuario debe contener al menos 3 letras y no números.'))
        return usuario

    def clean_correo_usuario(self):
        correo_usuario = self.cleaned_data['correo_usuario']
        # Aquí podrías añadir tu validación específica para el correo
        if not re.match(r'^\S+@\S+\.\S+$', correo_usuario):
            raise ValidationError(_('Por favor, ingrese una dirección de correo válida. Ej: Nombre@example.com'))
        return correo_usuario

    def clean_fecha_expiracion(self):
        fecha_expiracion = self.cleaned_data.get('fecha_expiracion')
        if fecha_expiracion and fecha_expiracion <= date.today():
            raise ValidationError(_('La fecha debe ser a partir del siguiente día en adelante.'))
        return fecha_expiracion

class Ioc_Automatico_Form(forms.Form):
    adjunto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}))
    notas = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4}))

    prefix = "IOC Automatico"
    
    def clean_notas(self):
        notas = self.cleaned_data['notas']
        if not notas.strip():
            raise ValidationError(_('Este campo no puede estar vacío.'))
        return notas

class Cambio_De_Ruta_Form(forms.Form):
<<<<<<< HEAD
    gateway = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    interfaz_salida = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
=======
    opciones_id_ruta = (
        ("","Ninguno"),
        ("PORT","PORT"),
        ("VLAN","VLAN"),
    )
    gateway = forms.CharField(label="Gateway")
    interfaz_salida = forms.CharField(label="Interfaz de Salida")
    prefijo_id_ruta = forms.ChoiceField(choices = opciones_id_ruta, label="Prefijo de ID de Ruta", required=False)
    id_ruta = forms.CharField(label="ID de Ruta")
>>>>>>> d5da5d1797be83d0f596e664be5b519b7553cee6

    prefix = "Cambio de Ruta"

    def clean_gateway(self):
        gateway = self.cleaned_data.get('gateway')
        if not self.validar_direccion_ip(gateway):
            raise ValidationError("Ingrese una dirección IP válida para el gateway.")
        return gateway

    def clean_interfaz_salida(self):
        interfaz_salida = self.cleaned_data.get('interfaz_salida')
        if not self.validar_direccion_ip(interfaz_salida):
            raise ValidationError("Ingrese una dirección IP válida para la interfaz de salida.")
        return interfaz_salida

    def validar_direccion_ip(self, ip):
        # Regex para validar una dirección IPv4
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if ip_pattern.match(ip):
            octetos = ip.split('.')
            return all(0 <= int(octeto) <= 255 for octeto in octetos)
        return False
        
# Cambiar el resto de cosas para usar el diccionario si queda mas comodo de trabajar
form_dict = {
    Ise_Vpn_Form().prefix: Ise_Vpn_Form,
    Ioc_Automatico_Form().prefix: Ioc_Automatico_Form,
    Cambio_De_Ruta_Form().prefix: Cambio_De_Ruta_Form
}

class FiltrodeFormulariosForm(forms.Form):
    opciones = [(k,k) for k in form_dict.keys()]
    lista_formularios = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=opciones)

class CambioClaveAdminForm(forms.Form):
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": design}), min_length=6)
    confirmar_nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": design}))

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_nueva_contraseña = cleaned_data.get("confirmar_nueva_contraseña")

        if nueva_contraseña and confirmar_nueva_contraseña and nueva_contraseña != confirmar_nueva_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Verificar la complejidad de la nueva contraseña
        if nueva_contraseña and not self.validar_contraseña(nueva_contraseña):
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres, incluyendo al menos 2 números, una mayúscula y un punto.")

    def validar_contraseña(self, contraseña):
        # Longitud mínima de 6 caracteres
        if len(contraseña) < 6:
            return False
        # Al menos 2 números
        if sum(c.isdigit() for c in contraseña) < 2:
            return False
        # Al menos una mayúscula
        if not any(c.isupper() for c in contraseña):
            return False
        # Al menos un punto
        if '.' not in contraseña:
            return False
        return True

class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "nombre_usuario",
            "email",
            "password",
            "telefono",
            "cargo",
            "horario_atencion",
            "is_staff"
        ]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"class": "design", "id": "id_nombre_usuario"}),
            "email": forms.EmailInput(attrs={"class": "design", "id": "id_email"}),
            "password": forms.PasswordInput(attrs={"class": "design", "id": "id_password"}),
            "telefono": forms.TextInput(attrs={"class": "design", "id": "id_telefono"}),
            "cargo": forms.TextInput(attrs={"class": "design", "id": "id_cargo"}),
            "horario_atencion": forms.TextInput(attrs={"class": "design", "id": "id_horario_atencion"}),
        }

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "nombre_usuario",
            "telefono",
            "cargo",
            "horario_atencion",
            "is_active",
            "is_staff"
        ]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"id": "id_nombre", "class": "form-control"}),
            "telefono": forms.TextInput(attrs={"id": "id_telefono", "class": "form-control"}),
            "cargo": forms.TextInput(attrs={"id": "id_cargo", "class": "form-control"}),
            "horario_atencion": forms.TextInput(attrs={"id": "id_horario_atencion", "class": "form-control"}),
        }