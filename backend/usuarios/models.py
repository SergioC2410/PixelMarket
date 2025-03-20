# Importaciones necesarias para el modelo
# AbstractUser: Clase base para crear un modelo de usuario personalizado.
# Group: Modelo que representa un grupo de usuarios.
# Permission: Modelo que representa un permisos específico.
from django.contrib.auth.models import AbstractUser, Group, Permission
# models: Proporciona clases base para definir modelos de datos en Django.
from django.db import models
# ValidationError: Excepción que se lanza cuando una validación falla.
from django.core.exceptions import ValidationError
# validate_email: Validador que verifica el formato de una dirección de correo electrónico.
from django.core.validators import validate_email
# PhoneNumberField: campo para la validacion de los numeros telefonicos
from phonenumber_field.modelfields import PhoneNumberField

# Definición del modelo de usuario personalizado
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Extiende el modelo de usuario predeterminado de Django con campos adicionales
    y funcionalidades específicas para el proyecto.
    """

    # Opciones para el campo 'rol'
    ROLES = (
        ('comprador', 'Comprador'),  # Rol de comprador
        ('vendedor', 'Vendedor'),    # Rol de vendedor
    )

    # Campos adicionales para el usuario
    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default='comprador',  # Valor predeterminado: comprador
        verbose_name='Rol del usuario'
    )
    telefono = PhoneNumberField(
        region='VE',  # Ajusta la región según tu país
        blank=True,   # El campo es opcional
        null=True,    # Puede ser NULL en la base de datos
        unique=True,  # El numero debe ser único en la base de datos
        verbose_name='Número de teléfono',
        help_text='Ej. +58 212 1235678'  # Mensaje de ayuda para el usuario
    )
    direccion = models.TextField(
        blank=True,  # El campo es opcional
        null=True,   # Puede ser NULL en la base de datos
        verbose_name='Dirección del usuario'
    )
    email = models.EmailField(
        unique=True,  # El email debe ser único en la base de datos
        blank=False,  # El campo es obligatorio
        null=False,   # No puede ser NULL en la base de datos
        verbose_name='Correo electrónico'
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
        related_name='usuarios_groups',  # Nombre de la relación inversa
        blank=True,  # El usuario puede no pertenecer a ningún grupo
        help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos asignados a sus grupos.',
        verbose_name='grupos'
    )

    # Relación ManyToMany con el modelo Permission (permisos de usuario)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_user_permissions',  # Nombre de la relación inversa
        blank=True,  # El usuario puede no tener permisos específicos
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario'
    )

    # Método para representar el usuario como una cadena (aparece en el panel de administración)
    def __str__(self):
        """
        Representación en cadena del usuario.
        Devuelve el nombre de usuario (username).
        """
        return self.username

    # Método para verificar si el usuario es un comprador
    def es_comprador(self):
        """
        Verifica si el usuario tiene el rol de comprador.
        Devuelve True si el rol es 'comprador', False en caso contrario.
        """
        return self.rol == 'comprador'

    # Método para verificar si el usuario es un vendedor
    def es_vendedor(self):
        """
        Verifica si el usuario tiene el rol de vendedor.
        Devuelve True si el rol es 'vendedor', False en caso contrario.
        """
        return self.rol == 'vendedor'

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



    # Mejoras sugeridas:
    # 1. Agregar validaciones personalizadas (ej: formato de teléfono).
    # 2. Implementar métodos útiles, como `es_vendedor()` o `es_comprador()`.