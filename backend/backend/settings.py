"""
Django settings for backend project.

Configuración optimizada para:
- Django REST Framework
- Documentación API con drf-yasg
- Panel de administración personalizado
- Configuración de CORS
- Entornos de desarrollo/producción
"""

from pathlib import Path
import os

# ==================== CONFIGURACIÓN BÁSICA ====================

# Directorio base del proyecto (se resuelve automáticamente)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para seguridad (¡NUNCA compartir en producción!)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-de-desarrollo')

# Modo debug (False en producción)
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts permitidos (ajustar en producción)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Configuración personalizada del admin
ADMIN_SITE_HEADER = "PixelMarket Admin"
ADMIN_SITE_TITLE = "Panel de Administración"
ADMIN_INDEX_TITLE = "Bienvenido al Panel de Control"

# ==================== APLICACIONES INSTALADAS ====================

INSTALLED_APPS = [
    # Apps de Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    
    
    # CORS (Comunicación con frontend)
    'corsheaders',
    
    # Tus aplicaciones
    'productos',
    'pedidos',
    'usuarios',
    'facturas',
]

# ==================== MIDDLEWARE ====================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Debe estar antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== CONFIGURACIÓN DE URLS ====================

ROOT_URLCONF = 'backend.urls'

# ==================== PLANTILLAS ====================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==================== BASE DE DATOS ====================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pixel_market_v2',
        'USER': 'Pixel_Team',
        'PASSWORD': 'P1x3l_M@rket!',
        'HOST': 'localhost', 
        'PORT': '3306',
    }
}

# ==================== VALIDACIÓN DE CONTRASEÑAS ====================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================== INTERNACIONALIZACIÓN ====================

LANGUAGE_CODE = 'es-ve'  # Español de Venezuela
TIME_ZONE = 'America/Caracas'  # Zona horaria de Venezuela
USE_I18N = True  # Habilita internacionalización
USE_L10N = True  # Habilita formatos locales
USE_TZ = True  # Usa zona horaria (recomendado)

# ==================== ARCHIVOS ESTÁTICOS Y MEDIA ====================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  

# ==================== DJANGO REST FRAMEWORK ====================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'productos.pagination.CustomPagination',
    'PAGE_SIZE': 10,  # Este será el tamaño por defecto, pero puede cambiarse con page_size
}

# ==================== CONFIGURACIÓN CORS ====================

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True

# ==================== CONFIGURACIÓN DRF-YASG (DOCUMENTACIÓN) ====================

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'DEFAULT_INFO': 'backend.urls.schema_info',
    'DEFAULT_API_URL': 'http://localhost:8000/api/',
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
    'HIDE_HOSTNAME': False,
}

# ==================== OTRAS CONFIGURACIONES ====================

# Tipo de campo automático por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tamaño máximo de upload (20MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520

# Configuración de sesión
SESSION_COOKIE_AGE = 1209600  # 2 semanas en segundos
SESSION_SAVE_EVERY_REQUEST = True

# Configuración de email (ejemplo)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP
EMAIL_PORT = 587  # Puerto para TLS
EMAIL_USE_TLS = True  # Cifrado TLS
EMAIL_HOST_USER = 'tucorreo@gmail.com'  # Usuario SMTP
EMAIL_HOST_PASSWORD = 'tupassword'  # Contraseña o App Password