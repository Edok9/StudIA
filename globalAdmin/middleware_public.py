"""
Middleware para manejar peticiones cuando no se identifica un tenant.
"""
import sys
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class PublicRootMiddleware(MiddlewareMixin):
    """
    Middleware que captura peticiones a la raíz cuando no hay tenant
    y las redirige al panel de administración global.
    
    Este middleware debe ejecutarse DESPUÉS de TenantMainMiddleware
    para poder detectar cuando no se encontró un tenant.
    """
    def process_response(self, request, response):
        # Si la respuesta es 404 y estamos en la raíz, verificar si es porque no hay tenant
        if response.status_code == 404 and request.path == '/':
            import sys
            sys.stdout.write('[PUBLIC ROOT] Detectado 404 en raíz\n')
            sys.stdout.flush()
            
            # Verificar si no se identificó un tenant
            if not hasattr(request, 'tenant') or request.tenant is None:
                sys.stdout.write('[PUBLIC ROOT] No hay tenant, redirigiendo a /global/login/\n')
                sys.stdout.flush()
                return HttpResponseRedirect('/global/login/')
        
        return response

