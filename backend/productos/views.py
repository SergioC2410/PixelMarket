from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer

# ==================== VISTAS PARA PRODUCTOS (CLASES BASADAS EN VISTAS GENÉRICAS) ====================
class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'precio']
    search_fields = ['nombre', 'descripcion']
    
    def perform_create(self, serializer):
        # Guardar imagen si viene en la petición
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save()
        
        if imagen:
            instance.imagen = imagen
            instance.save()

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = [MultiPartParser, JSONParser]  # Soporta actualización de imágenes

    def perform_update(self, serializer):
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save()
        
        if imagen:
            instance.imagen = imagen
            instance.save()

# ==================== VISTAS PARA CATEGORÍAS (USANDO @api_view PARA MÁXIMO CONTROL) ====================
@api_view(['GET', 'POST'])
def categoria_list(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def categoria_detail(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)