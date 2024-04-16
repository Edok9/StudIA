from django import forms
from .models import Usuario
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

design = "w-100 mb-2 p-2 border border-1"


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
    accion = forms.ChoiceField(choices=acciones, label="Accion",
                               widget=forms.Select(attrs={'class': f"form-select {design}"}))

    usuario = forms.CharField(label="Usuario de VPN",
                              widget=forms.TextInput(attrs={"class": f"form-control {design}"}))

    correo_usuario = forms.EmailField(label="Correo del Usuario",
                                      widget=forms.EmailInput(attrs={"class": f"form-control {design}"}))

    fecha_expiracion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class": f"form-control {design}"}),
                                       label="Fecha de Expiración", required=False)

    prefix = "Servicio VPN"
    
    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if not re.match(r'^[a-zA-Z]{3,}$', usuario):
            raise ValidationError(_('El usuario debe contener al menos 3 letras y no números.'))
        return usuario

    def clean_correo_usuario(self):
        correo_usuario = self.cleaned_data['correo_usuario']
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
    notas = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input', 
        'rows': 4, 
        'placeholder': 'Ingrese detalle de su solicitud...'
    }))

    prefix = "IOC Automatico"
    
    def clean_notas(self):
        notas = self.cleaned_data['notas']
        if not notas.strip():
            raise ValidationError(_('Este campo no puede estar vacío.'))
        return notas

class Cambio_De_Ruta_Form(forms.Form):
    opciones_id_ruta = (
        ("", "Ninguno"),
        ("PORT", "PORT"),
        ("VLAN", "VLAN"),
    )
    gateway = forms.CharField(
        label="Gateway",
        widget=forms.TextInput(attrs={'class': f"form-control {design}", 'placeholder': 'Ej. 192.168.1.1'}),
        required=True
    )
    prefijo_interfaz = forms.ChoiceField(
        choices=opciones_id_ruta,
        label="Prefijo de Interfaz de Salida",
        widget=forms.Select(attrs={'class': f"form-select {design}"}),
        required=False
    )
    interfaz_salida = forms.CharField(
        label="Interfaz de Salida",
        widget=forms.TextInput(attrs={'class': f"form-control {design}", 'placeholder': 'Ej. 5'}),
        required=True
    )
    ids_ruta = forms.CharField(
        label="IDs de Ruta",
        widget=forms.TextInput(attrs={'class': f"form-control {design}", 'placeholder': 'Ej. 12, 34, 56'}),
        required=False
    )

    prefix = "Cambio de Ruta"
    
    def clean_id_ruta(self):
        id_ruta = self.cleaned_data.get('id_ruta')
        return str(id_ruta) if id_ruta is not None else id_ruta

    def clean_gateway(self):
        gateway = self.cleaned_data.get('gateway')
        if not self.validar_direccion_ip(gateway):
            raise ValidationError("Ingrese una dirección IP válida para el gateway.")
        return gateway

    def clean_interfaz_salida(self):
        interfaz_salida = self.cleaned_data.get('interfaz_salida')
        if not interfaz_salida.strip():
            raise ValidationError("Este campo no puede estar vacío.")
        return interfaz_salida

    def validar_direccion_ip(self, ip):
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if ip_pattern.match(ip):
            octetos = ip.split('.')
            return all(0 <= int(octeto) <= 255 for octeto in octetos)
        return False
        
form_dict = {
    Ise_Vpn_Form().prefix: Ise_Vpn_Form,
    Ioc_Automatico_Form().prefix: Ioc_Automatico_Form,
    Cambio_De_Ruta_Form().prefix: Cambio_De_Ruta_Form
}

class FiltrodeFormulariosForm(forms.Form):
    opciones = [(k,k) for k in form_dict.keys()]
    lista_formularios = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=opciones)

class CambioClaveAdminForm(forms.Form):
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": f"form-control {design}"}), min_length=6)
    confirmar_nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": f"form-control {design}"}))

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_nueva_contraseña = cleaned_data.get("confirmar_nueva_contraseña")

        if nueva_contraseña and confirmar_nueva_contraseña and nueva_contraseña != confirmar_nueva_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if nueva_contraseña and not self.validar_contraseña(nueva_contraseña):
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres, incluyendo al menos 2 números, una mayúscula y un punto.")

    def validar_contraseña(self, contraseña):
        if len(contraseña) < 6:
            return False
        if sum(c.isdigit() for c in contraseña) < 2:
            return False
        if not any(c.isupper() for c in contraseña):
            return False
        if '.' not in contraseña:
            return False
        return True

class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_usuario", "email", "password", "telefono", "cargo", "horario_atencion", "is_staff"]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"class": "form-control", "id": "id_nombre_usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "id_email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "id": "id_password"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "id": "id_telefono"}),
            "cargo": forms.TextInput(attrs={"class": "form-control", "id": "id_cargo"}),
            "horario_atencion": forms.TextInput(attrs={"class": "form-control", "id": "id_horario_atencion"}),
        }

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if len(nombre_usuario) < 3 or re.search(r'\d', nombre_usuario):
            raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres y no puede contener números.')
        return nombre_usuario

    def clean_email(self):
        email = self.cleaned_data['email']
        if "@" not in email:
            raise ValidationError('Por favor, ingrese un correo electrónico válido.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6 or not re.search(r'[A-Z]', password) or len(re.findall(r'\d', password)) < 2 or '.' not in password:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres, incluyendo al menos una letra mayúscula, dos números y un punto.')
        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is not None: 
            telefono_str = str(telefono) 
            if not telefono_str.isdigit():
                raise ValidationError('El número de teléfono solo puede contener números.')
        else:
            raise ValidationError('Este campo es obligatorio.')
        return telefono

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_usuario", "telefono", "cargo", "horario_atencion", "is_active", "is_staff"]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"id": "id_nombre", "class": "form-control"}),
            "telefono": forms.TextInput(attrs={"id": "id_telefono", "class": "form-control"}),
            "cargo": forms.TextInput(attrs={"id": "id_cargo", "class": "form-control"}),
            "horario_atencion": forms.TextInput(attrs={"id": "id_horario_atencion", "class": "form-control"}),
        }

    def clean_nombre_usuario(self):
        nombre = self.cleaned_data.get('nombre_usuario')
        if not nombre:
            raise ValidationError('Por favor, complete el campo nombre.')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre
    
    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono')) 
        if not telefono:
            raise ValidationError('Por favor, complete el campo de teléfono.')
        if not re.match(r'^\d+$', telefono):
          raise ValidationError('El teléfono solo puede contener números.')
        return telefono

    def clean_cargo(self):
        cargo = self.cleaned_data.get('cargo')
        if not cargo:
            raise ValidationError('Por favor, complete el campo de cargo.')
        return cargo

    def clean_horario_atencion(self):
        horario = self.cleaned_data.get('horario_atencion')
        if not horario:
            raise ValidationError('Por favor, complete el campo de horario de atención.')
        return horario
        