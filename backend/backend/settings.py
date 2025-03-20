"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Base Directory del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Seguridad ---

# Clave secreta para la seguridad de tu proyecto (¡no debe compartirse!)
SECRET_KEY = 'django-insecure-uvg!+1^)=x%g)083+95zck-_hxhd%6^4&m&qukzqp2$-rjmp6v'

# Configuración de Debugging. En producción debe ser False
DEBUG = True

# Especifica qué hosts pueden acceder al proyecto
ALLOWED_HOSTS = []

# --- Django REST Framework (DRF) ---

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Solo permite respuestas en formato JSON
    ],
}


# --- Aplicaciones Instaladas ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    'corsheaders',  # Debe estar antes de las apps locales
    
    # Tus aplicaciones personalizadas
    'productos',  # App para manejar productos
    'pedidos',    # Nueva app para manejar pedidos (agrégala aquí)
    'usuarios',  # App para manejar usuarios
    'facturas',  # App para manejar facturas
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',  # Origen de tu frontend
]
# --- Middleware ---

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

# --- URLs ---

ROOT_URLCONF = 'backend.urls'

# --- Plantillas (Templates) ---

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Directorios donde buscar plantillas HTML (si los tienes)
        'APP_DIRS': True,  # Busca plantillas dentro de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Contexto de depuración
                'django.template.context_processors.request',  # Contexto de solicitud
                'django.contrib.auth.context_processors.auth',  # Contexto de autenticación
                'django.contrib.messages.context_processors.messages',  # Contexto de mensajes
            ],
        },
    },
]

# --- WSGI ---

WSGI_APPLICATION = 'backend.wsgi.application'


# --- Base de Datos ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Usamos MySQL como base de datos
        'NAME': 'Pixel_Market',  # Nombre de la base de datos
        'USER': 'Pixel_Market',  # Usuario de la base de datos
        'PASSWORD': 'pixelmarket1',  # Contraseña del usuario de la base de datos
        'HOST': 'localhost',  # Dirección del servidor de base de datos
        'PORT': '3306',  # Puerto para conectar con la base de datos
    }
}


# --- Validación de Contraseñas ---

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- Internacionalización (idioma y zona horaria) ---

LANGUAGE_CODE = 'en-us'  # Configuración del idioma

TIME_ZONE = 'UTC'  # Configuración de la zona horaria

USE_I18N = True  # Habilita la internacionalización

USE_TZ = True  # Habilita el uso de zonas horarias


# --- Archivos Estáticos (CSS, JavaScript, imágenes estáticas) ---

# URL pública para acceder a archivos estáticos
STATIC_URL = '/static/'

# Configuración para almacenar archivos estáticos adicionales en el directorio 'static'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Directorio adicional de archivos estáticos
]

# Solo necesario durante el desarrollo para servir archivos estáticos
if DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"  # Ruta donde se guardan los archivos estáticos procesados


# --- Archivos Multimedia (imágenes, documentos, etc.) ---

# URL pública para acceder a los archivos multimedia (como imágenes de productos)
MEDIA_URL = '/media/'

# Directorio en el que se guardarán los archivos multimedia cargados
MEDIA_ROOT = BASE_DIR / 'media'

# --- Clave primaria ---

# Tipo de campo para la clave primaria (auto-incrementable)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
