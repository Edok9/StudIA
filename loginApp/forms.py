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
    accion = forms.CharField()
    usuario = forms.CharField()
    correo_usuario = forms.EmailField()
    fecha_expiracion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

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