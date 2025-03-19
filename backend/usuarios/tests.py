from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.usuario_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
            'telefono': '12345678',
            'direccion': '123 Test St',
        }

    def test_crear_usuario(self):
        # Prueba para crear y guardar un usuario
        usuario = Usuario.objects.create_user(
            username=self.usuario_data['username'],
            email=self.usuario_data['email'],
            password=self.usuario_data['password'],
            telefono=self.usuario_data['telefono'],
            direccion=self.usuario_data['direccion']
        )
        usuario.save()

        # Verifica que el usuario se haya guardado correctamente
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(usuario.username, self.usuario_data['username'])
        self.assertEqual(usuario.email, self.usuario_data['email'])
        self.assertEqual(usuario.telefono, self.usuario_data['telefono'])
        self.assertEqual(usuario.direccion, self.usuario_data['direccion'])

    def test_validacion_telefono(self):
        # Prueba para verificar la validación del campo 'telefono'
        self.usuario_data['telefono'] = 'abc123'
        usuario = Usuario(**self.usuario_data)
        with self.assertRaises(ValidationError):
            usuario.full_clean()  # Llama a clean() y valida el modelo

    def test_validacion_email(self):
        # Prueba para verificar la validación del campo 'email'
        self.usuario_data['email'] = 'invalid-email'
        usuario = Usuario(**self.usuario_data)
        with self.assertRaises(ValidationError):
            usuario.full_clean()  # Llama a clean() y valida el modeloe.
