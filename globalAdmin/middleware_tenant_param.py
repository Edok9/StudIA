"""
Middleware para detectar el tenant desde un parámetro de URL.
Útil cuando no se pueden usar subdominios (como en Render.com).
"""
import sys
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name, schema_context
from clientManager.models import Empresa, Dominio


class TenantParamMiddleware(MiddlewareMixin):
    """
    Middleware que detecta el tenant desde un parámetro de query string o path.
    Se ejecuta DESPUÉS de TenantMainMiddleware para establecer el tenant si no se detectó.
    
    Soporta:
    - ?tenant=DUOC%20UC (query parameter)
    - /tenant/duoc/ (path parameter)
    """
    
    def process_request(self, request):
        # Guardar el parámetro del tenant en el request para usarlo después
        tenant_param = request.GET.get('tenant', None)
        
        # Intentar detectar desde path: /tenant/duoc/
        if not tenant_param and request.path.startswith('/tenant/'):
            path_parts = request.path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'tenant':
                tenant_slug = path_parts[2]
                # Buscar tenant por slug (nombre normalizado)
                try:
                    with schema_context(get_public_schema_name()):
                        tenant = Empresa.objects.get(schema_name__iexact=tenant_slug.replace('-', ' '))
                        tenant_param = tenant.schema_name
                except (Empresa.DoesNotExist, Empresa.MultipleObjectsReturned):
                    pass
        
        if tenant_param:
            request._tenant_param = tenant_param
        
        return None
    
    def process_response(self, request, response):
        # Si hay un parámetro de tenant y no se detectó un tenant, establecerlo
        if hasattr(request, '_tenant_param') and not hasattr(request, 'tenant'):
            try:
                with schema_context(get_public_schema_name()):
                    tenant = Empresa.objects.get(schema_name=request._tenant_param)
                    # Establecer el tenant en el request
                    request.tenant = tenant
                    # Establecer el schema en la conexión de base de datos
                    from django.db import connection
                    from django_tenants.postgresql_backend.base import DatabaseWrapper
                    if isinstance(connection, DatabaseWrapper):
                        connection.set_tenant(tenant)
                    
                    sys.stdout.write(f'[TENANT PARAM] Tenant establecido: {tenant.schema_name}\n')
                    sys.stdout.flush()
            except Empresa.DoesNotExist:
                sys.stdout.write(f'[TENANT PARAM] Tenant no encontrado: {request._tenant_param}\n')
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f'[TENANT PARAM] Error: {str(e)}\n')
                sys.stdout.flush()
        
        return response

