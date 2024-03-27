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
    periodo_reportes = forms.ChoiceField(choices=opciones, label="Periodo de Reportes")
    total_usuarios = forms.BooleanField(required=False, label="Total de Usuarios Registrados")

class Ise_Vpn_Form(forms.Form):
    ACCIONES_CHOICES = [
        ('', '-- Seleccione --'),
        ('Extensión de cuenta', 'Extensión de cuenta'),
        ('Cambio de contraseña', 'Cambio de contraseña'),
        ('Deshabilitación de cuenta', 'Deshabilitación de cuenta'),
    ]

    accion = forms.ChoiceField(choices=ACCIONES_CHOICES, label='Acción', required=True)
    usuario = forms.CharField(max_length=100, required=True)
    correo_usuario = forms.EmailField(required=True)
    fecha_expiracion = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    prefix = "Servicio VPN"

class Ioc_Automatico_Form(forms.Form):
    adjunto = forms.FileField(required=False)
    notas = forms.CharField()

    prefix = "IOC Automatico"

class Cambio_De_Ruta_Form(forms.Form):
    gateway = forms.CharField()
    interfaz_salida = forms.CharField()

    prefix = "Cambio de Ruta"      

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