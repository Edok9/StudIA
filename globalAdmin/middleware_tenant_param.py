"""
Middleware para detectar el tenant desde un parámetro de URL.
Útil cuando no se pueden usar subdominios (como en Render.com).
"""
import sys
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name
from clientManager.models import Empresa, Dominio


class TenantParamMiddleware(MiddlewareMixin):
    """
    Middleware que detecta el tenant desde un parámetro de query string o path.
    Se ejecuta ANTES de TenantMainMiddleware.
    
    Soporta:
    - ?tenant=DUOC%20UC (query parameter)
    - /tenant/duoc/ (path parameter)
    """
    
    def process_request(self, request):
        # Solo procesar si estamos en el dominio principal (no subdominios)
        host = request.get_host()
        
        # Si ya hay un tenant detectado por hostname, no hacer nada
        # (esto significa que estamos usando subdominios y funciona normalmente)
        if not host.startswith('studia-8dmp.onrender.com') and not host.startswith('localhost'):
            return None
        
        # 1. Intentar detectar desde query parameter: ?tenant=DUOC%20UC
        tenant_param = request.GET.get('tenant', None)
        
        # 2. Intentar detectar desde path: /tenant/duoc/
        if not tenant_param and request.path.startswith('/tenant/'):
            path_parts = request.path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'tenant':
                tenant_slug = path_parts[2]
                # Buscar tenant por slug (nombre normalizado)
                try:
                    tenant = Empresa.objects.get(schema_name__iexact=tenant_slug.replace('-', ' '))
                    tenant_param = tenant.schema_name
                except (Empresa.DoesNotExist, Empresa.MultipleObjectsReturned):
                    pass
        
        if tenant_param:
            try:
                # Buscar el tenant por schema_name
                tenant = Empresa.objects.get(schema_name=tenant_param)
                
                # Obtener el primer dominio del tenant (o crear uno temporal)
                dominio = tenant.domains.filter(is_primary=True).first()
                
                if dominio:
                    # Modificar el hostname en el request para que TenantMainMiddleware lo detecte
                    # Guardar el hostname original
                    request._original_host = host
                    
                    # Modificar el hostname para que coincida con el dominio del tenant
                    # Esto hará que TenantMainMiddleware detecte el tenant correctamente
                    request.META['HTTP_HOST'] = dominio.domain
                    request.META['SERVER_NAME'] = dominio.domain.split(':')[0]  # Sin puerto
                    
                    sys.stdout.write(f'[TENANT PARAM] Tenant detectado: {tenant.schema_name} via parámetro\n')
                    sys.stdout.write(f'[TENANT PARAM] Hostname modificado a: {dominio.domain}\n')
                    sys.stdout.flush()
                    
            except Empresa.DoesNotExist:
                sys.stdout.write(f'[TENANT PARAM] Tenant no encontrado: {tenant_param}\n')
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f'[TENANT PARAM] Error: {str(e)}\n')
                sys.stdout.flush()
        
        return None

