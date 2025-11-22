"""
Middleware para manejar peticiones cuando no se identifica un tenant.
"""
import sys
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class PublicRootMiddleware(MiddlewareMixin):
    """
    Middleware que captura peticiones a la raíz cuando no hay tenant
    y las redirige al panel de administración global.
    
    Este middleware debe ejecutarse DESPUÉS de TenantMainMiddleware
    para poder detectar cuando no se encontró un tenant.
    """
    def process_request(self, request):
        # Si estamos en la raíz y no se ha identificado un tenant aún,
        # verificar después de que TenantMainMiddleware se ejecute
        if request.path == '/' and not request.path.startswith('/global/'):
            # Marcar para verificar después en process_response
            request._check_public_root = True
        return None
    
    def process_response(self, request, response):
        # Si la respuesta es 404 o 500 en la raíz, verificar si es porque no hay tenant
        if (response.status_code in [404, 500] and request.path == '/' and 
            hasattr(request, '_check_public_root')):
            import sys
            sys.stdout.write(f'[PUBLIC ROOT] Detectado {response.status_code} en raíz\n')
            sys.stdout.flush()
            
            # Verificar si no se identificó un tenant o si estamos en el schema público
            from django_tenants.utils import get_public_schema_name
            public_schema = get_public_schema_name()
            
            try:
                # Verificar el tenant actual
                if hasattr(request, 'tenant'):
                    tenant_schema = getattr(request.tenant, 'schema_name', None)
                    sys.stdout.write(f'[PUBLIC ROOT] Tenant schema: {tenant_schema}\n')
                    sys.stdout.flush()
                    
                    # Si estamos en el schema público o no hay tenant, redirigir
                    if tenant_schema == public_schema or tenant_schema is None:
                        sys.stdout.write('[PUBLIC ROOT] Redirigiendo a /global/login/\n')
                        sys.stdout.flush()
                        return HttpResponseRedirect('/global/login/')
                else:
                    sys.stdout.write('[PUBLIC ROOT] No hay tenant, redirigiendo a /global/login/\n')
                    sys.stdout.flush()
                    return HttpResponseRedirect('/global/login/')
            except Exception as e:
                sys.stdout.write(f'[PUBLIC ROOT] ERROR: {str(e)}\n')
                sys.stdout.flush()
                # En caso de error, intentar redirigir de todas formas
                return HttpResponseRedirect('/global/login/')
        
        return response

