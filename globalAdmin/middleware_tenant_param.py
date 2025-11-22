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
    Se ejecuta ANTES de TenantMainMiddleware para modificar el hostname.
    
    Soporta:
    - ?tenant=DUOC%20UC (query parameter)
    - /tenant/duoc/ (path parameter)
    """
    
    def process_request(self, request):
        # Solo procesar si estamos en el dominio principal
        host = request.get_host()
        
        # Si ya estamos en un subdominio que funciona, no hacer nada
        if not (host.startswith('studia-8dmp.onrender.com') or host.startswith('localhost')):
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
                    with schema_context(get_public_schema_name()):
                        tenant = Empresa.objects.get(schema_name__iexact=tenant_slug.replace('-', ' '))
                        tenant_param = tenant.schema_name
                except (Empresa.DoesNotExist, Empresa.MultipleObjectsReturned):
                    pass
        
        # 3. Intentar leer desde la sesión (si ya se estableció antes y la sesión está disponible)
        if not tenant_param and hasattr(request, 'session'):
            tenant_param = request.session.get('tenant_schema_name', None)
        
        if tenant_param:
            try:
                with schema_context(get_public_schema_name()):
                    # Buscar el tenant por schema_name
                    tenant = Empresa.objects.get(schema_name=tenant_param)
                    
                    # Obtener el primer dominio del tenant
                    dominio = tenant.domains.filter(is_primary=True).first()
                    
                    if dominio:
                        # Guardar el hostname original
                        request._original_host = host
                        
                        # Guardar el tenant en la sesión para mantenerlo en requests posteriores
                        # Solo si la sesión está disponible (SessionMiddleware ya se ejecutó)
                        if hasattr(request, 'session'):
                            request.session['tenant_schema_name'] = tenant.schema_name
                        
                        # Modificar el hostname para que TenantMainMiddleware lo detecte
                        request.META['HTTP_HOST'] = dominio.domain
                        request.META['SERVER_NAME'] = dominio.domain.split(':')[0]  # Sin puerto
                        
                        sys.stdout.write(f'[TENANT PARAM] Tenant detectado: {tenant.schema_name} via parámetro/sesión\n')
                        sys.stdout.write(f'[TENANT PARAM] Hostname modificado a: {dominio.domain}\n')
                        sys.stdout.flush()
                    else:
                        sys.stdout.write(f'[TENANT PARAM] Tenant {tenant.schema_name} no tiene dominio configurado\n')
                        sys.stdout.flush()
                        
            except Empresa.DoesNotExist:
                sys.stdout.write(f'[TENANT PARAM] Tenant no encontrado: {tenant_param}\n')
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f'[TENANT PARAM] Error: {str(e)}\n')
                sys.stdout.flush()
        
        return None

