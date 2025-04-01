# Importaciones necesarias para el modelo
# AbstractUser: Clase base para crear un modelo de usuario personalizado.
# Group: Modelo que representa un grupo de usuarios.
# Permission: Modelo que representa un permisos específico.
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
# models: Proporciona clases base para definir modelos de datos en Django.
from django.db import models
# ValidationError: Excepción que se lanza cuando una validación falla.
from django.core.exceptions import ValidationError
# validate_email: Validador que verifica el formato de una dirección de correo electrónico.
from django.core.validators import validate_email
# PhoneNumberField: campo para la validacion de los numeros telefonicos
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

# Bancos de Venezuela (lista reducida)
BANCOS_NACIONALES = [
    ('0102', 'Banco de Venezuela'),
    ('0104', 'Venezolano de Crédito'),
    ('0105', 'Banco Mercantil'),
    ('0108', 'Banco Provincial'),
    ('0114', 'Bancaribe'),
    ('0115', 'Banco Exterior'),
    ('0116', 'Banco Occidental de Descuento (BOD)'),
    ('0128', 'Banco Caroní'),
    ('0134', 'Banesco'),
    ('0137', 'Banco Sofitasa'),
    ('0138', 'Banco Plaza'),
    ('0146', 'Banco de la Gente Emprendedora'),
    ('0151', 'BFC Banco Fondo Común'),
    ('0156', '100% Banco'),
    ('0157', 'DelSur Banco Universal'),
    ('0163', 'Banco del Tesoro'),
    ('0166', 'Banco Agrícola de Venezuela'),
    ('0168', 'Bancrecer'),
    ('0169', 'Mi Banco'),
    ('0171', 'Banco Activo'),
    ('0172', 'Bancamiga'),
    ('0174', 'Banplus'),
    ('0175', 'Banco Bicentenario'),
    ('0177', 'Banco de la Fuerza Armada Nacional Bolivariana (Banfanb)'),
]

ESTADOS_VENEZUELA = [
    ('AMA', 'Amazonas'),
    ('ANZ', 'Anzoátegui'),
    ('APU', 'Apure'),
    ('ARA', 'Aragua'),
    ('BAR', 'Barinas'),
    ('BOL', 'Bolívar'),
    ('CAR', 'Carabobo'),
    ('COJ', 'Cojedes'),
    ('DEL', 'Delta Amacuro'),
    ('FAL', 'Falcón'),
    ('GUA', 'Guárico'),
    ('LAR', 'Lara'),
    ('MER', 'Mérida'),
    ('MIR', 'Miranda'),
    ('MON', 'Monagas'),
    ('NES', 'Nueva Esparta'),
    ('POR', 'Portuguesa'),
    ('SUC', 'Sucre'),
    ('TAC', 'Táchira'),
    ('TRU', 'Trujillo'),
    ('VAR', 'Vargas'),
    ('YAR', 'Yaracuy'),
    ('ZUL', 'Zulia'),
]
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Ubicacion(models.Model):
    """Guarda la ubicación detallada del usuario en Venezuela"""
    usuario = models.OneToOneField(
        'Usuario',  # Usa comillas porque Usuario se define después
        on_delete=models.CASCADE,
        related_name='ubicacion'
    )
    estado = models.CharField(max_length=3, choices=ESTADOS_VENEZUELA)
    municipio = models.CharField(max_length=100)
    parroquia = models.CharField(max_length=100)
    direccion_exacta = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.usuario.email} - {self.estado}"

class MetodoPago(models.Model):
    """Métodos de pago asociados a un usuario"""
    TIPO_PAGO = [
        ('ZELLE', 'Zelle'),
        ('BINANCE', 'Binance'),
        ('PAGO_MOVIL', 'Pago Móvil'),
    ]
    
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='metodos_pago'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_PAGO)
    activo = models.BooleanField(default=True)
    
    # Campos específicos por tipo
    email_zelle = models.EmailField(blank=True, null=True)
    telefono_zelle = models.CharField(max_length=20, blank=True)
    email_binance = models.EmailField(blank=True, null=True)  
    banco_pago_movil = models.CharField(max_length=4, choices=BANCOS_NACIONALES, blank=True)
    telefono_pago_movil = PhoneNumberField(region='VE', blank=True, null=True)
    cedula_pago_movil = models.CharField(max_length=20, blank=True)

    def clean(self):
        """Valida campos requeridos según el tipo de pago"""
        if self.tipo == 'ZELLE' and not self.email_zelle:
            raise ValidationError('Zelle requiere un email asociado.')
        elif self.tipo == 'PAGO_MOVIL' and not self.banco_pago_movil:
            raise ValidationError('Pago Móvil requiere seleccionar un banco.')

    def __str__(self):
        return f"{self.usuario.email} - {self.tipo}"
# Definición del modelo de usuario personalizado
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Extiende el modelo de usuario predeterminado de Django con campos adicionales
    y funcionalidades específicas para el proyecto.
    """
    username = None
    
    email = models.EmailField(
        unique=True,  # El email debe ser único en la base de datos
        blank=False,  # El campo es obligatorio
        null=False,   # No puede ser NULL en la base de datos
        verbose_name='Correo electrónico'
    )
    
    # Configuración para usar email como identificador
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No se necesitan campos adicionales para crear un superusuario
    objects = UsuarioManager()
    # Campos adicionales
    telefono = PhoneNumberField(
        region='VE',  # Ajusta la región según tu país
        blank=True,   # El campo es opcional
        null=True,    # Puede ser NULL en la base de datos
        unique=True,  # El numero debe ser único en la base de datos
        verbose_name='Número de teléfono',
        help_text='Ej. +58 212 1235678'  # Mensaje de ayuda para el usuario
    )


    cedula = models.CharField(
        max_length=20,  # Ajusta la longitud según el formato de cédula en tu país
        unique=True,    # La cédula debe ser única en la base de datos
        blank=False,    # El campo es obligatorio
        null=False,     # No puede ser NULL en la base de datos
        verbose_name='Cédula',
        help_text='Ingrese su número de cédula (solo números).'  # Mensaje de ayuda
    )
    
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,  # Se establece automáticamente al crear el usuario
        verbose_name='Fecha de registro'
    )

    # Relación ManyToMany con el modelo Group (grupos de usuarios)
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_groups',  # 
        blank=True,
        help_text='...'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_user_permissions',  
        blank=True,
        help_text='...'
    )
    first_name = models.CharField(max_length=15, blank=False)
    last_name = models.CharField(max_length=15, blank=False)
    

    # Método para representar el usuario como una cadena (aparece en el panel de administración)
    def __str__(self):
        """

        Representación en cadena del usuario (ahora usando email).
        """
        return self.email

    # Método para obtener el nombre completo del usuario
    def nombre_completo(self):
        """
        Devuelve el nombre completo del usuario, combinando first_name y last_name.
        """
        return f"{self.first_name} {self.last_name}"

    # Método para validar los campos del usuario antes de guardar
    def clean(self):
        """
        Valida los campos del usuario antes de guardar en la base de datos.
        Se ejecuta automáticamente cuando se llama a `full_clean()` o `save()`.
        """
        super().clean()  # Llama al método clean() de la clase padre (AbstractUser)

        # Validación del campo 'email'
        try:
            validate_email(self.email)  # Valida que el email tenga un formato válido
        except ValidationError:
            raise ValidationError({'email': 'Ingresa un correo electrónico válido.'})
        
        if not self.cedula.isdigit():
            raise ValidationError({'cedula': 'La cédula debe contener solo números.'})
        if len(self.cedula) < 7 or len(self.cedula) > 20:
            raise ValidationError({'cedula': 'La cédula debe tener entre 7 y 20 dígitos.'})


    # Mejoras sugeridas:
    # 1. Agregar validaciones personalizadas (ej: formato de teléfono).
    # 2. Implementar métodos útiles, como `es_vendedor()` o `es_comprador()`.