from django import forms
from .models import Usuario

design = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"

class CambioClaveUsuarioForm(forms.Form):
    pass

class ReporteriaForm(forms.Form):
    opciones = (
        ("1", "24 Horas" ),
        ("2", "7 Días"),
        ("3", "1 Mes"),
    )
    periodo_reportes = forms.ChoiceField(choices=opciones, label="Periodo de Reportes")
    total_usuarios = forms.BooleanField(required=False, label="Total de Usuarios Registrados")

class Ise_Vpn_Form(forms.Form):
    accion = forms.CharField()
    usuario = forms.CharField()
    correo_usuario = forms.EmailField()
    fecha_expiracion = forms.DateInput()
    
    widgets = {
            "fecha_expiracion": forms.DateInput(attrs={'type': 'date'}),
        }

    prefix = "Servicio VPN"

class Ioc_Automatico_Form(forms.Form):
    adjunto = forms.FileField()
    notas = forms.CharField()

    prefix = "IOC Automatico"

class Cambio_De_Ruta_Form(forms.Form):
    gateway = forms.CharField()
    interfaz_salida = forms.CharField()

    prefix = "Cambio de Ruta"      

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