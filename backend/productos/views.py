from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Categoria, ImagenProducto
from .serializers import ProductoSerializer, CategoriaSerializer, ImagenProductoSerializer
from .pagination import CustomPagination  # Importar la paginación personalizada
from rest_framework.parsers import MultiPartParser, JSONParser
# ==================== VISTAS PARA PRODUCTOS ====================
class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'categoria': ['exact'],
        'precio': ['gte', 'lte']
    }
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']
    ordering_fields = ['precio', 'nombre', 'created_at']
    
    def perform_create(self, serializer):
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save()
        
        if imagen:
            instance.imagen = imagen
            instance.save()

    def get_queryset(self):
        return Producto.objects.filter(activo=True).select_related('categoria')

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    parser_classes = [MultiPartParser, JSONParser]
    lookup_field = 'id'

    def perform_update(self, serializer):
        imagen = self.request.FILES.get('imagen')
        instance = serializer.save()
        
        if imagen:
            instance.imagen = imagen
            instance.save()

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()

# ==================== VISTAS PARA IMÁGENES DE PRODUCTO ====================
class ImagenProductoViewSet(viewsets.ModelViewSet):
    queryset = ImagenProducto.objects.all()
    serializer_class = ImagenProductoSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        producto_id = self.request.query_params.get('producto')
        if producto_id:
            return ImagenProducto.objects.filter(producto_id=producto_id)
        return super().get_queryset()

# ==================== VISTAS PARA CATEGORÍAS ====================
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
