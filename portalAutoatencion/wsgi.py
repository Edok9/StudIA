"""
WSGI config for portalAutoatencion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portalAutoatencion.settings')

application = get_wsgi_application()

# Ejecutar inicialización automática solo en producción (Render.com)
# Esto se ejecuta DESPUÉS de get_wsgi_application() para asegurar que Django esté configurado
# y solo cuando el servicio realmente inicia, no durante el build
if os.getenv('RENDER') or os.getenv('DATABASE_URL'):
    try:
        from scripts.init_production import init_production
        init_production()
    except Exception as e:
        # No fallar el despliegue si hay un error en la inicialización
        print(f"[WSGI] Error en inicialización (ignorado): {e}")