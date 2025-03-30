from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class FacturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facturas'
    verbose_name = _('Gestión de Facturas')
    
    # Configuración avanzada
    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Aquí podemos registrar señales o realizar configuraciones iniciales.
        """
        # Importar señales (si las tienes)
        try:
            from . import signals  # noqa: F401
        except ImportError:
            pass
        
        # Configurar logging específico
        import logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Aplicación {self.verbose_name} inicializada correctamente")