from django.test import TestCase
from .models import Categoria

class CategoriaModelTest(TestCase):
    def test_crear_categoria(self):
        # Crear una categoría
        categoria = Categoria.objects.create(
            nombre="Electrónica",
            descripcion="Productos electrónicos"
        )

        # Verificar que la categoría se haya creado correctamente
        self.assertEqual(categoria.nombre, "Electrónica")
        self.assertEqual(categoria.descripcion, "Productos electrónicos")
        self.assertEqual(str(categoria), "Electrónica")  # Verificar el método __str__