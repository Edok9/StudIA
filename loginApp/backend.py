from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class TenantAwareBackend(ModelBackend):
    def authenticate(self, request, email=None, clave=None, **kwargs):
        try:
            tenant = request.tenant
            Usuario_Model = get_user_model()
            user = Usuario_Model.objects.get(email=email)
        except Usuario_Model.DoesNotExist:
            return None
        else:
            if user.check_password(clave):
                return user
