from django.test import TestCase
from .models import Categoria

class CategoriaModelTest(TestCase):
    ELECTRONICA = "Electrónica"

    def test_crear_categoria(self):
        # Crear una categoría
        categoria = Categoria.objects.create(
            nombre=self.ELECTRONICA,
            descripcion="Productos electrónicos"
        )

        # Verificar que la categoría se haya creado correctamente
        self.assertEqual(categoria.nombre, self.ELECTRONICA)
        self.assertEqual(categoria.descripcion, "Productos electrónicos")
        self.assertEqual(str(categoria), self.ELECTRONICA)  # Verificar el método __str__