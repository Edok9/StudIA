"""
Autenticación personalizada para JWT con el modelo Usuario.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from loginApp.models import Usuario
from django_tenants.utils import schema_context


class CustomJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT personalizada que funciona con el modelo Usuario.
    """
    def authenticate(self, request):
        """
        Sobrescribir authenticate para guardar el request y poder usarlo en get_user.
        """
        # Llamar al método padre para validar el token
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        
        # Guardar el request para usarlo en get_user
        self.request = request
        
        # Obtener el usuario usando el token validado
        user = self.get_user(validated_token)
        
        return (user, validated_token)
    
    def get_user(self, validated_token):
        """
        Intenta encontrar y retornar un usuario usando el token validado.
        Debe ejecutarse dentro del schema_context del tenant.
        """
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken('Token no contiene información de usuario válida.')
        
        # Obtener el tenant del request si está disponible
        # El middleware ya debería haber establecido request.tenant
        request = getattr(self, 'request', None)
        if request and hasattr(request, 'tenant'):
            # Usar schema_context para asegurar que la query se ejecute en el schema correcto
            with schema_context(request.tenant.schema_name):
                try:
                    user = Usuario.objects.get(id_usuario=user_id)
                except Usuario.DoesNotExist:
                    raise AuthenticationFailed('Usuario no encontrado.')
                
                if not user.is_active:
                    raise AuthenticationFailed('Usuario inactivo.')
                
                return user
        else:
            # Si no hay tenant en el request, intentar sin schema_context (fallback)
            # Esto no debería pasar si el middleware está funcionando correctamente
            try:
                user = Usuario.objects.get(id_usuario=user_id)
            except Usuario.DoesNotExist:
                raise AuthenticationFailed('Usuario no encontrado.')
            
            if not user.is_active:
                raise AuthenticationFailed('Usuario inactivo.')
            
            return user

