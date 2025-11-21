"""
WSGI config for portalAutoatencion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')

# Ejecutar inicialización automática solo en producción (Render.com)
# Esto crea el administrador global si las variables de entorno están configuradas
if os.getenv('RENDER') or os.getenv('DATABASE_URL'):
    try:
        from scripts.init_production import init_production
        init_production()
    except Exception as e:
        # No fallar el despliegue si hay un error en la inicialización
        print(f"[WSGI] Error en inicialización (ignorado): {e}")

application = get_wsgi_application()
