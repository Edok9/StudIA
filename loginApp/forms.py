from django import forms
from .models import Usuario

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
    accion = forms.ChoiceField(choices=acciones, label="Accion")
    usuario = forms.CharField(label="Usuario de VPN")
    correo_usuario = forms.EmailField(label="Correo del Usuario")
    fecha_expiracion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Expiración", required=False)

    prefix = "Servicio VPN"

class Ioc_Automatico_Form(forms.Form):
    adjunto = forms.FileField(required=False)
    notas = forms.CharField()

    prefix = "IOC Automatico"

class Cambio_De_Ruta_Form(forms.Form):
    gateway = forms.CharField()
    interfaz_salida = forms.CharField()

    prefix = "Cambio de Ruta"      
        
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
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": design}))
    confirmar_nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": design}))

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_nueva_contraseña = cleaned_data.get("confirmar_nueva_contraseña")

        if nueva_contraseña != confirmar_nueva_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")

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
            "nombre_usuario": forms.TextInput(attrs={"class": design}),
            "email": forms.EmailInput(attrs={"class": design}),
            "password": forms.PasswordInput(attrs={"class": design}),
            "telefono": forms.TextInput(attrs={"class": design}),
            "cargo": forms.TextInput(attrs={"class": design}),
            "horario_atencion": forms.TextInput(attrs={"class": design}),
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
            "nombre_usuario": forms.TextInput(attrs={"class": design}),
            "telefono": forms.TextInput(attrs={"class": design}),
            "cargo": forms.TextInput(attrs={"class": design}),
            "horario_atencion": forms.TextInput(attrs={"class": design}),
        }